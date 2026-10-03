from datetime import datetime, timedelta

import pytest

from excepciones import EntradaYaUtilizada, EventoNoCorrespondeAlDia, TicketNoEmitido
from main import app
from models import Entrada, EstadoEntrada, Evento
from repositories import EntradaRepositorySQL
from routers.acceso import get_reloj
from services.acceso_service import AccesoService

HOY = datetime(2026, 12, 1, 21, 30)
FECHA_DEL_EVENTO_DE_HOY = "2026-12-01T21:00:00"
FECHA_DEL_EVENTO_DE_MANANA = "2026-12-02T21:00:00"

MENSAJE_ACCESO = "Acceso Permitido"
MENSAJE_INEXISTENTE = "Ticket Inválido o Inexistente"
MENSAJE_NO_EMITIDO = "Ticket no emitido / Falta de pago"
MENSAJE_YA_UTILIZADA = "Entrada ya utilizada"
MENSAJE_OTRO_DIA = "La entrada no corresponde al evento del día"


class RelojFijo:
    """Doble de prueba: devuelve siempre la hora configurada, que el test puede cambiar."""

    def __init__(self, ahora: datetime):
        self.ahora = ahora

    def __call__(self) -> datetime:
        return self.ahora


@pytest.fixture
def reloj():
    reloj = RelojFijo(HOY)
    app.dependency_overrides[get_reloj] = lambda: reloj
    return reloj


def _crear_evento(client, fecha=FECHA_DEL_EVENTO_DE_HOY):
    lugar = client.post("/lugares", json={"nombre": "Estadio", "direccion": "Calle 1"}).json()
    platea = client.post(
        "/sectores", json={"lugar_id": lugar["id"], "nombre": "Platea", "capacidad_maxima": 3}
    ).json()
    creado = client.post(
        "/eventos",
        json={
            "lugar_id": lugar["id"],
            "nombre": "Rock Fest",
            "fecha": fecha,
            "precios": [{"sector_id": platea["id"], "precio": 12000}],
        },
    ).json()
    return creado["id"]


def _entrada_en_estado(session_factory, evento_id, estado, hora_ingreso=None):
    """Deja una entrada del evento en el estado pedido y devuelve su id y su codigo QR."""
    db = session_factory()
    entrada = db.query(Entrada).filter_by(evento_id=evento_id).order_by(Entrada.id).first()
    entrada.estado = estado
    entrada.hora_ingreso = hora_ingreso
    db.commit()
    return entrada.id, entrada.codigo_qr


def _escanear(client, codigo_qr):
    return client.post("/escanear-acceso", json={"codigo_qr": codigo_qr})


def _leer_entrada(session_factory, entrada_id):
    return session_factory().get(Entrada, entrada_id)


def test_escenario_1_entrada_emitida_del_dia_permite_el_acceso(client, session_factory, reloj):
    evento_id = _crear_evento(client)
    entrada_id, codigo_qr = _entrada_en_estado(session_factory, evento_id, EstadoEntrada.EMITIDA)

    respuesta = _escanear(client, codigo_qr)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["mensaje"] == MENSAJE_ACCESO
    assert cuerpo["id"] == entrada_id
    assert cuerpo["codigo_qr"] == codigo_qr
    assert cuerpo["estado"] == "Utilizada"
    assert datetime.fromisoformat(cuerpo["hora_ingreso"]) == HOY

    entrada = _leer_entrada(session_factory, entrada_id)
    assert entrada.estado == EstadoEntrada.UTILIZADA
    assert entrada.hora_ingreso == HOY


def test_escenario_2_entrada_ya_utilizada_es_rechazada_sin_pisar_la_hora(
    client, session_factory, reloj
):
    evento_id = _crear_evento(client)
    entrada_id, codigo_qr = _entrada_en_estado(session_factory, evento_id, EstadoEntrada.EMITIDA)

    primero = _escanear(client, codigo_qr)
    reloj.ahora = HOY + timedelta(minutes=10)
    segundo = _escanear(client, codigo_qr)

    assert primero.status_code == 200
    assert segundo.status_code == 409
    assert segundo.json()["detail"] == MENSAJE_YA_UTILIZADA
    entrada = _leer_entrada(session_factory, entrada_id)
    assert entrada.estado == EstadoEntrada.UTILIZADA
    assert entrada.hora_ingreso == HOY


def test_escenario_3_codigo_qr_inexistente(client, reloj):
    _crear_evento(client)

    respuesta = _escanear(client, "no-existe")

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == MENSAJE_INEXISTENTE


@pytest.mark.parametrize("estado", [EstadoEntrada.DISPONIBLE, EstadoEntrada.RESERVADA])
def test_escenario_4_entrada_no_emitida_es_rechazada(client, session_factory, reloj, estado):
    evento_id = _crear_evento(client)
    entrada_id, codigo_qr = _entrada_en_estado(session_factory, evento_id, estado)

    respuesta = _escanear(client, codigo_qr)

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == MENSAJE_NO_EMITIDO
    entrada = _leer_entrada(session_factory, entrada_id)
    assert entrada.estado == estado
    assert entrada.hora_ingreso is None


def test_entrada_de_un_evento_de_otro_dia_es_rechazada_y_sigue_emitida(
    client, session_factory, reloj
):
    evento_id = _crear_evento(client, fecha=FECHA_DEL_EVENTO_DE_MANANA)
    entrada_id, codigo_qr = _entrada_en_estado(session_factory, evento_id, EstadoEntrada.EMITIDA)

    respuesta = _escanear(client, codigo_qr)

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == MENSAJE_OTRO_DIA
    entrada = _leer_entrada(session_factory, entrada_id)
    assert entrada.estado == EstadoEntrada.EMITIDA
    assert entrada.hora_ingreso is None


def test_el_estado_se_valida_antes_que_la_fecha_del_evento(client, session_factory, reloj):
    evento_id = _crear_evento(client, fecha=FECHA_DEL_EVENTO_DE_MANANA)
    _, codigo_qr = _entrada_en_estado(session_factory, evento_id, EstadoEntrada.RESERVADA)

    respuesta = _escanear(client, codigo_qr)

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == MENSAJE_NO_EMITIDO


def test_rechaza_un_cuerpo_sin_codigo_qr(client, reloj):
    assert client.post("/escanear-acceso", json={}).status_code == 422


def test_el_ingreso_atomico_falla_si_otra_sesion_ya_dejo_entrar_la_entrada(
    client, session_factory
):
    evento_id = _crear_evento(client)
    entrada_id, _ = _entrada_en_estado(session_factory, evento_id, EstadoEntrada.EMITIDA)
    sesion_a = session_factory()
    entrada_vista_por_a = sesion_a.get(Entrada, entrada_id)

    sesion_b = session_factory()
    entrada_de_b = sesion_b.get(Entrada, entrada_id)
    entrada_de_b.registrar_ingreso(HOY)
    EntradaRepositorySQL(sesion_b).registrar_ingreso(entrada_de_b)

    entrada_vista_por_a.registrar_ingreso(HOY + timedelta(minutes=5))  # en memoria sigue EMITIDA
    with pytest.raises(EntradaYaUtilizada):
        EntradaRepositorySQL(sesion_a).registrar_ingreso(entrada_vista_por_a)

    entrada = _leer_entrada(session_factory, entrada_id)
    assert entrada.estado == EstadoEntrada.UTILIZADA
    assert entrada.hora_ingreso == HOY


def test_dos_escaneos_simultaneos_dejan_entrar_a_uno_solo(client, session_factory):
    evento_id = _crear_evento(client)
    entrada_id, codigo_qr = _entrada_en_estado(session_factory, evento_id, EstadoEntrada.EMITIDA)

    class RepositorioAdelantado(EntradaRepositorySQL):
        """Entre la lectura y la escritura otro escaneo ya hizo entrar a la entrada."""

        def buscar_por_codigo_qr(self, codigo):
            entrada = super().buscar_por_codigo_qr(codigo)
            otra = session_factory()
            ganadora = otra.get(Entrada, entrada.id)
            ganadora.registrar_ingreso(HOY)
            EntradaRepositorySQL(otra).registrar_ingreso(ganadora)
            return entrada

    servicio = AccesoService(
        RepositorioAdelantado(session_factory()), lambda: HOY + timedelta(minutes=5)
    )

    with pytest.raises(EntradaYaUtilizada):
        servicio.escanear_acceso(codigo_qr)

    entrada = _leer_entrada(session_factory, entrada_id)
    assert entrada.estado == EstadoEntrada.UTILIZADA
    assert entrada.hora_ingreso == HOY


def test_buscar_por_codigo_qr_devuelve_none_si_no_existe(session_factory):
    assert EntradaRepositorySQL(session_factory()).buscar_por_codigo_qr("nada") is None


def test_entrada_emitida_del_dia_registra_su_ingreso():
    evento = Evento(nombre="Rock Fest", fecha=datetime(2026, 12, 1, 21, 0))
    entrada = Entrada(estado=EstadoEntrada.EMITIDA, codigo_qr="qr", evento=evento)

    entrada.registrar_ingreso(HOY)

    assert entrada.estado == EstadoEntrada.UTILIZADA
    assert entrada.hora_ingreso == HOY


def test_entrada_rechaza_el_ingreso_segun_su_estado_sin_modificarse():
    evento = Evento(nombre="Rock Fest", fecha=datetime(2026, 12, 1, 21, 0))
    anterior = datetime(2026, 12, 1, 20, 0)

    utilizada = Entrada(
        estado=EstadoEntrada.UTILIZADA, codigo_qr="a", evento=evento, hora_ingreso=anterior
    )
    with pytest.raises(EntradaYaUtilizada):
        utilizada.registrar_ingreso(HOY)
    assert utilizada.hora_ingreso == anterior

    for estado in (EstadoEntrada.DISPONIBLE, EstadoEntrada.RESERVADA):
        entrada = Entrada(estado=estado, codigo_qr="b", evento=evento)
        with pytest.raises(TicketNoEmitido):
            entrada.registrar_ingreso(HOY)
        assert entrada.estado == estado
        assert entrada.hora_ingreso is None


def test_entrada_emitida_de_otro_dia_no_registra_el_ingreso():
    evento = Evento(nombre="Rock Fest", fecha=datetime(2026, 12, 2, 21, 0))
    entrada = Entrada(estado=EstadoEntrada.EMITIDA, codigo_qr="qr", evento=evento)

    with pytest.raises(EventoNoCorrespondeAlDia):
        entrada.registrar_ingreso(HOY)

    assert entrada.estado == EstadoEntrada.EMITIDA
    assert entrada.hora_ingreso is None


def test_evento_responde_si_es_el_evento_del_dia():
    evento = Evento(nombre="Rock Fest", fecha=datetime(2026, 12, 1, 21, 0))

    assert evento.es_del_dia(datetime(2026, 12, 1, 0, 0))
    assert evento.es_del_dia(datetime(2026, 12, 1, 23, 59))
    assert not evento.es_del_dia(datetime(2026, 11, 30, 23, 59))
    assert not evento.es_del_dia(datetime(2026, 12, 2, 0, 0))

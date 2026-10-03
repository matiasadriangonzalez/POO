from decimal import Decimal

import pytest

from excepciones import EntradaNoDisponible, TransicionInvalida
from main import app
from models import Entrada, EstadoEntrada, EstadoVenta, Venta
from pasarela import (
    TARJETA_RECHAZADA,
    DatosTarjeta,
    PasarelaPago,
    PasarelaPagoSimulada,
    RespuestaPago,
)
from repositories import EntradaRepositorySQL
from routers.pago import get_pasarela

TARJETA_APROBADA = "1111222233334444"
MENSAJE_NO_DISPONIBLE = "Los lugares seleccionados ya no se encuentran disponibles"


class PasarelaEspia(PasarelaPago):
    """Doble de prueba: registra las llamadas y responde siempre lo mismo."""

    def __init__(self, aprobar: bool):
        self._aprobar = aprobar
        self.llamadas: list[tuple[DatosTarjeta, Decimal]] = []

    def procesar_pago(self, tarjeta: DatosTarjeta, monto: Decimal) -> RespuestaPago:
        self.llamadas.append((tarjeta, monto))
        return RespuestaPago(aprobado=self._aprobar)


class PasarelaQueFalla(PasarelaPago):
    def procesar_pago(self, tarjeta: DatosTarjeta, monto: Decimal) -> RespuestaPago:
        raise RuntimeError("pasarela caida")


def _crear_evento(client, nombre="Rock Fest"):
    lugar = client.post("/lugares", json={"nombre": "Estadio", "direccion": "Calle 1"}).json()
    platea = client.post(
        "/sectores", json={"lugar_id": lugar["id"], "nombre": "Platea", "capacidad_maxima": 5}
    ).json()
    creado = client.post(
        "/eventos",
        json={
            "lugar_id": lugar["id"],
            "nombre": nombre,
            "fecha": "2026-12-01T21:00:00",
            "precios": [{"sector_id": platea["id"], "precio": 12000}],
        },
    ).json()
    return {"id": creado["id"], "platea": platea["id"]}


@pytest.fixture
def evento(client):
    return _crear_evento(client)


@pytest.fixture
def cliente(client):
    return client.post("/clientes", json={"nombre": "Ana", "email": "ana@mail.com"}).json()


@pytest.fixture
def pasarela_aprueba():
    pasarela = PasarelaEspia(aprobar=True)
    app.dependency_overrides[get_pasarela] = lambda: pasarela
    return pasarela


@pytest.fixture
def pasarela_rechaza():
    pasarela = PasarelaEspia(aprobar=False)
    app.dependency_overrides[get_pasarela] = lambda: pasarela
    return pasarela


def _elegir_entradas(client, evento, cantidad=2):
    respuesta = client.post(
        "/cotizar",
        json={"evento_id": evento["id"], "sector_id": evento["platea"], "cantidad": cantidad},
    )
    return respuesta.json()["entrada_ids"]


def _pagar(client, cliente_id, entrada_ids, numero=TARJETA_APROBADA):
    return client.post(
        "/iniciar-pago",
        json={
            "cliente_id": cliente_id,
            "entrada_ids": entrada_ids,
            "tarjeta": {"numero": numero, "titular": "Ana Perez"},
        },
    )


def _estados_de_entradas(session_factory, entrada_ids):
    db = session_factory()
    return {e.estado for e in db.query(Entrada).filter(Entrada.id.in_(entrada_ids)).all()}


def _cantidad_de_ventas(session_factory):
    return session_factory().query(Venta).count()


def test_escenario_1_pago_aprobado_emite_las_entradas_con_qr(
    client, session_factory, evento, cliente
):
    entrada_ids = _elegir_entradas(client, evento, 2)

    respuesta = _pagar(client, cliente["id"], entrada_ids)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "Pagada"
    assert Decimal(cuerpo["total"]) == Decimal("24000")
    assert {e["id"] for e in cuerpo["entradas"]} == set(entrada_ids)
    for entrada in cuerpo["entradas"]:
        assert entrada["estado"] == "Emitida"
        assert entrada["codigo_qr"]

    db = session_factory()
    venta = db.get(Venta, cuerpo["id"])
    assert venta.estado == EstadoVenta.PAGADA
    assert venta.cliente_id == cliente["id"]
    assert venta.total == Decimal("24000")
    assert {e.id for e in venta.entradas} == set(entrada_ids)
    assert _estados_de_entradas(session_factory, entrada_ids) == {EstadoEntrada.EMITIDA}


def test_escenario_1_la_pasarela_recibe_la_tarjeta_y_el_total(
    client, evento, cliente, pasarela_aprueba
):
    entrada_ids = _elegir_entradas(client, evento, 2)

    _pagar(client, cliente["id"], entrada_ids)

    assert len(pasarela_aprueba.llamadas) == 1
    tarjeta, monto = pasarela_aprueba.llamadas[0]
    assert tarjeta.numero == TARJETA_APROBADA
    assert tarjeta.titular == "Ana Perez"
    assert monto == Decimal("24000")


def test_escenario_2_tarjeta_rechazada_por_la_pasarela_simulada(
    client, session_factory, evento, cliente
):
    entrada_ids = _elegir_entradas(client, evento, 2)

    respuesta = _pagar(client, cliente["id"], entrada_ids, numero=TARJETA_RECHAZADA)

    assert respuesta.status_code == 402
    assert respuesta.json()["detail"] == "Pago denegado"
    assert _cantidad_de_ventas(session_factory) == 0
    assert _estados_de_entradas(session_factory, entrada_ids) == {EstadoEntrada.DISPONIBLE}


def test_escenario_2_pasarela_que_siempre_rechaza_libera_las_entradas(
    client, session_factory, evento, cliente, pasarela_rechaza
):
    entrada_ids = _elegir_entradas(client, evento, 2)

    respuesta = _pagar(client, cliente["id"], entrada_ids)

    assert respuesta.status_code == 402
    assert respuesta.json()["detail"] == "Pago denegado"
    assert len(pasarela_rechaza.llamadas) == 1
    assert _cantidad_de_ventas(session_factory) == 0
    assert _estados_de_entradas(session_factory, entrada_ids) == {EstadoEntrada.DISPONIBLE}


def test_escenario_2_las_entradas_liberadas_se_pueden_volver_a_pagar(
    client, evento, cliente
):
    entrada_ids = _elegir_entradas(client, evento, 2)
    _pagar(client, cliente["id"], entrada_ids, numero=TARJETA_RECHAZADA)

    respuesta = _pagar(client, cliente["id"], entrada_ids)

    assert respuesta.status_code == 200


def test_si_la_pasarela_falla_se_liberan_las_entradas(client, session_factory, evento, cliente):
    app.dependency_overrides[get_pasarela] = lambda: PasarelaQueFalla()
    entrada_ids = _elegir_entradas(client, evento, 2)

    with pytest.raises(RuntimeError):
        _pagar(client, cliente["id"], entrada_ids)

    assert _cantidad_de_ventas(session_factory) == 0
    assert _estados_de_entradas(session_factory, entrada_ids) == {EstadoEntrada.DISPONIBLE}


def test_escenario_3_entradas_ya_no_disponibles_abortan_antes_de_la_pasarela(
    client, session_factory, evento, cliente, pasarela_aprueba
):
    entrada_ids = _elegir_entradas(client, evento, 2)
    db = session_factory()
    for entrada in db.query(Entrada).filter(Entrada.id.in_(entrada_ids)).all():
        entrada.estado = EstadoEntrada.EMITIDA
    db.commit()

    respuesta = _pagar(client, cliente["id"], entrada_ids)

    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == MENSAJE_NO_DISPONIBLE
    assert pasarela_aprueba.llamadas == []
    assert _cantidad_de_ventas(session_factory) == 0


def test_escenario_3_si_una_sola_no_esta_disponible_no_se_reserva_ninguna(
    client, session_factory, evento, cliente, pasarela_aprueba
):
    entrada_ids = _elegir_entradas(client, evento, 2)
    db = session_factory()
    db.get(Entrada, entrada_ids[0]).estado = EstadoEntrada.RESERVADA
    db.commit()

    respuesta = _pagar(client, cliente["id"], entrada_ids)

    assert respuesta.status_code == 409
    assert pasarela_aprueba.llamadas == []
    assert _estados_de_entradas(session_factory, [entrada_ids[1]]) == {
        EstadoEntrada.DISPONIBLE
    }


def test_un_segundo_pago_sobre_las_mismas_entradas_recibe_409(
    client, evento, cliente, pasarela_aprueba
):
    entrada_ids = _elegir_entradas(client, evento, 2)

    primero = _pagar(client, cliente["id"], entrada_ids)
    segundo = _pagar(client, cliente["id"], entrada_ids)

    assert primero.status_code == 200
    assert segundo.status_code == 409
    assert segundo.json()["detail"] == MENSAJE_NO_DISPONIBLE
    assert len(pasarela_aprueba.llamadas) == 1


def test_rechaza_un_cliente_inexistente(
    client, session_factory, evento, pasarela_aprueba
):
    entrada_ids = _elegir_entradas(client, evento, 2)

    respuesta = _pagar(client, 999, entrada_ids)

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Cliente no encontrado"
    assert pasarela_aprueba.llamadas == []
    assert _estados_de_entradas(session_factory, entrada_ids) == {EstadoEntrada.DISPONIBLE}


def test_rechaza_una_entrada_inexistente_sin_tocar_las_demas(
    client, session_factory, evento, cliente, pasarela_aprueba
):
    entrada_ids = _elegir_entradas(client, evento, 2)

    respuesta = _pagar(client, cliente["id"], entrada_ids + [9999])

    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == MENSAJE_NO_DISPONIBLE
    assert pasarela_aprueba.llamadas == []
    assert _estados_de_entradas(session_factory, entrada_ids) == {EstadoEntrada.DISPONIBLE}


def test_rechaza_ids_de_entrada_duplicados(
    client, session_factory, evento, cliente, pasarela_aprueba
):
    entrada_ids = _elegir_entradas(client, evento, 1)

    respuesta = _pagar(client, cliente["id"], entrada_ids * 2)

    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == MENSAJE_NO_DISPONIBLE
    assert pasarela_aprueba.llamadas == []
    assert _estados_de_entradas(session_factory, entrada_ids) == {EstadoEntrada.DISPONIBLE}


def test_rechaza_entradas_de_distintos_eventos(
    client, session_factory, evento, cliente, pasarela_aprueba
):
    otro_evento = _crear_evento(client, nombre="Jazz Night")
    ids = _elegir_entradas(client, evento, 1) + _elegir_entradas(client, otro_evento, 1)

    respuesta = _pagar(client, cliente["id"], ids)

    assert respuesta.status_code == 400
    assert pasarela_aprueba.llamadas == []
    assert _estados_de_entradas(session_factory, ids) == {EstadoEntrada.DISPONIBLE}


def test_rechaza_una_lista_de_entradas_vacia(client, cliente):
    assert _pagar(client, cliente["id"], []).status_code == 422


def test_la_reserva_atomica_falla_si_otra_sesion_gano_las_entradas(
    client, session_factory, evento
):
    entrada_ids = _elegir_entradas(client, evento, 2)
    sesion_a = session_factory()
    entradas_vistas_por_a = sesion_a.query(Entrada).filter(Entrada.id.in_(entrada_ids)).all()

    sesion_b = session_factory()
    for entrada in sesion_b.query(Entrada).filter(Entrada.id.in_(entrada_ids)).all():
        entrada.estado = EstadoEntrada.RESERVADA
    sesion_b.commit()

    for entrada in entradas_vistas_por_a:
        entrada.reservar()  # en memoria sigue viendose DISPONIBLE
    with pytest.raises(EntradaNoDisponible):
        EntradaRepositorySQL(sesion_a).reservar(entradas_vistas_por_a)

    assert _estados_de_entradas(session_factory, entrada_ids) == {EstadoEntrada.RESERVADA}


def test_la_reserva_atomica_es_todo_o_nada(client, session_factory, evento):
    entrada_ids = _elegir_entradas(client, evento, 2)
    sesion_a = session_factory()
    entradas_vistas_por_a = sesion_a.query(Entrada).filter(Entrada.id.in_(entrada_ids)).all()

    sesion_b = session_factory()
    sesion_b.get(Entrada, entrada_ids[0]).estado = EstadoEntrada.RESERVADA
    sesion_b.commit()

    for entrada in entradas_vistas_por_a:
        entrada.reservar()
    with pytest.raises(EntradaNoDisponible):
        EntradaRepositorySQL(sesion_a).reservar(entradas_vistas_por_a)

    assert _estados_de_entradas(session_factory, [entrada_ids[1]]) == {
        EstadoEntrada.DISPONIBLE
    }


@pytest.mark.parametrize(
    "numero, aprobado",
    [(TARJETA_RECHAZADA, False), (TARJETA_APROBADA, True), ("4000000000000001", True)],
)
def test_la_pasarela_simulada_solo_rechaza_la_tarjeta_de_prueba(numero, aprobado):
    respuesta = PasarelaPagoSimulada().procesar_pago(
        DatosTarjeta(numero=numero, titular="Ana"), Decimal("100")
    )

    assert respuesta.aprobado is aprobado


def test_entrada_valida_sus_propias_transiciones():
    entrada = Entrada(estado=EstadoEntrada.DISPONIBLE, codigo_qr="qr")

    assert entrada.esta_disponible()
    entrada.reservar()
    assert entrada.estado == EstadoEntrada.RESERVADA
    assert not entrada.esta_disponible()
    entrada.liberar()
    assert entrada.estado == EstadoEntrada.DISPONIBLE
    entrada.reservar()
    entrada.emitir()
    assert entrada.estado == EstadoEntrada.EMITIDA


def test_entrada_rechaza_transiciones_invalidas():
    entrada = Entrada(estado=EstadoEntrada.DISPONIBLE, codigo_qr="qr")
    with pytest.raises(TransicionInvalida):
        entrada.emitir()
    with pytest.raises(TransicionInvalida):
        entrada.liberar()

    entrada.estado = EstadoEntrada.EMITIDA
    with pytest.raises(EntradaNoDisponible):
        entrada.reservar()


def test_venta_solo_se_confirma_desde_pendiente():
    venta = Venta(cliente_id=1, estado=EstadoVenta.PENDIENTE, entradas=[])

    venta.confirmar_pago()

    assert venta.estado == EstadoVenta.PAGADA
    with pytest.raises(TransicionInvalida):
        venta.confirmar_pago()

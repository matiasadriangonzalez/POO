from decimal import Decimal

import pytest

from models import Entrada, EstadoEntrada


@pytest.fixture
def evento(client):
    lugar = client.post("/lugares", json={"nombre": "Estadio", "direccion": "Calle 1"}).json()
    platea = client.post(
        "/sectores", json={"lugar_id": lugar["id"], "nombre": "Platea", "capacidad_maxima": 5}
    ).json()
    vip = client.post(
        "/sectores", json={"lugar_id": lugar["id"], "nombre": "VIP", "capacidad_maxima": 1}
    ).json()
    creado = client.post(
        "/eventos",
        json={
            "lugar_id": lugar["id"],
            "nombre": "Rock Fest",
            "fecha": "2026-12-01T21:00:00",
            "precios": [
                {"sector_id": platea["id"], "precio": 12000},
                {"sector_id": vip["id"], "precio": 30000},
            ],
        },
    ).json()
    return {"id": creado["id"], "platea": platea["id"], "vip": vip["id"]}


def _cotizar(client, evento_id, sector_id, cantidad):
    return client.post(
        "/cotizar",
        json={"evento_id": evento_id, "sector_id": sector_id, "cantidad": cantidad},
    )


def test_escenario_1_cotizacion_exitosa_calcula_el_subtotal(client, evento):
    respuesta = _cotizar(client, evento["id"], evento["platea"], 2)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert Decimal(cuerpo["total"]) == Decimal("24000")
    assert len(cuerpo["entrada_ids"]) == 2
    assert len(set(cuerpo["entrada_ids"])) == 2


def test_escenario_2_rechaza_si_no_hay_entradas_suficientes(client, evento):
    respuesta = _cotizar(client, evento["id"], evento["vip"], 3)

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "Capacidad insuficiente"


def test_escenario_2_no_cuenta_las_entradas_que_ya_no_estan_disponibles(
    client, session_factory, evento
):
    db = session_factory()
    ocupadas = db.query(Entrada).filter_by(sector_id=evento["platea"]).limit(4).all()
    for entrada in ocupadas:
        entrada.estado = EstadoEntrada.EMITIDA
    db.commit()

    respuesta = _cotizar(client, evento["id"], evento["platea"], 2)

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "Capacidad insuficiente"


@pytest.mark.parametrize("cantidad", [0, -1])
def test_escenario_3_rechaza_cantidades_invalidas(client, evento, cantidad):
    respuesta = _cotizar(client, evento["id"], evento["platea"], cantidad)

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "Cantidad inválida"


def test_cotizar_no_modifica_el_estado_de_las_entradas(client, session_factory, evento):
    _cotizar(client, evento["id"], evento["platea"], 2)

    estados = {e.estado for e in session_factory().query(Entrada).all()}
    assert estados == {EstadoEntrada.DISPONIBLE}


def test_rechaza_un_evento_inexistente(client):
    assert _cotizar(client, 999, 1, 1).status_code == 404


def test_rechaza_un_sector_sin_precio_en_el_evento(client, evento):
    assert _cotizar(client, evento["id"], 999, 1).status_code == 404

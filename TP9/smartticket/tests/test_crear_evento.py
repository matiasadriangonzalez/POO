import pytest

from models import Entrada, EstadoEntrada, PrecioSector


@pytest.fixture
def lugar_con_sectores(client):
    lugar = client.post("/lugares", json={"nombre": "Estadio", "direccion": "Calle 1"}).json()
    platea = client.post(
        "/sectores", json={"lugar_id": lugar["id"], "nombre": "Platea", "capacidad_maxima": 3}
    ).json()
    vip = client.post(
        "/sectores", json={"lugar_id": lugar["id"], "nombre": "VIP", "capacidad_maxima": 2}
    ).json()
    return lugar, platea, vip


def _evento(lugar_id, precios):
    return {
        "lugar_id": lugar_id,
        "nombre": "Rock Fest",
        "fecha": "2026-12-01T21:00:00",
        "precios": precios,
    }


def test_crear_evento_genera_una_entrada_por_cada_lugar_de_cada_sector(
    client, session_factory, lugar_con_sectores
):
    lugar, platea, vip = lugar_con_sectores

    respuesta = client.post(
        "/eventos",
        json=_evento(
            lugar["id"],
            [
                {"sector_id": platea["id"], "precio": 12000},
                {"sector_id": vip["id"], "precio": 30000},
            ],
        ),
    )

    assert respuesta.status_code == 201
    db = session_factory()
    por_sector = {
        sector_id: db.query(Entrada).filter_by(sector_id=sector_id).count()
        for sector_id in (platea["id"], vip["id"])
    }
    assert por_sector == {platea["id"]: 3, vip["id"]: 2}
    assert db.query(PrecioSector).count() == 2


def test_las_entradas_nacen_disponibles_con_qr_unico(client, session_factory, lugar_con_sectores):
    lugar, platea, vip = lugar_con_sectores
    client.post(
        "/eventos",
        json=_evento(
            lugar["id"],
            [
                {"sector_id": platea["id"], "precio": 12000},
                {"sector_id": vip["id"], "precio": 30000},
            ],
        ),
    )

    entradas = session_factory().query(Entrada).all()

    assert len(entradas) == 5
    assert all(e.estado == EstadoEntrada.DISPONIBLE for e in entradas)
    assert len({e.codigo_qr for e in entradas}) == 5


def test_rechaza_evento_si_falta_el_precio_de_un_sector(client, lugar_con_sectores):
    lugar, platea, _ = lugar_con_sectores

    respuesta = client.post(
        "/eventos",
        json=_evento(lugar["id"], [{"sector_id": platea["id"], "precio": 12000}]),
    )

    assert respuesta.status_code == 400


def test_rechaza_evento_con_precio_de_un_sector_ajeno_al_lugar(client, lugar_con_sectores):
    lugar, platea, vip = lugar_con_sectores

    respuesta = client.post(
        "/eventos",
        json=_evento(
            lugar["id"],
            [
                {"sector_id": platea["id"], "precio": 12000},
                {"sector_id": vip["id"], "precio": 30000},
                {"sector_id": 999, "precio": 1000},
            ],
        ),
    )

    assert respuesta.status_code == 400


def test_rechaza_evento_de_un_lugar_inexistente(client):
    respuesta = client.post("/eventos", json=_evento(999, []))

    assert respuesta.status_code == 404

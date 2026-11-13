"""Tests de caracterizacion de los endpoints CRUD (lugares, sectores, clientes, eventos).

Fijan el comportamiento HTTP (codigos y `detail`) que debe conservarse al mover la logica
de los routers a los servicios.
"""

import pytest


def _crear_lugar(client, nombre="Estadio", direccion="Calle 1"):
    return client.post("/lugares", json={"nombre": nombre, "direccion": direccion}).json()


def _crear_sector(client, lugar_id, nombre="Platea", capacidad=3):
    return client.post(
        "/sectores",
        json={"lugar_id": lugar_id, "nombre": nombre, "capacidad_maxima": capacidad},
    ).json()


def _crear_evento(client, lugar_id, sector_id):
    return client.post(
        "/eventos",
        json={
            "lugar_id": lugar_id,
            "nombre": "Rock Fest",
            "fecha": "2026-12-01T21:00:00",
            "precios": [{"sector_id": sector_id, "precio": 1000}],
        },
    ).json()


# --- Lugares ---


def test_crear_lugar_devuelve_201_con_id(client):
    respuesta = client.post("/lugares", json={"nombre": "Estadio", "direccion": "Calle 1"})

    assert respuesta.status_code == 201
    assert respuesta.json() == {"id": 1, "nombre": "Estadio", "direccion": "Calle 1"}


def test_listar_lugares_devuelve_todos(client):
    assert client.get("/lugares").json() == []
    _crear_lugar(client, "A")
    _crear_lugar(client, "B")

    respuesta = client.get("/lugares")

    assert respuesta.status_code == 200
    assert [lugar["nombre"] for lugar in respuesta.json()] == ["A", "B"]


def test_obtener_lugar_por_id(client):
    lugar = _crear_lugar(client)

    respuesta = client.get(f"/lugares/{lugar['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json() == lugar


def test_obtener_lugar_inexistente_devuelve_404(client):
    respuesta = client.get("/lugares/999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Lugar no encontrado"}


def test_crear_lugar_sin_direccion_devuelve_422(client):
    assert client.post("/lugares", json={"nombre": "Estadio"}).status_code == 422


def test_obtener_lugar_con_id_no_numerico_devuelve_422(client):
    assert client.get("/lugares/abc").status_code == 422


# --- Sectores ---


def test_crear_sector_devuelve_201_con_id(client):
    lugar = _crear_lugar(client)

    respuesta = client.post(
        "/sectores",
        json={"lugar_id": lugar["id"], "nombre": "Platea", "capacidad_maxima": 3},
    )

    assert respuesta.status_code == 201
    assert respuesta.json() == {
        "id": 1,
        "lugar_id": lugar["id"],
        "nombre": "Platea",
        "capacidad_maxima": 3,
    }


def test_crear_sector_con_lugar_inexistente_devuelve_404(client):
    respuesta = client.post(
        "/sectores", json={"lugar_id": 999, "nombre": "Platea", "capacidad_maxima": 3}
    )

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Lugar no encontrado"}


def test_listar_sectores_devuelve_todos(client):
    lugar = _crear_lugar(client)
    assert client.get("/sectores").json() == []
    _crear_sector(client, lugar["id"], "Platea")
    _crear_sector(client, lugar["id"], "VIP")

    respuesta = client.get("/sectores")

    assert respuesta.status_code == 200
    assert [sector["nombre"] for sector in respuesta.json()] == ["Platea", "VIP"]


def test_obtener_sector_por_id(client):
    lugar = _crear_lugar(client)
    sector = _crear_sector(client, lugar["id"])

    respuesta = client.get(f"/sectores/{sector['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json() == sector


def test_obtener_sector_inexistente_devuelve_404(client):
    respuesta = client.get("/sectores/999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Sector no encontrado"}


def test_crear_sector_sin_capacidad_devuelve_422(client):
    lugar = _crear_lugar(client)

    respuesta = client.post("/sectores", json={"lugar_id": lugar["id"], "nombre": "Platea"})

    assert respuesta.status_code == 422


# --- Clientes ---


def test_crear_cliente_devuelve_201_con_id(client):
    respuesta = client.post("/clientes", json={"nombre": "Ana", "email": "ana@mail.com"})

    assert respuesta.status_code == 201
    assert respuesta.json() == {"id": 1, "nombre": "Ana", "email": "ana@mail.com"}


def test_listar_clientes_devuelve_todos(client):
    assert client.get("/clientes").json() == []
    client.post("/clientes", json={"nombre": "Ana", "email": "ana@mail.com"})
    client.post("/clientes", json={"nombre": "Beto", "email": "beto@mail.com"})

    respuesta = client.get("/clientes")

    assert respuesta.status_code == 200
    assert [cliente["nombre"] for cliente in respuesta.json()] == ["Ana", "Beto"]


def test_obtener_cliente_por_id(client):
    cliente = client.post("/clientes", json={"nombre": "Ana", "email": "ana@mail.com"}).json()

    respuesta = client.get(f"/clientes/{cliente['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json() == cliente


def test_obtener_cliente_inexistente_devuelve_404(client):
    respuesta = client.get("/clientes/999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Cliente no encontrado"}


def test_crear_cliente_sin_email_devuelve_422(client):
    assert client.post("/clientes", json={"nombre": "Ana"}).status_code == 422


# --- Eventos ---


def test_listar_eventos_devuelve_todos(client):
    lugar = _crear_lugar(client)
    sector = _crear_sector(client, lugar["id"])
    assert client.get("/eventos").json() == []
    evento = _crear_evento(client, lugar["id"], sector["id"])

    respuesta = client.get("/eventos")

    assert respuesta.status_code == 200
    assert respuesta.json() == [evento]


def test_obtener_evento_por_id(client):
    lugar = _crear_lugar(client)
    sector = _crear_sector(client, lugar["id"])
    evento = _crear_evento(client, lugar["id"], sector["id"])

    respuesta = client.get(f"/eventos/{evento['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json() == evento
    assert respuesta.json()["precios"] == [{"sector_id": sector["id"], "precio": "1000.00"}]


def test_obtener_evento_inexistente_devuelve_404(client):
    respuesta = client.get("/eventos/999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Evento no encontrado"}


def test_crear_evento_con_lugar_inexistente_devuelve_404(client):
    respuesta = client.post(
        "/eventos",
        json={
            "lugar_id": 999,
            "nombre": "Rock Fest",
            "fecha": "2026-12-01T21:00:00",
            "precios": [],
        },
    )

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Lugar no encontrado"}


@pytest.mark.parametrize("fecha", ["no-es-fecha", None])
def test_crear_evento_con_fecha_invalida_devuelve_422(client, fecha):
    lugar = _crear_lugar(client)

    respuesta = client.post(
        "/eventos",
        json={"lugar_id": lugar["id"], "nombre": "Rock Fest", "fecha": fecha, "precios": []},
    )

    assert respuesta.status_code == 422


@pytest.mark.parametrize("capacidad", [0, -5])
def test_crear_sector_con_capacidad_no_positiva_devuelve_422(client, capacidad):
    lugar = _crear_lugar(client)

    respuesta = client.post(
        "/sectores",
        json={"lugar_id": lugar["id"], "nombre": "Platea", "capacidad_maxima": capacidad},
    )

    assert respuesta.status_code == 422

def test_webhook_pagos_acepta_una_notificacion(client):
    respuesta = client.post("/webhook-pagos", json={"evento": "pago.aprobado", "venta_id": 1})

    assert respuesta.status_code == 200
    assert respuesta.json() == {"recibido": True}


def test_webhook_pagos_acepta_cuerpo_vacio(client):
    respuesta = client.post("/webhook-pagos")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"recibido": True}

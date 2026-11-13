from typing import Any

from fastapi import APIRouter, Body

router = APIRouter(prefix="/webhook-pagos", tags=["Pago"])


@router.post("", summary="Webhook de la pasarela de pagos (esqueleto)")
def recibir_webhook(payload: dict[str, Any] | None = Body(default=None)):
    """Recibe notificaciones asincrónicas de la pasarela de pagos.

    Es un esqueleto: el enunciado no define su comportamiento. El pago actual es
    sincrónico a través de `PasarelaPago`, por lo que este endpoint solo confirma la recepción.
    """
    return {"recibido": True}

from fastapi import FastAPI

import models  # noqa: F401  (registra las tablas en Base.metadata)
from database import Base, engine
import manejador_excepciones
from routers import acceso, cliente, cotizacion, evento, lugar, pago, sector, webhook

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartTicket API",
    description="Venta de entradas y control de acceso.",
    version="0.1.0",
)

manejador_excepciones.registrar(app)

app.include_router(lugar.router)
app.include_router(sector.router)
app.include_router(evento.router)
app.include_router(cliente.router)
app.include_router(cotizacion.router)
app.include_router(pago.router)
app.include_router(acceso.router)
app.include_router(webhook.router)

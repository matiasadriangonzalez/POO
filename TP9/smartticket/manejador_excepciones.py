from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from excepciones import (
    CantidadInvalida,
    CapacidadInsuficiente,
    ClienteNoEncontrado,
    EntradaNoDisponible,
    EntradaYaUtilizada,
    EntradasDeDistintosEventos,
    ErrorDeDominio,
    EventoNoCorrespondeAlDia,
    EventoNoEncontrado,
    LugarNoEncontrado,
    PagoDenegado,
    PreciosInvalidos,
    SectorNoEncontradoEnEvento,
    TicketInvalido,
    TicketNoEmitido,
    TransicionInvalida,
)

CODIGO_HTTP = {
    LugarNoEncontrado: 404,
    EventoNoEncontrado: 404,
    SectorNoEncontradoEnEvento: 404,
    PreciosInvalidos: 400,
    CantidadInvalida: 400,
    CapacidadInsuficiente: 400,
    ClienteNoEncontrado: 404,
    EntradaNoDisponible: 409,
    EntradasDeDistintosEventos: 400,
    PagoDenegado: 402,
    TransicionInvalida: 409,
    TicketInvalido: 404,
    TicketNoEmitido: 400,
    EntradaYaUtilizada: 409,
    EventoNoCorrespondeAlDia: 400,
}


def registrar(app: FastAPI) -> None:
    @app.exception_handler(ErrorDeDominio)
    def manejar(_: Request, error: ErrorDeDominio) -> JSONResponse:
        codigo = CODIGO_HTTP.get(type(error), 400)
        return JSONResponse(status_code=codigo, content={"detail": error.mensaje})

# PARTE A: excepciones personalizadas.
# Cada clase representa un tipo de error propio del dominio del ejercicio.


class StringException(Exception):
    """Error de validación para cadenas obligatorias."""


class EnteroPositivoException(Exception):
    """Error de validación para enteros que deben ser positivos."""


class CollectionVaciaException(Exception):
    """La operación requiere una colección con elementos."""


class NoEncontradoException(Exception):
    """No se encontró el elemento solicitado."""
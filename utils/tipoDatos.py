# Tipo de datos disponibles para anotaciones

from enum import Enum, auto

class TipoDatos(Enum):

    TEXTO         = auto()
    NUMERO        = auto()
    FLOTANTE      = auto()
    BOOLEANO      = auto()
    IDENTIFICADOR = auto()
    LLAMADA = auto()



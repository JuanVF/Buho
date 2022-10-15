# Tipo de operandos aritmeticos disponibles para anotaciones

from enum import Enum, auto

class OperandosAritmeticos(Enum):

    MAS     = auto()
    MENOS   = auto()
    POR     = auto()
    ENTRE   = auto()
    RESIDUO = auto()
    ELEVADO = auto()
    MODULO  = auto()
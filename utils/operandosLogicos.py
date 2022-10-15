# Tipo de operandos logicos disponibles para anotaciones

from enum import Enum, auto

class OperandosLogicos(Enum):
    MENOR       = auto()
    MAYOR       = auto()
    MENOR_IGUAL = auto()
    MAYOR_IGUAL = auto()
    DIFERENTE   = auto()
    IGUAL       = auto()
    Y           = auto()
    O           = auto()
    NO          = auto()
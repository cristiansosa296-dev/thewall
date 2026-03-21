from enum import Enum


class Direccion(Enum):
    ADELANTE = 0
    ATRAS = 1


class Velocidad(Enum):
    BAJA = 1
    ALTA = 2


class Movimiento(Enum):
    FRENAR = 0
    ADELANTE = 1
    ATRAS = 2
    IZQUIERDA = 3
    DERECHA = 4

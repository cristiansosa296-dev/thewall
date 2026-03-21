import time
from .motor import Motor
from .types import Direccion, Velocidad, Movimiento


class RobotDrive:
    def __init__(self, config):
        self.izquierdo = Motor(config.motor_izquierdo)
        self.derecho = Motor(config.motor_derecho)

        self.velocidad = Velocidad.BAJA
        self.movimiento = Movimiento.FRENAR
        self.last_update = time.time()

    def set_velocidad(self, velocidad: Velocidad):
        self.velocidad = velocidad

    def forward(self):
        self.movimiento = Movimiento.ADELANTE
        self.izquierdo.mover(Direccion.ADELANTE, self.velocidad)
        self.derecho.mover(Direccion.ADELANTE, self.velocidad)
        self._update_time()

    def backward(self):
        self.movimiento = Movimiento.ATRAS
        self.izquierdo.mover(Direccion.ATRAS, self.velocidad)
        self.derecho.mover(Direccion.ATRAS, self.velocidad)
        self._update_time()

    def girar_izquierda(self):
        self.movimiento = Movimiento.IZQUIERDA
        self.izquierdo.mover(Direccion.ADELANTE, Velocidad.BAJA)
        self.derecho.mover(Direccion.ADELANTE, Velocidad.ALTA)
        self._update_time()

    def girar_derecha(self):
        self.movimiento = Movimiento.DERECHA
        self.izquierdo.mover(Direccion.ADELANTE, Velocidad.ALTA)
        self.derecho.mover(Direccion.ADELANTE, Velocidad.BAJA)
        self._update_time()

    def detenerse(self):
        self.movimiento = Movimiento.FRENAR
        self.izquierdo.detenerse()
        self.derecho.detenerse()
        self._update_time()

    def obtener_estado(self):
        return {
            "movimiento": self.movimiento.name,
            "velocidad": self.velocidad.name,
            "timestamp": self.last_update
        }

    def _update_time(self):
        self.last_update = time.time()

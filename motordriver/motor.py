import RPi.GPIO as GPIO
from .tipos import Direccion, Velocidad


class Motor:
    def __init__(self, config):
        self.config = config

        GPIO.setup(self.config.marcha_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.config.velocidad_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.config.sentido_pin, GPIO.OUT, initial=GPIO.LOW)

        self.mireccion = Direccion.ADELANTE
        self.velocidad = Velocidad.BAJA
        self.marcha = False

    def mover(self, direccion: Direccion, velocidad: Velocidad):
        self.marcha = True
        self.direccion = direccion
        self.velocidad = velocidad

        GPIO.output(self.config.marcha_pin, GPIO.HIGH)

        GPIO.output(
            self.config.sentido_pin,
            GPIO.LOW if direccion == Direccion.ADELANTE else GPIO.HIGH
        )

        GPIO.output(
            self.config.velocidad_pin,
            GPIO.LOW if velocidad == Velocidad.BAJA else GPIO.HIGH
        )

    def detenerse(self):
        GPIO.output(self.config.marcha_pin, GPIO.LOW)
        GPIO.output(self.config.velocidad_pin, GPIO.LOW)
        GPIO.output(self.config.sentido_pin, GPIO.LOW)

        self.marcha = False


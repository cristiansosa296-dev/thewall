from flask import Flask, jsonify, request
from flask_cors import CORS
import atexit
import os
import RPi.GPIO as GPIO

from motordriver.config import MotorConfig, RobotConfig
from motordriver.robot import RobotDrive
from motordriver.tipos import Velocidad


app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": [
#     "http://192.168.1.50:8000",
#     "http://localhost:8000"
# ]}})

# =========================
# Inicialización de hardware
# =========================
GPIO.setmode(GPIO.BCM)

config = RobotConfig(
    motor_izquierdo=MotorConfig(marcha_pin=23, velocidad_pin=24, sentido_pin=18),
    motor_derecho=MotorConfig(marcha_pin=17, velocidad_pin=22, sentido_pin=27),
)

robot = RobotDrive(config)


@atexit.register
def limpiar_al_salir():
    try:
        robot.detenerse()
    finally:
        GPIO.cleanup()


# =========================
# Helpers
# =========================
def parsear_velocidad(valor: str) -> Velocidad:
    valor = str(valor).strip().lower()
    if valor in {"1", "low", "baja"}:
        return Velocidad.BAJA
    if valor in {"2", "high", "alta"}:
        return Velocidad.ALTA
    raise ValueError("Velocidad inválida. Usa 1/2, low/high o baja/alta.")


def respuesta_ok(**extra):
    payload = {"ok": True, **extra}
    return jsonify(payload), 200


def respuesta_error(mensaje: str, estado: int = 400):
    return jsonify({"ok": False, "error": mensaje}), estado


# =========================
# Endpoints
# =========================
@app.get("/salud")
def salud():
    return respuesta_ok(servicio="robot-api")


@app.get("/estado")
def estado():
    return respuesta_ok(estado=robot.get_state())


@app.post("/velocidad")
def setear_velocidad():
    data = request.get_json(silent=True) or {}
    valor = data.get("velocidad")
    if valor is None:
        return respuesta_error("Falta el campo 'velocidad'.")

    try:
        velocidad = parsear_velocidad(valor)
    except ValueError as exc:
        return respuesta_error(str(exc))

    robot.set_velocidad(velocidad)
    return respuesta_ok(mensaje="Velocidad actualizada.", estado=robot.get_estado())


@app.post("/mover/adelante")
def mover_adelante():
    robot.adelante()
    return respuesta_ok(mensaje="Movimiento adelante.", estado=robot.get_estado())


@app.post("/mover/atras")
def mover_atras():
    robot.atras()
    return respuesta_ok(mensaje="Movimiento atrás.", estado=robot.get_estado())


@app.post("/mover/izquierda")
def mover_izquierda():
    robot.girar_izquierda()
    return respuesta_ok(mensaje="Giro a la izquierda.", estado=robot.get_estado())


@app.post("/mover/derecha")
def mover_derecha():
    robot.girar_derecha()
    return respuesta_ok(mensaje="Giro a la derecha.", estado=robot.get_estado())


@app.post("/detener")
def detener():
    robot.detenerse()
    return respuesta_ok(mensaje="Robot detenido.", estado=robot.get_estado())


@app.post("/comando")
def comando():
    data = request.get_json(silent=True) or {}
    accion = str(data.get("accion", "")).strip().lower()

    if not accion:
        return respuesta_error("Falta el campo 'accion'.")

    if accion == "adelante":
        robot.adelante()
    elif accion == "atras":
        robot.atras()
    elif accion == "izquierda":
        robot.girar_izquierda()
    elif accion == "derecha":
        robot.girar_derecha()
    elif accion == "detener":
        robot.detenerse()
    else:
        return respuesta_error("Acción inválida. Usa adelante, atras, izquierda, derecha o detener.")

    return respuesta_ok(mensaje=f"Comando ejecutado: {accion}", estado=robot.get_estado())


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port, debug=False)

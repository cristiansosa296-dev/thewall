import sys
import tty
import termios
import select
import time
import RPi.GPIO as GPIO

from motordriver.config import MotorConfig, RobotConfig
from motordriver.robot import RobotDrive
from motordriver.tipos import Velocidad


def get_key(timeout=0.1):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            return sys.stdin.read(1)
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main():
    GPIO.setmode(GPIO.BCM)

    config = RobotConfig(
        motor_izquierdo=MotorConfig(marcha_pin=23, velocidad_pin=24, sentido_pin=18),
        motor_derecho=MotorConfig(marcha_pin=17, velocidad_pin=22, sentido_pin=27),
    )

    robot = RobotDrive(config)

    print("Control por teclado")
    print("w=adelante | s=atras | a=izquierda | d=derecha")
    print("1=vel baja | 2=vel alta | x=stop | q=salir")

    try:
        while True:
            key = get_key()

            if key is None:
                robot.detenerse()
                continue

            if key == "1":
                robot.set_velocidad(Velocidad.BAJA)
                print("Velocidad: BAJA")

            elif key == "2":
                robot.set_velocidad(Velocidad.ALTA)
                print("Velocidad: ALTA")

            elif key == "w":
                robot.adelante()
                print("Adelante")

            elif key == "s":
                robot.atras()
                print("Atras")

            elif key == "a":
                robot.girar_izquierda()
                print("Izquierda")

            elif key == "d":
                robot.girar_derecha()
                print("Derecha")

            elif key == "x":
                robot.detenerse()
                print("Stop")

            elif key == "q":
                print("Saliendo...")
                break

            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nInterrumpido.")

    finally:
        robot.detenerse()
        GPIO.cleanup()


if __name__ == "__main__":
    main()

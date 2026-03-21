from dataclasses import dataclass

@dataclass
class MotorConfig:
    marcha_pin: int
    velocidad_pin: int
    sentido_pin: int


@dataclass
class RobotConfig:
    motor_izquierdo: MotorConfig
    motor_derecho: MotorConfig

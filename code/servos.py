# servos.py - Door and bird servo sequences for cuckoo clock

import machine
import time

import config

_door = None
_bird = None


def init():
    """Initialize PWM for both servos. Call once at startup."""
    global _door, _bird
    _door = machine.PWM(machine.Pin(config.PIN_SERVO_DOOR))
    _door.freq(1000 * 1000 // config.SERVO_PERIOD_US)
    _bird = machine.PWM(machine.Pin(config.PIN_SERVO_BIRD))
    _bird.freq(1000 * 1000 // config.SERVO_PERIOD_US)
    # Start closed/in
    _set_duty_us(_door, config.SERVO_DOOR_CLOSED)
    _set_duty_us(_bird, config.SERVO_BIRD_IN)


def _set_duty_us(pwm, us):
    """Set PWM duty in microseconds (period = SERVO_PERIOD_US)."""
    pwm.duty_ns(us * 1000)


def run_cuckoo_sequence():
    """
    Run full cuckoo sequence: open door -> bird out -> (caller plays sound) -> bird in -> close door.
    Caller should play cuckoo audio between bird_out() and bird_in() or during the open phase.
    """
    open_door()
    time.sleep_ms(config.SERVO_MOVE_MS)
    bird_out()
    time.sleep_ms(config.SERVO_MOVE_MS)
    # Caller plays cuckoo here; we wait a minimum then retract
    time.sleep_ms(800)
    bird_in()
    time.sleep_ms(config.SERVO_MOVE_MS)
    close_door()


def open_door():
    _set_duty_us(_door, config.SERVO_DOOR_OPEN)


def close_door():
    _set_duty_us(_door, config.SERVO_DOOR_CLOSED)


def bird_out():
    _set_duty_us(_bird, config.SERVO_BIRD_OUT)


def bird_in():
    _set_duty_us(_bird, config.SERVO_BIRD_IN)

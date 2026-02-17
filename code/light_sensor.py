# light_sensor.py - BH1750 ambient light sensor (I2C) for night mode

import machine
import time

import config

# BH1750 default I2C address
BH1750_ADDR = 0x23
# One-time high-res mode
BH1750_OT_HR = 0x20

_i2c = None


def init():
    """Initialize I2C and BH1750. Call once at startup."""
    global _i2c
    _i2c = machine.I2C(0, scl=machine.Pin(config.PIN_I2C_SCL), sda=machine.Pin(config.PIN_I2C_SDA), freq=400000)


def read_lux():
    """
    Read ambient light in lux. Returns float.
    Returns 0.0 on read error (e.g. sensor not present).
    """
    global _i2c
    if _i2c is None:
        init()
    try:
        _i2c.writeto(BH1750_ADDR, bytes([BH1750_OT_HR]))
        time.sleep_ms(120)  # One-time high-res conversion time
        buf = _i2c.readfrom(BH1750_ADDR, 2)
        return (buf[0] << 8 | buf[1]) / 1.2
    except OSError:
        return 0.0


def is_night_mode():
    """True if ambient light is below night-mode threshold (do not chime)."""
    return read_lux() < config.NIGHT_MODE_LUX_THRESHOLD

# clock_logic.py - When to chime (time + night mode) and run cuckoo sequence

import time

import config
import light_sensor
import servos
import audio


_last_chime_minute = -1  # Avoid double chime in same minute


def should_chime_now():
    """
    True if we are on a chime boundary (:00 and optionally :30) and not in night mode.
    Uses RTC (set by NTP). Coarse: check once per minute from main loop.
    """
    global _last_chime_minute
    if light_sensor.is_night_mode():
        return False
    t = time.localtime()
    minute = t[4]
    hour = t[3]
    if minute == 0:
        pass  # Full hour
    elif config.CHIME_AT_HALF_HOUR and minute == 30:
        pass  # Half hour
    else:
        return False
    # Only once per minute
    key = hour * 60 + minute
    if key == _last_chime_minute:
        return False
    _last_chime_minute = key
    return True


def trigger_cuckoo(volume=None, manual=False):
    """
    Run full cuckoo: servos + cuckoo sound.
    If manual=True, caller may skip night-mode check (already done by web handler).
    """
    # Run servo sequence; play cuckoo during the open phase
    def do_sequence():
        servos.open_door()
        time.sleep_ms(config.SERVO_MOVE_MS)
        servos.bird_out()
        time.sleep_ms(config.SERVO_MOVE_MS)
        audio.play_cuckoo(volume)
        time.sleep_ms(200)
        servos.bird_in()
        time.sleep_ms(config.SERVO_MOVE_MS)
        servos.close_door()

    do_sequence()


def trigger_chime_for_current_time(volume=None):
    """
    Chime according to current time: at :00 run full cuckoo (servos + cuckoo);
    at :30 play half-hour chime only (no servos).
    """
    t = time.localtime()
    minute = t[4]
    if minute == 30 and config.CHIME_AT_HALF_HOUR:
        audio.play_chime_half(volume)
    elif minute == 0:
        trigger_cuckoo(volume=volume, manual=False)

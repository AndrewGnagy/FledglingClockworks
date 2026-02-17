# network_ntp.py - WiFi connection and NTP time sync for Pico W

import network
import ntptime
import time

import config


def connect_wifi():
    """Connect to WiFi using config. Blocks until connected or timeout."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return True
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    timeout = 15
    start = time.ticks_ms()
    while not wlan.isconnected() and time.ticks_diff(time.ticks_ms(), start) < timeout * 1000:
        time.sleep_ms(200)
    return wlan.isconnected()


def sync_ntp():
    """Set RTC from NTP. Call after WiFi is connected. May raise on DNS/timeout."""
    ntptime.host = config.NTP_SERVER
    ntptime.settime()


def last_ntp_sync_time():
    """Return last NTP sync time (for periodic re-sync). Simple implementation: track in global."""
    return getattr(sync_ntp, "_last_sync", 0)


def maybe_resync_ntp():
    """Re-sync NTP if interval has elapsed. Call from main loop."""
    interval = config.NTP_SYNC_INTERVAL_S
    if interval <= 0:
        return
    now = time.time()
    last = last_ntp_sync_time()
    if now - last >= interval:
        try:
            sync_ntp()
            sync_ntp._last_sync = now
        except Exception:
            pass

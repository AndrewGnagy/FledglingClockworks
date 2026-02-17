# main.py - Smart Cuckoo Clock (Pico W) entrypoint
# Initializes subsystems, runs main loop (time check + chime, web server).

import socket
import time

import config
import network_ntp
import light_sensor
import servos
import audio
import clock_logic
import web_server


def main():
    # --- Init ---
    light_sensor.init()
    servos.init()
    audio.init()

    if not network_ntp.connect_wifi():
        # Continue without network; RTC may be wrong until NTP available
        pass
    else:
        try:
            network_ntp.sync_ntp()
            network_ntp.sync_ntp._last_sync = time.time()
        except Exception:
            pass

    listen_sock = socket.socket()
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind(("0.0.0.0", 80))
    listen_sock.listen(2)
    listen_sock.setblocking(False)

    # --- Main loop ---
    while True:
        if clock_logic.should_chime_now():
            clock_logic.trigger_chime_for_current_time(volume=web_server.get_volume())

        network_ntp.maybe_resync_ntp()
        web_server.poll(listen_sock, timeout_ms=50)

        time.sleep_ms(1000)  # Check about once per second


if __name__ == "__main__":
    main()

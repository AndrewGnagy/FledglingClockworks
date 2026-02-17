# web_server.py - Minimal HTTP server for phone control (trigger, volume, modes)

import socket
import time

import config
import clock_logic
import light_sensor


# Current volume (0.0..1.0) and mode overrides (e.g. night mode override)
_current_volume = config.DEFAULT_VOLUME
_night_mode_override = None  # None = use sensor; True = force night (no chime); False = force day


def get_volume():
    return _current_volume


def set_volume(v):
    global _current_volume
    _current_volume = max(0.0, min(1.0, float(v)))


def get_night_mode_override():
    return _night_mode_override


def set_night_mode_override(value):
    global _night_mode_override
    _night_mode_override = value  # True, False, or None


def _is_night_mode():
    if _night_mode_override is not None:
        return _night_mode_override
    return light_sensor.is_night_mode()


def _html():
    lux = light_sensor.read_lux()
    return """<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Cuckoo Clock</title></head>
<body>
<h1>Smart Cuckoo Clock</h1>
<p>Light: %.1f lux | Night mode: %s</p>
<p><a href="/trigger">Trigger cuckoo now</a></p>
<form method="post" action="/volume">
Volume: <input type="range" name="v" min="0" max="100" value="%d"/>
<input type="submit" value="Set"/>
</form>
<p>Night mode: <a href="/mode?night=1">Force night</a> | <a href="/mode?night=0">Force day</a> | <a href="/mode?night=auto">Auto</a></p>
</body></html>""" % (
        lux,
        "yes" if _is_night_mode() else "no",
        int(_current_volume * 100),
    )


def _handle_get(path, _headers):
    if path == "/" or path == "/index.html":
        return "200 OK", "text/html", _html()
    if path == "/trigger":
        if not _is_night_mode():
            clock_logic.trigger_cuckoo(volume=_current_volume, manual=True)
        return "302 Found", None, None, "/"
    if path.startswith("/mode?"):
        # Parse ?night=0|1|auto
        q = path.split("?", 1)[-1]
        for part in q.split("&"):
            if part.startswith("night="):
                v = part.split("=", 1)[1]
                if v == "1":
                    set_night_mode_override(True)
                elif v == "0":
                    set_night_mode_override(False)
                else:
                    set_night_mode_override(None)
                break
        return "302 Found", None, None, "/"
    return "404 Not Found", "text/plain", "Not found"


def _handle_post(path, body, _headers):
    if path == "/volume" and body:
        for part in body.split("&"):
            if part.startswith("v="):
                try:
                    set_volume(int(part.split("=", 1)[1]) / 100.0)
                except ValueError:
                    pass
                break
        return "302 Found", None, None, "/"
    return "404 Not Found", "text/plain", "Not found"


def handle_client(cl):
    try:
        data = cl.recv(1024)
        if not data:
            cl.close()
            return
        lines = data.decode("utf-8").split("\r\n")
        req = lines[0].split()
        if len(req) < 2:
            cl.close()
            return
        method, path = req[0], req[1]
        headers = {}
        body_start = 0
        for i, line in enumerate(lines[1:], 1):
            if line == "":
                body_start = i + 1
                break
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()
        body = "\r\n".join(lines[body_start:]) if body_start else ""
        if method == "GET":
            result = _handle_get(path, headers)
        elif method == "POST":
            result = _handle_post(path, body, headers)
        else:
            result = "405 Method Not Allowed", "text/plain", "Method not allowed"
        status = result[0]
        ctype = result[1]
        payload = result[2]
        location = result[3] if len(result) > 3 else None
        if location:
            cl.send("HTTP/1.0 %s\r\nLocation: %s\r\nConnection: close\r\n\r\n" % (status, location))
        else:
            cl.send("HTTP/1.0 %s\r\nContent-Type: %s\r\nConnection: close\r\n\r\n" % (status, ctype or "text/html"))
            if payload:
                cl.send(payload)
    except Exception:
        pass
    try:
        cl.close()
    except Exception:
        pass


def poll(listen_sock, timeout_ms=10):
    """
    Accept one client if any, handle request, then return.
    Call from main loop. listen_sock: socket bound to 0.0.0.0:80.
    """
    try:
        cl, _ = listen_sock.accept()
        handle_client(cl)
    except OSError:
        pass

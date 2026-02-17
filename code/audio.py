# audio.py - I2S audio playback for Waveshare Pico-Audio (WAV/PCM)
# Pico has limited RAM; use short WAV files. See docs/AUDIO_ASSETS_PLAN.md for format.

import machine
import time

import config

_i2s = None


def init():
    """Initialize I2S for Pico-Audio (PCM5101A pins: DIN=26, BCK=27, LRCK=28)."""
    global _i2s
    # MicroPython I2S: typically (id, sck, ws, sd, mode=I2S.TX, bits=16, format=I2S.STEREO, rate=22050, ...)
    # Pico W: sck=BCK, ws=LRCK, sd=DIN
    _i2s = machine.I2S(
        0,
        sck=machine.Pin(config.PIN_I2S_BCK),
        ws=machine.Pin(config.PIN_I2S_LRCK),
        sd=machine.Pin(config.PIN_I2S_DIN),
        mode=machine.I2S.TX,
        bits=16,
        format=machine.I2S.STEREO,
        rate=22050,
        ibuf=2048,
    )


def play_wav(path, volume=None):
    """
    Play a WAV file from the filesystem. Blocks until done or error.
    path: e.g. 'cuckoo.wav'. volume: 0.0..1.0 (optional, from config if not set).
    WAV expected: 16-bit, mono or stereo, 22050 Hz (or 16000) for compatibility.
    """
    global _i2s
    if _i2s is None:
        init()
    vol = config.DEFAULT_VOLUME if volume is None else max(0.0, min(1.0, volume))
    try:
        with open(path, "rb") as f:
            # Skip WAV header (first 44 bytes typical for PCM)
            header = f.read(44)
            if len(header) < 44 or header[:4] != b"RIFF":
                # Not a WAV or short file
                return
            # Read and push chunks to I2S
            chunk = bytearray(512)
            while True:
                n = f.readinto(chunk)
                if n <= 0:
                    break
                if vol < 1.0 and n >= 2:
                    # Simple volume: scale 16-bit samples (stereo: L R L R)
                    for i in range(0, n, 2):
                        if i + 1 < n:
                            s = chunk[i] | (chunk[i + 1] << 8)
                            if s >= 32768:
                                s -= 65536
                            s = int(s * vol)
                            s = max(-32768, min(32767, s))
                            chunk[i] = s & 0xFF
                            chunk[i + 1] = (s >> 8) & 0xFF
                _i2s.write(chunk[:n])
    except OSError:
        pass
    # Allow buffer to drain
    time.sleep_ms(50)


def play_cuckoo(volume=None):
    """Convenience: play the cuckoo WAV from config."""
    play_wav(config.CUCKOO_FILE, volume)


def play_chime_half(volume=None):
    """Convenience: play half-hour chime if file exists."""
    try:
        play_wav(config.CHIME_HALF_FILE, volume)
    except OSError:
        pass


def play_chime_full(volume=None):
    """Convenience: play full-hour chime if file exists."""
    try:
        play_wav(config.CHIME_FULL_FILE, volume)
    except OSError:
        pass

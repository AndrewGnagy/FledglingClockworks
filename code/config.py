# config.py - Central configuration for Smart Cuckoo Clock (Pico W)
# Edit WiFi credentials and pin assignments here; keep in sync with docs/WIRING.md

# --- WiFi ---
WIFI_SSID = "your_ssid"
WIFI_PASSWORD = "your_password"

# --- NTP ---
NTP_SERVER = "pool.ntp.org"
NTP_SYNC_INTERVAL_S = 86400  # Re-sync every 24 hours (0 = sync only at boot)

# --- GPIO (match docs/WIRING.md) ---
# Servos (PWM)
PIN_SERVO_DOOR = 14   # GP14 - door open/close
PIN_SERVO_BIRD = 15   # GP15 - bird in/out

# I2C (BH1750 light sensor)
PIN_I2C_SDA = 16      # GP16
PIN_I2C_SCL = 17      # GP17

# I2S (Waveshare Pico-Audio; initial PCM5101A version)
# Rev2.1 uses DIN=22, MCLK=26, LRCK=27, SCLK=28
PIN_I2S_DIN = 26      # GP26 - data
PIN_I2S_BCK = 27      # GP27 - bit clock
PIN_I2S_LRCK = 28     # GP28 - word clock

# --- Night mode (light sensor) ---
NIGHT_MODE_LUX_THRESHOLD = 10.0  # Below this lux, do not chime (night)

# --- Volume (0.0 .. 1.0; applied in software or hardware if supported) ---
DEFAULT_VOLUME = 0.8

# --- Audio files (on Pico filesystem under / or /assets) ---
# Use WAV for reliable playback; see docs/AUDIO_ASSETS_PLAN.md
CUCKOO_FILE = "cuckoo.wav"
CHIME_HALF_FILE = "chime_half.wav"
CHIME_FULL_FILE = "chime_full.wav"

# --- Servo timing (duty cycle or angle; adjust for your linkage) ---
# Typical MG90S: 1ms=0°, 1.5ms=90°, 2ms=180° at 50Hz (20000 us period)
SERVO_PERIOD_US = 20000
SERVO_DOOR_CLOSED = 1000   # us - door closed
SERVO_DOOR_OPEN = 2000     # us - door open
SERVO_BIRD_IN = 1000       # us - bird inside
SERVO_BIRD_OUT = 2000      # us - bird outside
SERVO_MOVE_MS = 300        # ms to move between positions

# --- Chime schedule ---
CHIME_AT_HALF_HOUR = True   # If True, chime at :00 and :30
# If False, only at :00 (and optionally number of cuckoos = hour)

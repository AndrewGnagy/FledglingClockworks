# 🕒 Smart Cuckoo Clock (Pico W Edition)

A modern, DIY take on the classic Black Forest Cuckoo Clock. This project replaces traditional mechanical bellows and weights with a **Raspberry Pi Pico W**, servos, and high-fidelity digital audio, all housed in a custom **laser-cut** wooden enclosure.

## 🚀 Key Features

* **Phone Control:** Integrated web server for triggering the cuckoo, adjusting volume, and toggling modes via smartphone.
* **Network Time (NTP):** Automatic time synchronization over Wi-Fi—no manual setting or RTC drift.
* **Night Mode:** Intelligent light sensing to prevent chimes in a dark room.
* **Digital Audio:** High-quality MP3 playback for authentic bird calls and chimes.

---

## 🛠 Hardware Components

### Core Logic & Connectivity

* **Raspberry Pi Pico WH:** The brain of the project. Features dual-core ARM Cortex-M0+ and **onboard Wi-Fi** for network connectivity and web hosting. Includes pre-soldered headers for easy wiring.

### Motion & Mechanics

* **MG90S Micro Servos (x2):** High-torque metal gear servos.
* *Servo 1:* Operates the cuckoo door.
* *Servo 2:* Controls the bird's forward/backward movement.


* **Quartz Clock Movement:** A standalone battery-powered unit with a **long shaft** to drive the physical hands through the wooden face.

### Audio & Sensing

* **[Waveshare Pico-Audio Expansion](https://www.waveshare.com/pico-audio.htm):** Provides a dedicated DAC (Digital-to-Analog Converter) and speaker output for crisp audio playback.
* **BH1750 Digital Light Sensor:** An I2C sensor used to measure ambient light levels (Lux) to enable/disable sound during nighttime.
* **8 Ohm 2W Speaker:** Internal speaker for the cuckoo call.

### Power & Structure

* **5V 2A Power Supply:** Dedicated power for the servos to prevent Pico brownouts.
* **Laser-Cut Enclosure:** Custom-designed 3mm/6mm Birch Plywood housing.

---

## 📂 Project Structure

* `/code`: MicroPython scripts for the Pico W.
* `/cad`: SVG/DXF files for the laser-cut enclosure.
* `/assets`: MP3 audio files (cuckoo calls, chimes).
* `/docs`: Wiring diagrams and assembly photos.

---

## 🛠 Tech Stack

* **Language:** MicroPython
* **IDE:** Cursor / VS Code
* **Communication:** I2C (Sensor), PWM (Servos), SPI/I2S (Audio)

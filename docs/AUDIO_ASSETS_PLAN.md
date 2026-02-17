# Audio Assets Plan – Manual Work

This document defines how to select, license, name, and prepare audio files for the Smart Cuckoo Clock so they are ready to use on the Pico (see [README](../README.md) and `/assets`). The firmware may play WAV/PCM for reliability; MP3 can be used as a source format and converted.

---

## Required assets (checklist)

- [ ] **Cuckoo call**
  - One or two notes (“cuck-oo”); loopable or one-shot.
  - Suggested duration: 1–3 seconds.
  - Used when the clock chimes (on the hour and optionally half-hour) and for manual trigger.
- [ ] **Optional: half-hour chime**
  - Short sequence (e.g. single tone or short melody) for :30.
- [ ] **Optional: full-hour chime**
  - Longer sequence or “number of cuckoos” = hour (e.g. 1–12 cuckoos).

Tick off when each file is sourced, licensed, and converted to the target format.

---

## Format and specs (target for Pico)

- **Recommended playback format:** WAV (PCM) for simplicity and low CPU on Pico.
  - Sample rate: 22050 Hz or 16000 Hz (mono).
  - Bit depth: 16-bit.
  - Mono preferred to save space and processing.
- **Max file size:** Keep each asset small enough to fit in Pico flash with the rest of the project (e.g. on the order of tens to low hundreds of KB per file).
- **If using MP3 on device:** Specify bit rate (e.g. 64–128 kbps) and max duration; ensure a decoder is available in the firmware (see plan: may require WAV if no decoder).

---

## Sourcing options

- **Royalty-free / CC libraries**
  - Freesound.org (filter by CC0, CC-BY; check attribution).
  - BBC Sound Effects (check license for your use).
  - Other “sound effects” or “nature / bird” packs that allow personal/diy use.
- **Record your own**
  - Use a quiet room; consistent level; trim silence at start/end.
- **Commission or buy**
  - Single license for “cuckoo” and “chime” if you need a specific character or quality.

Document the source URL or “self-recorded” and the license for each file (see Licensing below).

---

## Licensing

- For each asset, record:
  - **File name** (in repo)
  - **Source** (URL or “self-recorded”)
  - **License** (e.g. CC0, CC-BY, “Commercial license – [vendor]”)
  - **Attribution** (if required, e.g. “Sound by [author] from Freesound” and add to main README).
- **Where to store:** Either a table in this doc or a small file per asset in `assets/licenses/` (e.g. `assets/licenses/cuckoo.txt` with license + source).

Example table (fill in when you add files):

| Asset       | Source        | License | Attribution |
|------------|---------------|---------|-------------|
| cuckoo.wav | (to be added) |         |             |
| chime_*.wav| (to be added) |         |             |

---

## Naming and placement

- **Suggested names:**
  - `assets/cuckoo.wav` – main cuckoo call.
  - `assets/chime_half.wav` – half-hour chime (optional).
  - `assets/chime_full.wav` – full-hour chime or melody (optional).
- Keep names short and consistent with what [code/config.py](../code/config.py) or the audio module expects (e.g. `config.CUCKOO_FILE = "cuckoo.wav"`).
- See main [README](../README.md) for the `/assets` folder in the project structure.

---

## Post-processing

- **Normalize volume** so levels are similar across assets (e.g. -3 dB peak or similar).
- **Trim silence** at start and end to reduce file size and latency.
- **Convert to target format** (e.g. MP3 → WAV, resample to 22050 Hz or 16000 Hz, mono, 16-bit).

Example with `ffmpeg` (run from repo root or `assets/`):

```bash
# Example: convert and resample to 22050 Hz mono 16-bit WAV
ffmpeg -i source_cuckoo.mp3 -ar 22050 -ac 1 -acodec pcm_s16le -y cuckoo.wav

# Normalize (optional; normalize filter or use sox/audacity)
ffmpeg -i cuckoo.wav -af loudnorm=I=-16:LRA=11:TP=-1.5 -ar 22050 -ac 1 -y cuckoo_normalized.wav
```

Add your own one-liners or a small script here as you standardize your workflow.

---

## References

- Main project and `/assets`: [README](../README.md).
- Software that plays these files: `code/audio.py` and plan section on audio format (WAV vs MP3).

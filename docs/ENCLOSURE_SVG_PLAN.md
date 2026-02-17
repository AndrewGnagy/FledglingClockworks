# Enclosure SVG/CAD Plan – Manual Work

This document is a checklist and specification for designing and exporting the laser-cut wooden enclosure for the Smart Cuckoo Clock. Use it when doing the manual CAD work so panels and exports stay consistent. See the main [README](../README.md) for project overview and the `/cad` folder in the repo structure.

---

## Design goals

- **Material:** 3 mm and 6 mm birch plywood (as in README).
- **Contents:** Housing for Pico W, Waveshare Pico-Audio, two MG90S servos, BH1750, 8 Ω speaker, and quartz clock movement.
- **Mechanics:** Cuckoo door and bird mechanism must align with the two servos (door servo, bird servo).
- **Output:** Files suitable for laser cutting (SVG and/or DXF), with clear cut vs. engrave layers.

---

## Panels to create (checklist)

Use this list when designing; tick off as each part is done.

- [ ] **Face (clock face)**
  - Hole for quartz movement long shaft (exact diameter from your movement).
  - Cutout for cuckoo door and bird (size and position to match servo travel and door part).
  - Numeral markings or cutouts (e.g. 12, 3, 6, 9 or full dial).
  - Material: 3 mm or 6 mm as chosen.
- [ ] **Door (cuckoo door)**
  - Small door that one servo opens/closes; dimensions and pivot to match linkage and face cutout.
  - Material: 3 mm (typical).
- [ ] **Left side**
  - Height/depth to fit Pico stack, servos, speaker; optional ventilation or cable holes.
- [ ] **Right side**
  - Mirror of left or symmetric design.
- [ ] **Top**
  - Optional vents; optional access for USB.
- [ ] **Bottom**
  - Optional feet or vents; stability.
- [ ] **Back**
  - Access for USB/power; optional ventilation; optional battery door if quartz uses internal battery.
- [ ] **Internal parts**
  - Mounts or shelves for Pico (+ Pico-Audio), speaker, and optionally battery holder for quartz movement.
- [ ] **Optional**
  - Speaker grille (cut or engrave).
  - Cable-routing cutouts.

---

## Naming and versioning

- **Suggested pattern:** `cad/<panel>_<thickness>_v<n>.<ext>`
  - Examples: `face_3mm_v1.svg`, `door_3mm_v1.svg`, `side_left_6mm_v1.svg`.
- **DXF:** Either same folder with `.dxf` extension or a subfolder, e.g. `cad/dxf/` with the same base names.
- Bump version (e.g. `v1` → `v2`) when you change geometry so laser shop or you can track which file set was used for a cut.

---

## Export for laser

- **Format:** SVG or DXF, per your laser cutter or service.
- **Cut paths:** Use single strokes (outline-only) for cuts; no fill-only shapes for through-cuts. Typical: stroke width 0.1 mm or “hairline” and “cut” layer.
- **Engrave:** If you have engrave layers (e.g. numerals), put them on a separate layer and name it clearly (e.g. “engrave”).
- **Material:** Tag each file or layer with thickness (3 mm vs 6 mm) so the right power/speed is used.
- **Kerf:** If the workshop expects kerf compensation (e.g. 0.1 mm), document it in the file name or a `cad/README.txt` (e.g. “kerf 0.1 mm”) so they can compensate if needed.

---

## Critical dimensions to decide

Before finalizing SVGs, fix these and note them in this doc or in `cad/dimensions.txt`:

| Item | What to define |
|------|----------------|
| Quartz shaft | Hole diameter (and depth if recessed). |
| Door | Width × height; pivot position and arm length to match servo horn. |
| Face cutout | Opening for door + bird; position relative to shaft center. |
| Pico W + Pico-Audio | Footprint and height; internal clearance for stack. |
| Speaker | Diameter and depth; grille area if used. |
| BH1750 | Placement and any window/hole for light. |
| Servos | Mounting centers and arm travel; link to door and bird. |

---

## References

- Main project structure and “Laser-Cut Enclosure”: [README](../README.md).
- Wiring and placement of electronics: [WIRING.md](WIRING.md).
- Repo folder for all CAD files: `/cad` (and optionally `/cad/dxf`).

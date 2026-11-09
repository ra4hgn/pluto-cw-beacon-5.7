# CW Beacon on 5.7 GHz (RA4HGN)

A Morse-code (CW) beacon for the
[ADALM-PlutoSDR](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html).
It transmits a repeating `CQ CQ DE BEACON` message in the 6 cm amateur band
(around 5760 MHz).

The project ships **two implementations** of the same beacon:

| Version | Where it runs | Use it when |
|---|---|---|
| **GNU Radio** (`gnuradio/`) | on a host PC, streams I/Q to the Pluto | you want a GUI, live controls, easy tweaking |
| **On-target C** (`on-target/`) | directly on the Pluto's ARM CPU (autonomous) | you want a standalone beacon with no PC |

## Screenshots

| Flowgraph (GNU Radio) | GUI window |
|---|---|
| ![flowgraph](images/flowgraph.png) | ![window](images/window-v2.png) |

## Version 1 — GNU Radio (`gnuradio/`)

- Complex 800 Hz tone → signal at **LO + 800 Hz**.
- Live Qt GUI: LO frequency (5760–5762 MHz, 10 kHz step), tone (300–3000 Hz),
  speed (5–60 WPM), TX attenuation (0–60 dB).
- Baseband sample rate 1 MHz, streamed to the Pluto over USB.

Requirements: GNU Radio 3.10+ with `gr-iio`, Python 3, NumPy, PyQt5.

```bash
cd gnuradio
grcc microwave_morse_beacon.grc      # optional: regenerate the .py
python3 microwave_morse_beacon.py    # or open the .grc in GNU Radio Companion
```

The transmitted text is defined in
`gnuradio/microwave_morse_beacon_epy_block_0.py` (`self.message`).

## Version 2 — On-target C (`on-target/`)

Autonomous beacon that runs on the Pluto itself, using the FPGA's built-in
DDS tone generator (no I/Q streaming). Build, upload and run instructions are
in [`on-target/README.md`](on-target/README.md).

The transmitted text is defined in `on-target/beacon.c` (`#define MSG`).

## License

[GPL-3.0](LICENSE).

## Author

RA4HGN

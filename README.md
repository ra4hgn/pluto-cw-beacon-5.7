# CW Beacon on 5.7 GHz (RA4HGN)

A Morse-code (CW) beacon transmitter for the
[ADALM-PlutoSDR](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html),
built with [GNU Radio](https://www.gnuradio.org/). It transmits in the 6 cm
amateur band (around 5760 MHz).

## Features

- Repeating Morse message `CQ CQ DE BEACON` (hardcoded, editable).
- Single-sideband keying: a complex 800 Hz tone, so the signal appears at
  **LO + tone** (e.g. 5760.1 MHz + 800 Hz) during key-down.
- Live Qt GUI controls:
  | Control | Range | Default |
  |---|---|---|
  | LO Frequency | 5760–5762 MHz (10 kHz step) | 5760.1 MHz |
  | Tone | 300–3000 Hz | 800 Hz |
  | Speed (WPM) | 5–60 | 20 |
  | TX Attenuation | 0–60 dB | 10 dB |
- Baseband sample rate: 1 MHz.

## Requirements

- GNU Radio 3.10+ with `gr-iio` (PlutoSDR support)
- ADALM-PlutoSDR
- Python 3, NumPy, PyQt5

## Usage

1. Connect the PlutoSDR over USB.
2. Open `microvawe_morse_beacon.grc` in GNU Radio Companion and press **Run**
   (F6).

The device is auto-detected via IIO (`iio.get_pluto_uri()`).

The Python script is generated from the flowgraph; regenerate and run it with:

```bash
grcc microvawe_morse_beacon.grc
python3 microvawe_morse_beacon.py
```

## How it works

```
Morse envelope (float, 1 MHz) ──► float_to_complex ─┐
                                                     ├─► multiply ──► PlutoSDR Sink (LO)
800 Hz tone (complex, 1 MHz) ───────────────────────┘
```

The embedded Python block (`microvawe_morse_beacon_epy_block_0.py`) builds a
float keying envelope (0/1) from a Morse dictionary, then it is up-converted
to a complex 800 Hz tone and sent to the PlutoSDR.

## Customising the message

The beacon text is defined in `microvawe_morse_beacon_epy_block_0.py`:

```python
self.message = "CQ CQ DE BEACON"
```

Change it and the flowgraph will transmit the new message (letters A–Z and
spaces are supported).

## License

[GPL-3.0](LICENSE) — see the LICENSE file.

## Author

RA4HGN

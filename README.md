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

## Frequency range: extending the AD9363 to 6 GHz

The ADALM-Pluto uses the **AD9363**, officially limited to **325 MHz – 3.8 GHz**
— below the beacon's **5760.100 MHz**. That 3.8 GHz cap is a **firmware**
limit (the device-tree `compatible` string), not a silicon limit: the AD9363 RF
front-end actually reaches **6 GHz**.

The range is extended via the U-Boot environment — connect over SSH and run:

```bash
ssh root@192.168.2.1

# 1. Tell the driver the chip is an AD9364 (opens 70 MHz – 6 GHz)
fw_setenv attr_name compatible
fw_setenv attr_val ad9364

# 2. Enable the second CPU core of the Zynq (faster)
fw_setenv maxcpus

# 3. Reboot to apply
reboot
```

After the reboot, `iio_info` reports an AD9364 model and exposes the full
6 GHz range:

```bash
iio_info -a | grep -E 'hw_model|frequency_available'
```

```
hw_model: Analog Devices PlutoSDR Rev.B (Z7010-AD9364)
altvoltage1: TX_LO  frequency_available: [46875001 1 6000000000]
altvoltage0: RX_LO  frequency_available: [70000000 1 6000000000]
```

This project was developed on an **AD9363** unit with this 6 GHz extension
applied — that is why the beacon transmits on 5760.100 MHz.

## License

[GPL-3.0](LICENSE).

## Author

RA4HGN

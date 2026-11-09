# On-target CW Beacon (C + libiio, DDS)

Standalone C implementation of the CW beacon that runs **directly on the
ADALM-PlutoSDR** (AD9363 + Zynq-7010) — no host PC required.

It uses the Pluto's **built-in DDS tone generator**: the FPGA produces the
800 Hz tone, and the program only keys it on/off with the Morse timing.

## Prerequisites (on the PC)

- ARM cross-compiler, libiio headers, cmake, git:

  ```bash
  sudo apt install gcc-arm-linux-gnueabihf libiio-dev cmake git
  ```

- Pluto connected over USB (SSH `192.168.2.1`, user `root`, password `analog`).

## Build

1. Build a **static** libiio for ARM (local backend only):

   ```bash
   git clone --branch v0.25 --depth 1 https://github.com/analogdevicesinc/libiio.git ~/libiio
   cd ~/libiio && mkdir -p build && cd build
   cmake .. -DCMAKE_C_COMPILER=arm-linux-gnueabihf-gcc \
       -DCMAKE_SYSTEM_NAME=Linux -DCMAKE_SYSTEM_PROCESSOR=arm \
       -DBUILD_SHARED_LIBS=OFF -DWITH_LOCAL_BACKEND=ON \
       -DWITH_XML_BACKEND=OFF -DWITH_NETWORK_BACKEND=OFF \
       -DWITH_USB_BACKEND=OFF -DWITH_SERIAL_BACKEND=OFF \
       -DWITH_IIOD=OFF -DNO_THREADS=ON \
       -DWITH_TESTS=OFF -DWITH_DOC=OFF -DWITH_EXAMPLES=OFF -DWITH_MAN=OFF
   make
   ```

2. Cross-compile the beacon (statically linked against that libiio):

   ```bash
   cd on-target
   make
   ```

3. Upload to the Pluto (persistent `/mnt/jffs2`) and run:

   ```bash
   make upload
   make run
   ```

Stop with `Ctrl+C`. See *Autostart on power-up* below to start it on every boot.

## Autostart on power-up

The Pluto's root filesystem (`/`, `/etc`, `/root`) is a **RAM filesystem**
(rootfs/ramfs) — changes there are lost on reboot. The only persistent
writable location is **`/mnt/jffs2`** (JFFS2 on the QSPI flash).

The stock firmware already provides a persistent autostart hook:
`/etc/init.d/S98autostart` runs `/mnt/jffs2/autorun.sh` at boot if it exists.

So to start the beacon automatically on every power-up:

1. Upload the binary to the persistent partition:

   ```bash
   scp -O beacon root@192.168.2.1:/mnt/jffs2/beacon
   ```

2. On the Pluto (`ssh root@192.168.2.1`) create `/mnt/jffs2/autorun.sh`:

   ```sh
   chmod +x /mnt/jffs2/beacon
   cat > /mnt/jffs2/autorun.sh << 'EOF'
   #!/bin/sh
   nohup /mnt/jffs2/beacon >/dev/null 2>&1 &
   EOF
   chmod +x /mnt/jffs2/autorun.sh
   ```

3. Reboot and verify:

   ```sh
   reboot
   # after it boots:
   ps | grep beacon
   ```

No firmware rebuild is needed — `/mnt/jffs2` survives power cycles.

## Configuration

`#define` constants at the top of `beacon.c`:

| Constant | Meaning | Default |
|---|---|---|
| `LO_FREQ` | TX carrier | 5760100000 (5760.100 MHz) |
| `TONE_FREQ` | keying tone (Hz) | 800 |
| `WPM` | keying speed | 20 |
| `TX_ATTEN` | TX attenuation (dB) | 10 |
| `TONE_SCALE` | DDS amplitude (0..1) | 0.6 |
| `MSG` | message text | `CQ CQ DE BEACON` |

## Troubleshooting

- **`sftp-server: not found` / `scp: Connection closed`**: the Pluto runs
  Dropbear SSH (no SFTP). Use `scp -O` for both directions, or pipe over SSH
  with `cat`.

- **Device / channel names**: verify with `iio_info -a`; adjust
  `ad9361-phy`, `cf-ad9361-dds-core-lpc`, `altvoltage0`/`altvoltage2` (I/Q
  tone), `altvoltage1` (LO) in `beacon.c` if needed.

- **No keying / continuous tone**: DDS keying uses the `raw` attribute; if
  your firmware differs, try toggling `scale` instead.

- **"not found" after reboot**: the binary was in RAM — re-upload it.

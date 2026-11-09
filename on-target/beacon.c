/*
 * CW Beacon on 5.7 GHz (RA4HGN) — standalone on ADALM-PlutoSDR
 * =====================================================================
 * DDS tone-generator version: the FPGA generates the 800 Hz tone directly,
 * and the code only keys it on/off (no I/Q streaming, no sample-rate
 * juggling). Runs on the Pluto's ARM CPU.
 *
 * Build (cross-compile for ARM, static libiio):
 *     arm-linux-gnueabihf-gcc -static -O2 -o beacon beacon.c \
 *         -I$HOME/libiio -I$HOME/libiio/build -L$HOME/libiio/build -liio -lm
 */

#include <errno.h>
#include <iio.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define LO_FREQ     5760100000ULL  /* TX LO, 5760.100 MHz */
#define TONE_FREQ   800            /* keying tone, Hz     */
#define WPM         20             /* keying speed        */
#define TX_ATTEN    10.0           /* TX attenuation, dB  */
#define TONE_SCALE  0.6            /* DDS amplitude 0..1  */

#define MSG         "CQ CQ DE BEACON"

static const char *const morse[26] = {
    ".-",    "-...",  "-.-.",  "-..",   ".",     "..-.",  /* A-F */
    "--.",   "....",  "..",    ".---",  "-.-",   ".-..",  /* G-L */
    "--",    "-.",    "---",   ".--.",  "--.-",  ".-.",   /* M-R */
    "...",   "-",     "..-",   "...-",  ".--",   "-..-",  /* S-X */
    "-.--",  "--.."                                        /* Y-Z */
};

static struct iio_context *ctx = NULL;

static void cleanup(void)
{
    if (ctx) { iio_context_destroy(ctx); ctx = NULL; }
}

static void on_signal(int sig)
{
    (void)sig;
    cleanup();
    exit(0);
}

static void key(struct iio_channel *i, struct iio_channel *q, int on)
{
    iio_channel_attr_write_longlong(i, "raw", on ? 1 : 0);
    iio_channel_attr_write_longlong(q, "raw", on ? 1 : 0);
}

int main(void)
{
    signal(SIGINT,  on_signal);
    signal(SIGTERM, on_signal);
    setvbuf(stdout, NULL, _IONBF, 0);

    int dot_us = 1200000 / WPM;   /* dot = 60 ms */

    ctx = iio_create_default_context();
    if (!ctx) { fprintf(stderr, "no IIO context\n"); return 1; }

    struct iio_device *phy = iio_context_find_device(ctx, "ad9361-phy");
    struct iio_device *dds = iio_context_find_device(ctx, "cf-ad9361-dds-core-lpc");
    if (!dds) dds = iio_context_find_device(ctx, "cf-ad9361-lpc");
    if (!phy || !dds) { fprintf(stderr, "devices not found\n"); cleanup(); return 1; }

    struct iio_channel *tx_lo   = iio_device_find_channel(phy, "altvoltage1", true);
    struct iio_channel *phy_out = iio_device_find_channel(phy, "voltage0", true);
    struct iio_channel *dds_i   = iio_device_find_channel(dds, "altvoltage0", true); /* TX1_I_F1 */
    struct iio_channel *dds_q   = iio_device_find_channel(dds, "altvoltage2", true); /* TX1_Q_F1 */
    if (!tx_lo || !phy_out || !dds_i || !dds_q) {
        fprintf(stderr, "channels not found\n");
        cleanup();
        return 1;
    }

    /* configure: tone frequency, amplitude, LO, attenuation */
    iio_channel_attr_write_longlong(dds_i, "frequency", TONE_FREQ);
    iio_channel_attr_write_longlong(dds_q, "frequency", TONE_FREQ);
    iio_channel_attr_write_double(dds_i, "scale", TONE_SCALE);
    iio_channel_attr_write_double(dds_q, "scale", TONE_SCALE);
    key(dds_i, dds_q, 0);   /* start keyed off */
    iio_channel_attr_write_double(phy_out, "hardwaregain", -TX_ATTEN);
    iio_channel_attr_write_longlong(tx_lo, "frequency", LO_FREQ);

    printf("CW beacon (DDS): LO=%.3f MHz, %d WPM, %d Hz tone\n",
           LO_FREQ / 1e6, WPM, TONE_FREQ);

    /* keying loop: repeat the message forever */
    for (;;) {
        for (const char *p = MSG; *p; p++) {
            char ch = *p;
            if (ch == ' ') {
                usleep(4 * dot_us);   /* word gap (7 units total) */
                continue;
            }
            if (ch >= 'a' && ch <= 'z') ch -= 'a' - 'A';
            if (ch < 'A' || ch > 'Z') continue;
            const char *code = morse[ch - 'A'];
            for (const char *s = code; *s; s++) {
                int mark_us = (*s == '.') ? dot_us : 3 * dot_us;
                key(dds_i, dds_q, 1);
                usleep(mark_us);
                key(dds_i, dds_q, 0);
                usleep(dot_us);       /* inter-symbol */
            }
            usleep(2 * dot_us);       /* inter-letter */
        }
    }
}

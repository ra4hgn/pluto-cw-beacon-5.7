#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CW Beacon on 5.7 GHz (RA4HGN)
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import iio
import microvawe_morse_beacon_epy_block_0 as epy_block_0  # embedded python block
import threading
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class microvawe_morse_beacon(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "CW Beacon on 5.7 GHz (RA4HGN)", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("CW Beacon on 5.7 GHz (RA4HGN)")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "microvawe_morse_beacon")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.wpm = wpm = 20
        self.tx_freq = tx_freq = 5760.1
        self.tx_atten = tx_atten = 10
        self.tone_freq = tone_freq = 800
        self.samp_rate = samp_rate = 1000000

        ##################################################
        # Blocks
        ##################################################

        self._wpm_range = qtgui.Range(5, 60, 1, 20, 200)
        self._wpm_win = qtgui.RangeWidget(self._wpm_range, self.set_wpm, "Speed (WPM)", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._wpm_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_freq_range = qtgui.Range(5760, 5762, 0.01, 5760.1, 200)
        self._tx_freq_win = qtgui.RangeWidget(self._tx_freq_range, self.set_tx_freq, "LO Frequency (MHz)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tx_freq_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_atten_range = qtgui.Range(0, 60, 0.5, 10, 200)
        self._tx_atten_win = qtgui.RangeWidget(self._tx_atten_range, self.set_tx_atten, "TX Attenuation (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tx_atten_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tone_freq_range = qtgui.Range(300, 3000, 50, 800, 200)
        self._tone_freq_win = qtgui.RangeWidget(self._tone_freq_range, self.set_tone_freq, "Tone (Hz)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tone_freq_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('' if '' else iio.get_pluto_uri(), [True, True], 0x8000, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(2000000)
        self.iio_pluto_sink_0.set_frequency((round(tx_freq * 1e6)))
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, tx_atten)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.epy_block_0 = epy_block_0.blk(wpm=wpm)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, tone_freq, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_float_to_complex_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "microvawe_morse_beacon")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_wpm(self):
        return self.wpm

    def set_wpm(self, wpm):
        self.wpm = wpm
        self.epy_block_0.wpm = self.wpm

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.iio_pluto_sink_0.set_frequency((round(self.tx_freq * 1e6)))

    def get_tx_atten(self):
        return self.tx_atten

    def set_tx_atten(self, tx_atten):
        self.tx_atten = tx_atten
        self.iio_pluto_sink_0.set_attenuation(0,self.tx_atten)

    def get_tone_freq(self):
        return self.tone_freq

    def set_tone_freq(self, tone_freq):
        self.tone_freq = tone_freq
        self.analog_sig_source_x_0.set_frequency(self.tone_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)




def main(top_block_cls=microvawe_morse_beacon, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()

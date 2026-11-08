"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, wpm=20):
        gr.sync_block.__init__(
            self,
            name='Morse Beacon',
            in_sig=None,
            out_sig=[np.float32]
        )
        self.message = "CQ CQ DE BEACON"
        self.samp_rate = 1e6
        self.morse = {
            'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.',
            'G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..',
            'M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.',
            'S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-',
            'Y':'-.--','Z':'--..',' ':' '
        }
        self._wpm = wpm
        self._regenerate()

    @property
    def wpm(self):
        return self._wpm

    @wpm.setter
    def wpm(self, value):
        self._wpm = value
        self._regenerate()

    def _regenerate(self):
        self.dot_samples = int(self.samp_rate * 1.2 / self._wpm)
        self.samples = self._generate()
        self.pos = 0

    def _generate(self):
        out = []
        for ch in self.message.upper():
            if ch == ' ':
                out.extend([0.0] * self.dot_samples * 7)
                continue
            code = self.morse.get(ch, '')
            for sym in code:
                if sym == '.':
                    out.extend([1.0] * self.dot_samples)
                elif sym == '-':
                    out.extend([1.0] * self.dot_samples * 3)
                out.extend([0.0] * self.dot_samples)
            out.extend([0.0] * self.dot_samples * 2)
        return np.array(out, dtype=np.float32)

    def work(self, input_items, output_items):
        out = output_items[0]
        n = len(out)
        end = self.pos + n
        if end <= len(self.samples):
            out[:] = self.samples[self.pos:end]
        else:
            wrap = len(self.samples) - self.pos
            out[:wrap] = self.samples[self.pos:]
            out[wrap:] = self.samples[:(n - wrap)]
        self.pos = end % len(self.samples)
        return n

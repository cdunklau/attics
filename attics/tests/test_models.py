from __future__ import absolute_import

import unittest

from attics.models import Color

NORM_GREEN_HSL = 0.333333, 1, 0.5
NORM_GREEN_RGB = 0, 1, 0
HEX_GREEN = '#00FF00'


class ColorTestCase(unittest.TestCase):
    def test_repr(self):
        output = '<Color %s>' % HEX_GREEN
        assert repr(Color(hsl=NORM_GREEN_HSL)) == output
        assert repr(Color(rgb=NORM_GREEN_RGB)) == output

    def test_repr_alpha(self):
        alpha = 0.8
        output = '<Color rgba(0, 255, 0, 0.8)>'
        assert repr(Color(hsl=NORM_GREEN_HSL, alpha=alpha)) == output
        assert repr(Color(rgb=NORM_GREEN_RGB, alpha=alpha)) == output

    def test_str(self):
        assert str(Color(hsl=NORM_GREEN_HSL)) == HEX_GREEN
        assert str(Color(rgb=NORM_GREEN_RGB)) == HEX_GREEN

    def test_str_alpha(self):
        alpha = 0.8
        color = Color(rgb=NORM_GREEN_RGB, alpha=alpha)
        assert str(color) == 'rgba(0, 255, 0, 0.8)'

    def test_alpha_clipping_high(self):
        color = Color(rgb=(1, 1, 1), alpha=1.1)
        assert color.alpha == 1.0

    def test_alpha_clipping_low(self):
        color = Color(rgb=(1, 1, 1), alpha=-0.1)
        assert color.alpha == 0

    def test_hsl_clipping_high(self):
        color = Color(hsl=(1, 1.1, 1.1))
        assert color.hue == 0
        assert color.saturation == 1
        assert color.lightness == 1

    def test_hsl_clipping_low(self):
        color = Color(hsl=(2, -1, -1))
        assert color.hue == 0
        assert color.saturation == 0
        assert color.lightness == 0

    def test_clipping_degrees_wrap(self):
        color = Color(hsl=(1.5, 1, 1))
        assert color.hue == 0.5
        color = Color(hsl=(-0.1, 1, 1))
        assert color.hue == 0.9

    def test_rgb_clipping_high(self):
        color = Color(rgb=(1.1, 1.1, 1.1))
        assert color.red == 1.0
        assert color.green == 1.0
        assert color.blue == 1.0

    def test_clipping_low(self):
        color = Color(rgb=(-0.1, -0.1, -0.1))
        assert color.red == 0
        assert color.green == 0
        assert color.blue == 0

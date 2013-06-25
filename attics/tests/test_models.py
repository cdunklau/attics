from __future__ import absolute_import

import unittest

from attics.models import Color


class ColorTestCase(unittest.TestCase):
    def test_repr(self):
        hsl = 0.333333, 1, 0.5
        rgb = 0, 1, 0
        output = '<Color rgb(%s%%, %s%%, %s%%)>' % (0, 100, 0)  # blue!
        assert repr(Color(hsl=hsl)) == output
        assert repr(Color(rgb=rgb)) == output

    def test_repr_alpha(self):
        hsl = 0.33333, 1, 0.5
        rgb = 0, 1, 0
        alpha = 0.8
        output = '<Color rgba(%s%%, %s%%, %s%%, %s)>' % (0, 100, 0, 0.8)
        assert repr(Color(hsl=hsl, alpha=alpha)) == output
        assert repr(Color(rgb=rgb, alpha=alpha)) == output

    def test_str(self):
        rgb = 0, 1, 0
        assert str(Color(rgb=rgb)) == 'rgb(0%, 100%, 0%)'

    def test_str_alpha(self):
        rgb = 0, 1, 0
        alpha = 0.8
        assert str(Color(rgb=rgb, alpha=alpha)) == 'rgba(0%, 100%, 0%, 0.8)'

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

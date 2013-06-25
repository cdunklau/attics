from __future__ import absolute_import

import unittest

from attics.models import Color, Length


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

    def test_hsl_clipping_high(self):
        color = Color(hsl=(1, 1.1, 1.1), alpha=1.1)
        assert color.hue == 0
        assert color.saturation == 1
        assert color.lightness == 1
        assert color.alpha == 1

    def test_clipping_low(self):
        color = HSLColor(720, -1, -1, -0.1)
        assert color.hue == '0'
        assert color.saturation == '0%'
        assert color.lightness == '0%'
        assert color.alpha == '0'

    def test_clipping_degrees_wrap(self):
        color = HSLColor(540, 100, 100)
        assert color.hue == '180'
        color = HSLColor(-1, 100, 100)
        assert color.hue == '359'


class RGBColorTestCase(unittest.TestCase):
    def test_str_function(self):
        color = RGBColor(255, 255, 255, preferhex=False)
        assert str(color) == 'rgb(255, 255, 255)'

    def test_str_function_alpha(self):
        color = RGBColor(255, 255, 255, 0.8, preferhex=False)
        assert str(color) == 'rgba(255, 255, 255, 0.8)'

    def test_str_function_alpha_even_with_preferhex(self):
        color = RGBColor(255, 255, 255, 0.8, preferhex=True)
        assert str(color) == 'rgba(255, 255, 255, 0.8)'

    def test_str_hex_3char(self):
        color = RGBColor(0xFF, 0xFF, 0xFF, preferhex=True)
        assert str(color) == '#FFF'
        color = RGBColor(0x00, 0x00, 0x00, preferhex=True)
        assert str(color) == '#000'
        color = RGBColor(0xAA, 0x00, 0x33, preferhex=True)
        assert str(color) == '#A03'

    def test_str_hex_6char(self):
        color = RGBColor(0xFA, 0xFA, 0xFA, preferhex=True)
        assert str(color) == '#FAFAFA'

    def test_clipping_high(self):
        color = RGBColor(256, 256, 256, 1.1, preferhex=False)
        assert color.red == '255'
        assert color.green == '255'
        assert color.blue == '255'
        assert color.alpha == '1'

    def test_clipping_low(self):
        color = RGBColor(-1, -1, -1, -0.1, preferhex=False)
        assert color.red == '0'
        assert color.green == '0'
        assert color.blue == '0'
        assert color.alpha == '0'


class RGBPercentageColorTestCase(unittest.TestCase):
    def test_repr(self):
        color = RGBPercentageColor(100, 100, 100)
        output = '<RGBPercentageColor(red=100%, green=100%, blue=100%)>'
        assert repr(color) == output

    def test_repr_alpha(self):
        color = RGBPercentageColor(100, 100, 100, 0.8)
        output = ('<RGBPercentageColor(red=100%, green=100%, '
                  'blue=100%, alpha=0.8)>')
        assert repr(color) == output

    def test_str(self):
        color = RGBPercentageColor(100, 100, 100)
        assert str(color) == 'rgb(100%, 100%, 100%)'

    def test_str_alpha(self):
        color = RGBPercentageColor(100, 100, 100, 0.8)
        assert str(color) == 'rgba(100%, 100%, 100%, 0.8)'
        color = RGBPercentageColor(100, 100, 100, 0.8)
        assert str(color) == 'rgba(100%, 100%, 100%, 0.8)'

    def test_clipping_high(self):
        color = RGBPercentageColor(101, 101, 101, 1.1)
        assert color.red == '100%'
        assert color.green == '100%'
        assert color.blue == '100%'
        assert color.alpha == '1'

    def test_clipping_low(self):
        color = RGBPercentageColor(-1, -1, -1, -0.1)
        assert color.red == '0%'
        assert color.green == '0%'
        assert color.blue == '0%'
        assert color.alpha == '0'

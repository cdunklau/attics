from __future__ import division

from math import fmod
from colorsys import hls_to_rgb as _hls_to_rgb, rgb_to_hls as _rgb_to_hls


class Color(object):
    """
    An abstract representation of a CSS color value.

    Methods assume instances are not mutated, create a new instance
    instead!

    """
    def __init__(self, rgb=None, hsl=None, alpha=None):
        """
        Inputs must be normalized from the native CSS formats to the
        inclusive range 0.0-1.0. Inputs outside this range will be
        clipped to the edge of the range, except for hue, which will
        be wrapped around.

        Exactly one of ``rgb`` and ``hsl`` must be specified, they
        are mutually exclusive.

        :param rgb: Iterable of three floats between 0.0 and 1.0:
                    red, green, and blue amounts.
        :param hsl: Iterable of three floats between 0.0 and 1.0:
                    hue, saturation, and lightness.
        :param alpha: Alpha value between 0.0 and 1.0.
        """
        if (rgb is None) == (hsl is None):
            raise TypeError("Must specify exactly one of 'rgb', 'hsl'")
        if rgb:
            red, green, blue = [_clip_to_range(c, 0.0, 1.0) for c in rgb]
            hue, lightness, saturation = _rgb_to_hls(red, green, blue)
        elif hsl:
            hue, saturation, lightness = (
                fmod(fmod(hsl[0], 1.0) + 1.0, 1.0),
                _clip_to_range(hsl[1], 0.0, 1.0),
                _clip_to_range(hsl[2], 0.0, 1.0),
            )
            red, green, blue = _hls_to_rgb(hue, lightness, saturation)
        self.red, self.green, self.blue = red, green, blue
        self.hue, self.saturation, self.lightness = hue, saturation, lightness

        self.alpha = 1.0 if alpha is None else _clip_to_range(alpha, 0.0, 1.0)

    @classmethod
    def from_rgb_integer_strings(cls, red, green, blue, alpha='1.0'):
        """
        Return a new ``Color`` instance populated from string
        integers. If provided, ``alpha`` is a float integer.

        """
        rgb = (
            _norm_byte_integer(red),
            _norm_byte_integer(green),
            _norm_byte_integer(blue),
        )
        alpha = float(alpha)
        return cls(rgb=rgb, alpha=alpha)

    @classmethod
    def from_rgb_percent_strings(cls, red, green, blue, alpha='1.0'):
        """
        Return a new ``Color`` instance populated from string
        percentages (float strings ending in '%'). If provided,
        ``alpha`` is a float integer.

        """
        rgb = _norm_percent(red), _norm_percent(green), _norm_percent(blue)
        alpha = float(alpha)
        return cls(rgb=rgb, alpha=alpha)

    @classmethod
    def from_hsl_strings(cls, hue, saturation, lightness, alpha='1.0'):
        """
        Return a new ``Color`` instance populated from strings.
        Percentages are float strings ending in '%'.

        :param hue: The hue value as a string float in degrees
        :param saturation: The saturation value as a percentage
        :param lightness: The lightness value as a percentage

        """
        hsl = (
            _norm_degrees(hue),
            _norm_percent(saturation),
            _norm_percent(lightness),
        )
        alpha = float(alpha)
        return cls(hsl=hsl, alpha=alpha)

    def __unicode__(self):
        rgb = (
            _denorm_as_byte_integer(self.red),
            _denorm_as_byte_integer(self.green),
            _denorm_as_byte_integer(self.blue),
        )
        if round(self.alpha, 2) >= 1.00:
            return u'#%02X%02X%02X' % rgb
        else:
            return u'rgba(%d, %d, %d, %s)' % (
                rgb + (_format_float(self.alpha),)
            )

    def __str__(self):
        return unicode(self).decode('utf-8')

    def __repr__(self):
        return '<Color %s>' % str(self)

    def lightened(self, percent):
        """
        Return a new :class:`Color` instance lightened by
        ``percent``.

        """
        newlightness = self.lightness + self.lightness * (percent / 100)
        hsl = self.hue, self.saturation, newlightness
        return Color(hsl=hsl, alpha=self.alpha)

    def darkened(self, percent):
        """
        Return a new :class:`Color` instance darkened by
        ``percent``.

        """
        return self.lightened(-percent)

    def saturated(self, percent):
        """
        Return a new :class:`Color` instance saturated by
        ``percent``.

        """
        newsaturation = self.saturation + self.saturation * (percent / 100)
        hsl = self.hue, newsaturation, self.lightness
        return Color(hsl=hsl, alpha=self.alpha)

    def desaturated(self, percent):
        """
        Return a new :class:`Color` instance desaturated by
        ``percent``.

        """
        return self.saturated(-percent)

    def rotated(self, degrees):
        """
        Return a new :class:`Color` instance with the hue rotated
        by ``degrees``.

        """
        newhue = self.hue + degrees / 360.0
        hsl = newhue, self.saturation, self.lightness
        return Color(hsl=hsl, alpha=self.alpha)

    def complemented(self):
        """
        Return a new :class:`Color` instance which is the complement
        of the color.

        """
        return self.rotated(180)

    def purified(self):
        """
        Return a new :class:`Color` instance which is a pure hue
        (100% saturation and 50% lightness).

        """
        return Color(hsl=(self.hue, 1, 0.5), alpha=self.alpha)

class Length(object):
    def __init__(self, value, unit):
        self.value = float(value)
        self.unit = unit.lower()


def _clip_to_range(value, start=0, end=1):
    if value < start:
        return start
    if value > end:
        return end
    return value


def _norm_percent(percent_string):
    return float(percent_string.rstrip('%')) / 100.0


def _norm_byte_integer(integer_string):
    return int(integer_string) / 255.0


def _norm_degrees(degrees_string):
    return float(degrees_string) / 360.0


def _denorm_as_percent_string(normval):
    return u'%s%%' % _format_float(normval * 100.0)


def _denorm_as_byte_integer(normval):
    return int(round(normval * 255.0, 0))


def _format_float(fval):
    base = u'%.2f' % round(fval, 2)
    return base.rstrip(u'0').rstrip(u'.')

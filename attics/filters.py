from __future__ import absolute_import

from functools import wraps

import jinja2

from attics.models import Color
from attics.parsers import parse_color


COLOR_FILTERS = {}

def _color_filter(f):
    """
    Decorator for filters that deal with :class:`models.Color`.

    Ensure that the value passed to the function is a ``Color``
    instance.

    """
    @wraps(f)
    def wrapper(value, *args):
        if not isinstance(value, Color):
            value = parse_color(value)
        return f(value, *args)
    COLOR_FILTERS[wrapper.func_name] = wrapper
    return wrapper


@_color_filter
def lightened(value, percent):
    return value.lightened(float(percent))


@_color_filter
def darkened(value, percent):
    return value.darkened(float(percent))


@_color_filter
def saturated(value, percent):
    return value.saturated(float(percent))


@_color_filter
def desaturated(value, percent):
    return value.desaturated(float(percent))


@_color_filter
def rotated(value, degrees):
    return value.rotated(float(degrees))


@_color_filter
def complemented(value):
    return value.complemented()
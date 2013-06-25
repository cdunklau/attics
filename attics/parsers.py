from __future__ import absolute_import

import os.path

import parsley

from attics.models import Color, Length


with open(os.path.join(os.path.dirname(__file__), 'css_colors.csv')) as _fp:
    print _fp.name
    COLOR_VALUES = {}
    for line in _fp:
        name, red, green, blue = line.strip().split(',')
        COLOR_VALUES[name] = (red, green, blue)
    del name, red, green, blue, line

LENGTH_UNITS = frozenset([
    # Relative
    'em', 'ex', 'ch', 'rem', 'vw', 'vh', 'vmin', 'vmax',
    # Absolute
    'cm', 'mm', 'in', 'px', 'pt', 'pc',
])


css_grammar = parsley.makeGrammar(r"""
# Main rules
color = hash6 | hash3 | colorname | rgb | rgba | hsl | hsla
length = (float | integer):V name:U ?(U in LENGTH_UNITS)
                -> Length(V, U)


# Color types
colorname = name:n ?(n.lower() in COLOR_VALUES)
                -> Color.from_rgb_integer_strings(*COLOR_VALUES[n.lower()])

hash6 =    '#' <hexdigit{6}>:six
                -> Color.from_rgb_integer_strings(
                    *[str(int(six[n:n+2], 16)) for n in range(0,6,2)]
                )
hash3 =    '#' <hexdigit{3}>:three
                -> Color.from_rgb_integer_strings(
                    *[str(int(d * 2, 16)) for d in three]
                )
rgb =   'rgb(' ws
            (
                (integer:R sep integer:G sep integer:B)
                    -> Color.from_rgb_integer_strings(R, G, B)
                | (percent:R sep percent:G sep percent:B)
                    -> Color.from_rgb_percent_strings(R, G, B)
            ):instance
        ws ')' -> instance
rgba =  'rgba(' ws
            (
                (
                    integer:R sep
                    integer:G sep
                    integer:B sep
                    (float | integer):A
                ) -> Color.from_rgb_integer_strings(R, G, B, A)
                | (
                    percent:R sep
                    percent:G sep
                    percent:B sep
                    (float | integer):A
                ) -> Color.from_rgb_percent_strings(R, G, B, A)
            ):instance
        ws ')' -> instance
hsl =   'hsl(' ws (float | integer):H sep percent:S sep percent:L ws ')'
            -> Color.from_hsl_strings(H, S, L)
hsla =  'hsla(' ws
            (float | integer):H sep
            percent:S sep
            percent:L sep
            (float | integer):A
        ws ')' -> Color.from_hsl_strings(H, S, L, A)


# General rules
name = < letter+ >
hexdigit = anything:x ?(x.lower() in 'abcdef0123456789') -> x
sep = < ws ',' ws >
percent = < (float | integer) '%' >
float = < sign digit* '.' digit+ >
integer = < sign digit+ >
number = float | integer
sign = ('+' | '-')?

""", {
    'COLOR_VALUES': COLOR_VALUES,
    'Color': Color,
    'LENGTH_UNITS': LENGTH_UNITS,
    'Length': Length,
})


def parse_color(candidate):
    return css_grammar(candidate).color()


def parse_length(candidate):
    return css_grammar(candidate).length()


def parse_number(candidate):
    return float(css_grammar(candidate).number())

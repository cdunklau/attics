from __future__ import absolute_import

import unittest
import itertools

import pytest

from attics.parsers import css_grammar


class ColorGrammarTestCase(unittest.TestCase):
    def run_rule(self, rule, input):
        return getattr(css_grammar(input), rule)()

    def test_colorname_rule(self):
        names = ['black', 'BLACK', 'goldenrod']
        for name in names:
            self.run_rule('colorname', name)

    def test_hash6_rule(self):
        for hash in ['#012345', '#6789ab', '#cdefff', '#012DEF']:
            self.run_rule('hash6', hash)

    def test_hash3_rule(self):
        for hash in ['#acd', '#123', '#AFF']:
            self.run_rule('hash3', hash)

    def test_rgb_rule_integer(self):
        self.run_rule('rgb', 'rgb(255, 255, 255)')

    def test_rgb_rule_percentage(self):
        self.run_rule('rgb', 'rgb(100%, 100%, 100%)')

    def test_rgba_rule_integer(self):
        self.run_rule('rgba', 'rgba(255, 255, 255, 0.8)')

    def test_rgba_rule_percentage(self):
        self.run_rule('rgba', 'rgba(100%, 100%, 100%, 0.8)')

    def test_hsl_rule(self):
        self.run_rule('hsl', 'hsl(180, 100%, 50%)')

    def test_hsla_rule(self):
        self.run_rule('hsla', 'hsla(180, 100%, 50%, 0.8)')

    def test_color_rule(self):
        self.run_rule('color', '#FF0000')

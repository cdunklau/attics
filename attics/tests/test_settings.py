from __future__ import absolute_import

import unittest
import io
import textwrap
import ConfigParser

from attics.settings import config_to_dict, merge_dict_of_dicts


class ConfigToDictTestCase(unittest.TestCase):
    def run_config_to_dict(self, config_string):
        fp = io.BytesIO(textwrap.dedent(config_string))
        config = ConfigParser.RawConfigParser()
        config.readfp(fp)
        return config_to_dict(config)

    def test_config_to_dict(self):
        config_string = """
            [Meta]
            title: Dead Parrot Sketch
            aired: 7 December 1969
            [Actors]
            customer: John Cleese
            shopkeeper: Michael Palin
        """
        config = {
            'Meta': {
                'title': 'Dead Parrot Sketch',
                'aired': '7 December 1969',
            },
            'Actors': {
                'customer': 'John Cleese',
                'shopkeeper': 'Michael Palin',
            },
        }
        assert self.run_config_to_dict(config_string) == config

    def test_always_lowercased_option_names(self):
        config_string = """
            [Actors]
            CUSTomer: John Cleese
        """
        config = {'Actors': {'customer': 'John Cleese'}}
        assert self.run_config_to_dict(config_string) == config


class UpdateDictOfDictsTestCase(unittest.TestCase):
    def test_base_case(self):
        merged = merge_dict_of_dicts({}, {})
        assert merged == {}
        merged = merge_dict_of_dicts({}, {}, {})
        assert merged == {}
        merged = merge_dict_of_dicts({}, {}, {}, {})
        assert merged == {}

    def test_updates_outer(self):
        first = {'existing': {}}
        second = {'new': {}}
        result = {'existing': {}, 'new': {}}
        merged = merge_dict_of_dicts(first, second)
        assert merged == result

    def test_updates_inner(self):
        first = {'existing': {'tochange': 'originaltochange'}}
        second = {'existing': {'tochange': 'updatedtochange'}}
        result = {'existing': {'tochange': 'updatedtochange'}}
        merged = merge_dict_of_dicts(first, second)
        assert merged == result

    def test_updates_inner_leaving_others(self):
        first = {'existing': {
            'tochange': 'originaltochange',
            'leave': 'originalleave',
        }}
        second = {'existing': {'tochange': 'updatedtochange'}}
        result = {'existing': {
            'tochange': 'updatedtochange',
            'leave': 'originalleave',
        }}
        merged = merge_dict_of_dicts(first, second)
        assert merged == result

    def test_updates_new_inner(self):
        first = {'existing': {}}
        second = {'new': {'newinner': 'newinnerval'}}
        result = {'existing': {}, 'new': {'newinner': 'newinnerval'}}
        merged = merge_dict_of_dicts(first, second)
        assert merged == result

    def test_functional(self):
        first = {
            'existing': {
                'innerkey': 'innervalue',
                'innerkey2': 'notreplaced',
            },
            'existing2': {
                'innerkey': 'innervalue',
                'innerkey2': 'innervalue2',
            },
        }
        second = {
            'existing': {
                'innerkey': 'differentinnervalue',
                'otherinnerkey': 'otherinnervalue',
            },
            'new': {
                'newinnerkey': 'newinnervalue',
            },
        }
        result = {
            'existing': {
                'innerkey': 'differentinnervalue',
                'innerkey2': 'notreplaced',
                'otherinnerkey': 'otherinnervalue',
            },
            'existing2': {
                'innerkey': 'innervalue',
                'innerkey2': 'innervalue2',
            },
            'new': {
                'newinnerkey': 'newinnervalue',
            },
        }
        merged = merge_dict_of_dicts(first, second)
        assert merged == result

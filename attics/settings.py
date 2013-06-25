from __future__ import absolute_import

import os.path


def create_default_settings():
    return {
        'attics': {
            'input_path': 'content',
            'output_path': 'output',
            'theme': 'simple',
            'themedir': None,
        },
        'site': {
            'title': None,
        },
        'colors': {},
        'lengths': {},
        'images': {},
    }


def config_to_dict(config):
    """
    Return a dict of dicts representing the configparser instance
    ``config``.

    The outer keys are section names, the inner keys are option
    names, and the inner values are the option values. For example,
    this input to configparser:

        [Meta]
        title: Dead Parrot Sketch
        aired: 7 December 1969
        [Actors]
        customer: John Cleese
        shopkeeper: Michael Palin

    ...would result in the following structure:

        {
            'Meta': {
                'title': 'Dead Parrot Sketch',
                'aired': '7 December 1969',
            },
            'Actors': {
                'customer': 'John Cleese',
                'shopkeeper': 'Michael Palin',
            },
        }

    """
    return dict(
        (section, dict(config.items(section)))
        for section in config.sections()
    )


def merge_dict_of_dicts(*dicts):
    """
    Return a dict of dicts with values updated in left-to-right
    order.

    """
    if len(dicts) < 2:
        raise TypeError('merge_dict_of_dicts requires at least two arguments')
    out = {}
    for d in dicts:
        for key, inner in d.items():
            out_inner = out.setdefault(key, {})
            out_inner.update(inner)
    return out

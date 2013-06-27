import logging
import ConfigParser

from attics.utils import open_file


logger = logging.getLogger(__name__)


def create_default_settings():
    return {
        'attics': {
            'input_path': 'content',
            'output_path': 'output',
            'theme_search': None,
            'theme': 'simple',
        },
        'site': {
            'title': None,
        },
        'images': {},
        'files': {},
    }


class ConfigError(Exception):
    """Raised when a configuration file couldn't be parsed."""


def parse_config(config_filename):
    """
    Parse ``config_filename`` and return the dict of dicts
    structure representing the configuration file.

    """
    logger.debug("Attempting to parse config at '%s'", config_filename)
    with open_file(config_filename) as cfg_fp:
        cfg = ConfigParser.RawConfigParser()
        try:
            cfg.readfp(cfg_fp)
        except ConfigParser.Error as e:
            raise ConfigError(
                'Failed to parse config file %s: %s' % (
                    config_filename,
                    e,
                )
            )
    return config_to_dict(cfg)


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

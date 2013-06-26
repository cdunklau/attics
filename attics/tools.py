from __future__ import absolute_import

import os.path
import io
import sys
import re
import argparse
import ConfigParser
import logging
import pprint
import textwrap

import jinja2
from ometa.runtime import ParseError

from attics import settings
from attics.processors import MarkdownReader
from attics.parsers import parse_color


logger = logging.getLogger(__name__)


def run(config):
    working_dir = config['attics']['working_dir']
    input_dir = os.path.join(working_dir, config['attics']['input_path'])
    output_dir = os.path.join(working_dir, config['attics']['output_path'])
    themedir = config['attics']['themedir']

    jinjaenv = setup_environment(
        site=config['site'],
        colors=config['colors'],
        lengths=config['lengths'],
        images=config['images'],
    )

    style_template_filename = os.path.join(themedir, 'style.css')
    logger.info("Reading style template '%s'", style_template_filename)
    with open_file(style_template_filename) as style_fp:
        style_template = jinjaenv.from_string(style_fp.read())

    template_filename = os.path.join(themedir, 'index.html')
    logger.info("Reading template '%s'", template_filename)
    with open_file(template_filename) as template_fp:
        template = jinjaenv.from_string(template_fp.read())

    logger.info("Reading input files from '%s'", input_dir)
    pages = MarkdownReader().read_dir(input_dir)
    logger.info("Found %d input files", len(pages))

    write_file(
        os.path.join(output_dir, 'style.css'),
        style_template.render()
    )

    for content, metadata in pages:
        title = metadata['title']
        filename = metadata['filename'] + '.html'
        write_file(
            os.path.join(output_dir, filename),
            template.render(title=title, content=content)
        )


def main():
    args = parse_args()
    setup_logger(args.verbosity)
    config_filename = os.path.abspath(args.config)
    config = make_configuration(config_filename, args)
    run(config)


def make_configuration(config_filename, args):
    default_config = settings.create_default_settings()
    working_dir = os.path.dirname(config_filename)
    default_config['attics']['working_dir'] = working_dir
    user_config = parse_config(config_filename)
    args_config = get_args_config(args)
    base_config = settings.merge_dict_of_dicts(
        default_config,
        user_config,
        args_config,
    )
    themedir = find_themedir(base_config['attics']['theme'], working_dir)
    theme_config = parse_config(os.path.join(themedir, 'theme.ini'))
    config = settings.merge_dict_of_dicts(theme_config, base_config)
    config['attics']['themedir'] = themedir
    logger.debug(
        "Resolved configuration: \n%s",
        pprint.pformat(config, indent=2, width=70)
    )
    logger.info("Validating and processing configuration")
    process_and_validate_config(config)
    return config


def process_and_validate_config(config):
    """
    Validate config and change relevant section values into unified
    types.

    Only validates colors at the moment.

    """
    parsed_colors = {}
    for colorref, colorstr in config['colors'].iteritems():
        try:
            parsed_colors[colorref] = parse_color(colorstr)
        except ParseError:
            logger.warning('Failed to parse color "%s", ignoring' % colorstr)
    config['colors'] = parsed_colors


def setup_environment(site, colors, lengths, images):
    jinjaenv = jinja2.Environment(undefined=jinja2.StrictUndefined)
    jinjaenv.globals['site'] = site
    jinjaenv.globals['colors'] = colors
    jinjaenv.globals['lengths'] = lengths
    jinjaenv.globals['images'] = images
    jinjaenv.globals['parse_color'] = parse_color
    return jinjaenv


def find_themedir(themespec, working_dir):
    """
    Search for the theme name or path.

    Search in this order:

    -   a directory relative to the config file
    -   a theme built in to Attics

    """
    to_search = [
        working_dir,
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'themes',
        ),
    ]
    for search in to_search:
        logger.debug(
            "Searching for theme '%s' in %s" % (
                themespec,
                search,
            )
        )
        themedir = os.path.join(search, themespec)
        if os.path.isdir(themedir):
            break
    else:
        raise FatalError(
            "Could not find theme '%s' in %s" % (
                themespec,
                ' or '.join("'%s'" % d for d in to_search),
            )
        )
    logger.debug("Validating theme at '%s'", themedir)
    for required in ('theme.ini', 'style.css', 'index.html'):
        logger.debug("Checking for '%s'", required)
        if not os.path.isfile(os.path.join(themedir, required)):
            raise FatalError(
                "Could not find required file %s in theme folder '%s'" % (
                    required,
                    themedir,
                )
            )
    logger.debug("Theme contains all required files")
    logger.info("Using theme '%s' at '%s'", themespec, themedir)
    return themedir


def open_file(filename, mode='r'):
    try:
        return io.open(filename, mode, encoding="utf-8")
    except (OSError, IOError) as e:
        raise FatalError(
            'Failed to open file %s, OS reports: "%s"' % (
                filename,
                e,
            )
        )


def write_file(filename, content):
    logger.info("Writing to %s", filename)
    with open_file(filename, 'w') as fp:
        fp.write(content)


def setup_logger(verbosity):
    if verbosity <= 0:
        loglevel = logging.WARNING
    elif verbosity == 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.DEBUG
    logging.basicConfig(stream=sys.stderr)
    logger.setLevel(loglevel)
    logger.debug(
        'logging has been set up with verbosity %d (%s)',
        min(verbosity, 2),
        logging.getLevelName(loglevel),
    )


class FatalError(Exception):
    def __init__(self, msg, *args, **kwargs):
        logger.critical(msg, *args, **kwargs)
        self.args = [msg, args, kwargs]


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
            raise FatalError(
                'Failed to parse config file %s: %s' % (
                    config_filename,
                    e,
                )
            )
    return settings.config_to_dict(cfg)


def get_args_config(args):
    """
    Return a config structure of items from the command line.

    """
    args_regex = re.compile(
        r'^([a-z_]+)\.([a-z_]+)\.(?:=|\s+)(.+)$'
    )
    base = {'site': {}}
    if args.input_path:
        base['site']['input_path'] = args.input_path
    if args.output_path:
        base['site']['output_path'] = args.output_path
    for item in args.options:
        match = args_regex.match(item)
        if match:
            section, option, value = match.groups()
            base.setdefault(section, {})[option] = value
        else:
            logger.warning(
                "Ignoring invalid option spec '%s'" % item
            )
    return base


def parse_args(args=None):
    description = "Create simple static sites from Markdown files.",
    epilog = textwrap.dedent(
        """Relative paths are taken from the configuration file's
        parent directory.
    """)
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS]",
        description=description,
        epilog=epilog,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-v',
        action='count',
        dest='verbosity',
        default=0,
        help='Verbose output. Specify twice for debug output.',
    )
    parser.add_argument(
        '-c', '--config',
        default='site.ini',
        metavar='CONFIGFILE',
        help='The path to the user configuration file',
    )
    parser.add_argument(
        '-i', '--input',
        dest='input_path',
        metavar='INPUT_PATH',
        help=textwrap.dedent(
            """The path to the source content directory relative to
            the configuration file's folder.
        """),
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_path',
        metavar='OUTPUT_PATH',
        help=textwrap.dedent(
            """The path to the output directory relative to the
            configuration file's folder.
        """),
    )
    parser.add_argument(
        '-O', '--option',
        metavar='OPTION',
        dest='options',
        action='append',
        default=(),
        help='Configuration value override.',
    )
    if args is None:
        return parser.parse_args()
    return parser.parse_args(args)

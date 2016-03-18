from __future__ import absolute_import

import os.path
import sys
import argparse
import logging
import pprint
import textwrap
import shlex
import subprocess

from attics.settings import (
    parse_config, create_default_settings, merge_dict_of_dicts,
)
from attics.readers import MarkdownReader
from attics.models import Theme
from attics.utils import copy_file, write_file


logger = logging.getLogger(__name__)


def main():
    args = parse_args()
    setup_logger(args.verbosity)
    try:
        config = make_configuration(
            args.config,
            args.input_path,
            args.output_path
        )
        logger.debug("Using configuration:\n%s" % pprint.pformat(config))
        run(config)
    except Exception as e:
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.exception("Caught exception, traceback:")
        else:
            logger.critical(
                "Caught exception, re-run with -vv for full details: %s" % e
            )
        sys.exit(1)


def run(config):
    input_dir = config['attics']['input_path']
    output_dir = config['attics']['output_path']

    theme = Theme(config['attics']['theme'], config['attics']['theme_search'])
    theme.validate()
    theme.update_files(config, config['attics']['input_path'])

    logger.info("Reading input files from '%s'", input_dir)
    pages = MarkdownReader().read_dir(input_dir)
    pages.sort(key=lambda x: x.title)
    pages.sort(key=lambda x: x.index)
    logger.info("Found %d input files", len(pages))

    for page in pages:
        rendered = theme.render_template(page, pages, config['site'])
        write_file(os.path.join(output_dir, unicode(page)), rendered)
    for file in theme.files.values():
        copy_file(file.location, os.path.join(output_dir, unicode(file)))
    for image in theme.images.values():
        copy_file(image.location, os.path.join(output_dir, unicode(image)))


def compile_less_css(dirpath):
    """
    Attempt to compile files in ``dirpath`` ending with '.less' into
    '.css' files.

    The LESS compiler must be on PATH for this work (``lessc.exe``
    on Windows, ``lessc`` on others).

    """
    less_input_output_files = []
    for name in os.listdir(dirpath):
        if name.lower().endswith('.less') and os.path.isfile(name):
            base, ext = os.path.splitext(name)
            less_input_output_files.append(
                os.path.join(dirpath, '%s.%s' % (base, ext)),
                os.path.join(dirpath, '%s.css' % base),
            )
    if not less_input_output_files:
        return
    if 'win32' in sys.platform:
        lessc = 'lessc.exe'
    else:
        lessc = 'lessc'
    logger.info(
        "Attempting to compile %d LESS files in %s" % (
            len(less_input_output_files),
            dirpath,
        )
    )
    try:
        subprocess.call(lessc)
    except OSError as e:
        logger.warning(
            "Could not find LESS compiler, is it installed and on PATH?"
        )
        return
    for src, dst in less_input_output_files:
        proc = subprocess.Popen(
            [lessc, src, dst],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        if proc.returncode != 0:
            logger.warning("Failed to compile %s, output:" % src)
            logger.warning(out)
            logger.warning("Error output:")
            logger.warning(err)
        else:
            logger.info("Compiled %s to %s" % (src, dst))


def make_configuration(config_filename, input_path=None, output_path=None):
    default_config = create_default_settings()
    theme_search_dir = os.path.dirname(config_filename)
    default_config['attics']['theme_search'] = theme_search_dir
    user_config = parse_config(config_filename)
    args_config = {'attics': {}}
    if input_path is not None:
        args_config['attics']['input_path'] = input_path
    if output_path is not None:
        args_config['attics']['output_path'] = output_path
    return merge_dict_of_dicts(default_config, user_config, args_config)


def setup_logger(verbosity):
    if verbosity <= 0:
        loglevel = logging.WARNING
    elif verbosity == 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.DEBUG
    logging.basicConfig(stream=sys.stderr, level=loglevel)
    logger.debug(
        'logging has been set up with verbosity %d (%s)',
        min(verbosity, 2),
        logging.getLevelName(loglevel),
    )


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
        dest='config',
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
    if args is None:
        return parser.parse_args()
    return parser.parse_args(args)

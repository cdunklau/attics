import io
import shutil
import logging


logger = logging.getLogger(__name__)


def open_file(filename, mode='r'):
    logger.debug("Opening file %s" % filename)
    return io.open(filename, mode, encoding="utf-8")


def write_file(filename, content):
    logger.info("Writing to %s", filename)
    with open_file(filename, 'w') as fp:
        fp.write(content)


def copy_file(src, dest):
    logger.info("Copying %s to %s", src, dest)
    shutil.copy(src, dest)

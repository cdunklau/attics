import os
import os.path
import io
import glob
import itertools
import logging

import markdown

from attics.models import Page


logger = logging.getLogger(__name__)


class MarkdownReader(object):
    file_extensions = ['md', 'markdown', 'mkd', 'mdown']

    def __init__(self):
        self._md = markdown.Markdown(
            output_format='html5',
            safe_mode=False,
            extensions=['meta'],
        )

    def _find_files(self, source_dir):
        """
        Return an iterable of Markdown files in ``source_dir``.

        """
        entries = itertools.chain.from_iterable(
            glob.glob(os.path.join(source_dir, '*.%s' % ex))
            for ex in self.file_extensions
        )
        for entry in entries:
            if os.path.isfile(entry):
                yield entry

    def read(self, path):
        """
        Read and process a Markdown file from ``path`` and return a
        :class:`models.Page` instance.

        """
        logger.info("Reading '%s'", path)
        with io.open(path, encoding='utf-8') as f:
            raw = f.read()
        self._md.reset()
        content = self._md.convert(raw)
        metadata = dict((k, ' '.join(v)) for k, v in self._md.Meta.items())
        return Page(path, content, metadata)

    def read_dir(self, source_dir):
        """
        Read and process Markdown files in ``source_dir`` and return
        a list of (content, metadata) tuples.

        """
        pages = []
        for filename in self._find_files(source_dir):
            pages.append(self.read(filename))
        return pages

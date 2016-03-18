import os
import logging

import jinja2

from attics.settings import parse_config


logger = logging.getLogger(__name__)


BUILT_IN_THEMES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'themes',
)


class FileNotFound(Exception):
    """Raised when an expected file was not found"""


class Theme(object):
    template_name = 'layout.html'
    theme_config_file = 'theme.ini'

    builtin = False
    """True if the theme is built in to Attics"""

    location = None
    """
    The file path to the theme

    An absolute path if built in, relative to the current working
    directory if not.
    """

    name = None
    """The name of the theme"""

    files = None
    """
    A dict of :class:`File` instances keyed by the name specified
    in the config file, to be passed to the template to render.
    """

    images = None
    """
    A dict of :class:`Image` instances keyed by the name specified
    in the config file, to be passed to the template to render.
    """

    template = None
    """The ``jinja2.Template`` instance used for rendering pages"""

    _themespec = None
    _search_dir = None

    def __init__(self, themespec, search_dir):
        self._themespec, self._search_dir = themespec, search_dir
        self.images, self.files = {}, {}

    def validate(self):
        self._find_themedir()
        self._validate_files()
        self._parse_template()
        config = parse_config(os.path.join(self.location, 'theme.ini'))
        self.update_files(config, self.location)
        logger.info("Using theme '%s' at '%s'", self.name, self.location)

    def render_template(self, page, pages, site):
        """
        Render :attr:`template` with the images, files, and page
        content and metadata.

        :param page:    the :class:`Page` to render as content
        :param pages:   a list of :class:`Page` instances to use in
                        for navigation links
        :param site:    a dict of strings for use in the template

        """
        return self.template.render({
            'files': self.files,
            'images': self.images,
            'pages': pages,
            'page': page,
            'site': site,
        })

    def update_files(self, config, base):
        """
        Resolve the image and file paths in ``config`` (relative to
        ``base``) into :class:`Image` and :class:`File` instances
        and update their respective attributes.

        """
        for imagespec, imagepath in config.get('images', {}).iteritems():
            image = Image(os.path.join(base, imagepath), imagespec)
            self.images[imagespec] = image
        for filespec, filepath in config.get('files', {}).iteritems():
            file = File(os.path.join(base, filepath), filespec)
            self.files[filespec] = file

    def _find_themedir(self):
        """
        Search for the theme name or path, and set the discovered
        path as :attr:`location`.

        Search in this order:

        -   relative to :attr:`_search_dir`
        -   a theme built in to Attics

        If ``themespec`` is a path, the built in theme search will
        be skipped.

        """
        themespec = self._themespec
        search_dir = self._search_dir
        logger.info("Searching for theme '%s'" % themespec)
        themedir = os.path.join(search_dir, themespec)
        logger.debug("Checking '%s'" % themedir)
        if os.path.isdir(themedir):
            logger.info("Found theme at '%s'" % themedir)
            self.location = themespec
            self.name = os.path.basename(themespec)
        elif not os.path.dirname(themespec):
            themedir = os.path.join(BUILT_IN_THEMES, themespec)
            logger.debug("Checking '%s'" % themedir)
            if os.path.isdir(themedir):
                logger.info("Found built-in theme at '%s'" % themedir)
                self.location = themedir
                self.name = themespec
                self.builtin = True
        else:
            raise FileNotFound("Could not locate theme '%s'" % themespec)

    def _validate_files(self):
        """
        Check that :attr:`location` contains all the required files.

        """
        themedir = self.location
        logger.debug("Validating theme at '%s'", themedir)
        for required in (self.theme_config_file, self.template_name):
            logger.debug("Checking for '%s'", required)
            if not os.path.isfile(os.path.join(themedir, required)):
                raise FileNotFound(
                    "Could not find required file %s in theme folder '%s'" % (
                        required,
                        themedir,
                    )
                )
        logger.debug("Theme contains all required files")

    def _parse_template(self):
        """
        Parse the "layout.html" template into a ``jinja2.Template``
        instance and assign it to :attr:`template`.

        """
        logger.debug(
            'Loading template at %s' % os.path.join(
                self.location,
                self.template_name
            )
        )
        env = jinja2.Environment(
            undefined=jinja2.StrictUndefined,
            loader=jinja2.FileSystemLoader(self.location),
        )
        self.template = env.get_template(self.template_name)


class File(object):
    location = None
    name = None
    extn = None

    def __init__(self, path, name=None):
        if not os.path.isfile(path):
            raise FileNotFound(path)
        self.location = os.path.normpath(path)
        self.extn = os.path.splitext(path)[1]
        self.name = name or os.path.normpath(os.path.basename(path))

    def __unicode__(self):
        return self.name + self.extn

    def __repr__(self):
        return '<File %s at %s>' % (self.name, self.location)


class Image(File):
    def __repr__(self):
        return '<Image %s at %s>' % (self.name, self.location)


class Page(File):
    content = None
    title = None
    index = None

    def __init__(self, path, content, metadata):
        self.location = os.path.normpath(path)
        self.content = content
        self.extn = '.html'
        no_ext = os.path.basename(os.path.splitext(path)[0])
        self.name = metadata.get('name', no_ext)
        self.title = metadata.get('title', no_ext)
        index_candidate = metadata.get('index', '0')
        try:
            self.index = int(index_candidate)
        except ValueError:
            logger.warning(
                'Invalid index %s in page %s, ignoring' % (
                    index_candidate,
                    self.location,
                )
            )
            self.index = 0

    def __repr__(self):
        return '<Page %s at %s>' % (self.name, self.location)

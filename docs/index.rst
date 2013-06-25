Attics
######

Attics is a generator for simple sites, written in Python_, and leverages
Markdown_ and Jinja2_ for content generation and templating. It supports
Python versions 2.6, 2.7, 3.2, and 3.3.

.. _Python: http://www.python.org/
.. _Markdown: http://pythonhosted.org/Markdown/
.. _Jinja2: http://jinja.pocoo.org/

Basic usage
===========

The configuration file
======================

Attics uses a configuration file with INI-like syntax, its default name is
"attics.ini". There is one required section (*site*) with one required option
(*title*). A minimal example::

    [site]
    title: My Attics Site

Sections consist of a section name (surrounded by square brackets) followed by
zero or more ``option: value`` pairs. Section and option names must be
lowercased. Blank lines and lines that start with ``#`` or ``;`` are ignored.
Those characters can be used to insert comments. Here is a more detailed
example::

    [site]
    title: Similar Pet Shops Ltd.
    slogan: Your friends in Ipswitch
    [colors]
    # not sure about the blue... lighten it up a bit?
    primary: #1240AB
    secondary: #FFAA00
    [lengths]
    large_border: 20px
    small_border: 10px


The "site" section
------------------

This section contains overall settings for your project.

For files and folders, relative paths are based off of the directory of the
configuration file.

.. data:: title

    The title of the site. The only required option.

    With the default theme, this is rendered in the main banner, and will
    appear in the title bar of your browser window or tab.

.. data:: slogan

    The slogan for the site. Blank by default.

.. data:: input_path

    The folder where the source files are located (default *content*).

.. data:: output_path

    The folder where the generated HTML, CSS, and other files will be placed
    (default: *output*).

.. data:: url_prefix

    The prefix to use on all internal URLs (default */*).

    May be a full URL, or just a path.


The "colors", "lengths", and "images" sections
=================================================

There are three other sections that are used by themes. The *colors* section
allows you to change the colors, *lengths* allows you to change things
like margin, border, text, and column sizes, and *images* allows you to
provide your own images for things like logos and background images.


Commands
========

The ``attics`` command is the main interface into the program:

``attics [options] COMMAND [args]``
    Options:

    ``-c CONFIGFILE, --config=CONFIGFILE``
        Path to the user configuration file. Defaults to ``site.ini``.
    ``-i SOURCEDIR, --input=SOURCEDIR``
        Path to the directory where source content is located. Defaults to
        ``content``.
    ``-o DESTDIR, --output=DESTDIR``
        Path to the directory where the output files will be generated.
        Defaults to ``output``.
    ``-O OPTION, --option=OPTION``
        Add or override theme config values.  

        OPTION consists of a SECTION, a period, a NAME, the equals sign, and
        a VALUE: ``SECTION.NAME=VALUE``. SECTION is the section in the
        configuration file where the option is defined, NAME is the name of
        the option, and VALUE is the value assigned to the option.

        For example, if the config file specifies a ``favorite`` option in
        the ``[colors]`` section with a value of ``blue``, this will override
        it to ``yellow`` if provided on the command line:
        ``-O colors.favorite=yellow``

``attics generate``
    Attempt to find a ``site.ini`` file in the current folder and use that to
    generate the site content.

``attics testtheme THEMEDIR``
    Validate the structure and configuration files in THEMEDIR to ensure they
    are valid. 


Contents:

.. toctree::
    :maxdepth: 2

    themes.rst
    


Indices and tables
##################

*   :ref:`genindex`
*   :ref:`modindex`
*   :ref:`search`


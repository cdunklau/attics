Attics
######

Attics is a generator for simple sites, written in Python_. It supports
Python versions 2.6 and 2.7.

.. _Python: http://www.python.org/

While there are other static site generators available, those that I've seen
tend to have some common blockers for what I wanted to accomplish. The goals
of Attics are:

1.  Set up and usage must be as easy as possible for non-programmers.
2.  KISS: simplicity is paramount. No need to support heirarchical layouts
    or bother with chronological contexts: there are other generators
    that do that stuff already.
3.  Simple built-in themes as well as the ability to point to a custom theme.

Basic usage
===========

The configuration file
======================

Attics uses a configuration file with INI-like syntax, its default name is
"site.ini". There is one required section ("site") with one required option
("title"). A minimal example::

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
    [attics]
    oup


The "site" section
------------------

This section contains overall settings for your project.

.. data:: title

    The title of the site. The only required option.

    With the default theme, this is rendered in the main banner, and will
    appear in the title bar of your browser window or tab.

Themes may define other options in this section for you to use.


The "attics" section
--------------------

This section allows you to change the input and output directories, theme,
and theme search folder. Paths are relative to the folder where the config
file is located.

.. data:: theme

    The name or path of the theme to use (default *content*). This can be one
    of the themes built in to Attics, or a custom theme.

.. data:: theme_search

    The path to the location of custom themes. Defaults to the folder where
    the config file is located.

.. data:: input_path

    The folder where the source files are located (default *content*).

.. data:: output_path

    The folder where the generated HTML, CSS, and other files will be placed
    (default: *output*).


The "files" and "images" sections
---------------------------------

Themes may define files (such as CSS and JS assets) and images (such as logos
and backgrond images) that are referenced in the page rendering. You may
override any of these in your site.ini.


Commands
========

The ``attics`` command is the main interface into the program:

``attics [options]``
    Options:

    ``-c CONFIGFILE, --config=CONFIGFILE``
        Path to the user configuration file. Defaults to ``site.ini``.
    ``-i SOURCEDIR, --input=SOURCEDIR``
        Path to the directory where source content is located. Defaults to
        ``content``, relative to the folder where the config file is located.
    ``-o DESTDIR, --output=DESTDIR``
        Path to the directory where the output files will be generated.
        Defaults to ``output``, relative to the folder where the config file
        is located.

Contents:

.. toctree::
    :maxdepth: 2

    themes.rst
    


Indices and tables
##################

*   :ref:`genindex`
*   :ref:`modindex`
*   :ref:`search`


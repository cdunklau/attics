Creating Themes
###############

Structure
=========

A theme is named after its enclosing folder. The folder must contain the
following files:

``theme.ini``
    The configuration file. This file defines the variable names and default
    values to be used in the templates. These variables can be overridden by
    the end user of your theme so they can customize the look and feel of the
    theme without changing the theme itself.

``index.html``
    Jinja2 template which defines the layout of the pages themselves.

All other files in the folder which are registered in the config file will be
copied to the assets directory in the output path unless overridden by user
settings.

Here is an example of the structure of a typical theme::

    theme_name/
    │
    ├── theme.ini
    ├── layout.html
    ├── style.css
    └── biglogo.png


The theme.ini configuration file
================================

.. _ConfigParser: http://docs.python.org/2/library/configparser.html

The configuration file uses INI-like syntax supported by Python's
ConfigParser_ module, and should contain three sections: ``[colors]``,
``[lengths]``, and ``[images]``.

-   Each of the sections contains zero or more ``name: value`` pairs, where
    ``name`` is the name of the variable used in the templates, and ``value``
    is the *default* value.
-   Section names must be lowercased.
-   Value names can only contain ASCII letters, digits, and the underscore.
    Case is not significant, but value names should be lowercased, as they
    will be provided to the templates lowercased.
-   Blank lines and lines that start with ``#`` or ``;`` are ignored. Those
    characters can be used to insert comments.

An example configuration file, which fits with the example folder structure
from above::

    [files]
    stylesheet: style.css
    [images]
    logo: biglogo.png


Writing Templates
=================

.. _`Jinja2 website`: http://jinja.pocoo.org/docs/templates/

Templates are written using Jinja2 syntax. You can find the full template
designer documentation on the `Jinja2 website`_.

The parameters from the configuration file are accessible from three global
variables, named after the sections in the configuration file. Each default
value's name is accessed with a dot on the end of the section name: To access
our logo image, it's simply ``images.logo``, and the stylesheet is just
``files.stylesheet``. Inside the template, the syntax is:

.. code-block:: html+jinja

    <link href="{{ files.stylesheet }}" rel="stylesheet" type="text/css">

    <img src="{{ images.logo }}" alt="logo">

Along with ``files`` and ``images`` from the config file (or the user's
overrides), the template is also passed ``page`` (the current page being
rendered) and ``pages`` (a list of all the pages).






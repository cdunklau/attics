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

``style.css``
    A "dynamic" stylesheet that responds to user-configured values for colors,
    lengths, and image URLs.

All other files in the folder will be copied to the assets directory in the
output path unless overridden by user settings.

Here is an example of the structure of a typical theme::

    theme_name/
    │
    ├── theme.ini
    ├── index.html
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

    [colors]
    primary: green
    text: darkblue
    [lengths]
    # This should be between 500 and 800 px
    main_column_width: 600px
    font_size: 1.5em
    [images]
    logo: biglogo.png

For default values, there are some restrictions to make testing simpler. The
theme tester and site generator will reject invalid defaults.

-   Default values for ``[colors]`` and ``[lengths]`` may be any valid CSS
    color and dimension, respectively.
-   Values in the ``[images]`` section are the file names of image files in
    the ``static/img/`` folder.


Writing Templates
=================

.. _`Jinja2 website`: http://jinja.pocoo.org/docs/templates/

Templates are written using Jinja2 syntax. You can find the full template
designer documentation on the `Jinja2 website`_.

The parameters from the configuration file are accessible from three global
variables, named after the sections in the configuration file. Each default
value's name is accessed with a dot on the end of the section name: To access
our logo image, it's simply ``images.logo``. Inside the template, the syntax
is:

.. code-block:: html+jinja

    {{ images.logo }}
    <!-- to use in an image tag, just use it in the src attribute: -->
    <img src="{{ images.logo }}" alt="logo">

Similarly, we can access the colors and lengths as well, although you
probably want to do that from the stylesheet.

.. code-block:: css+jinja

    body {
        color: {{ colors.text }};
    }
    h1,h2,h3,h4 {
        color: {{ colors.primary }};
    }

Using Colors
------------

Colors specified in the config file are parsed into a unified type. You can
use the methods on the color objects to transform them in various ways.
This makes it a snap to use only a few colors on which to base the entire
theme:

.. code-block:: css+jinja

    body {
        color: {{ colors.text }};
        background-color: {{ colors.primary.desaturated(50) }};
    }
    h1,h2,h3,h4 {
        color: {{ colors.primary.lightened(30) }};
    }

You can use the ``parse_color`` function to turn a valid CSS color string
into a color type, so you can use the transformation methods:

.. code-block:: css+jinja

    {% set textcolor = parse_color("#0000aa") %}
    body {
        color: {{ textcolor }};
    }
    h1,h2,h3,h4 {
        color: {{ textcolor.lightened(30) }};
    }


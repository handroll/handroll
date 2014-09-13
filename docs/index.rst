handroll - A website generator for software artisans
====================================================

handroll is a static website generator that uses markup languages like
Markdown, reStructuredText, and Textile.

handroll development is done on `GitHub
<https://github.com/mblayman/handroll>`_. Announcements and discussions happen
on `Google Groups <https://groups.google.com/forum/#!forum/handroll>`_.

Installation
------------

handroll is available for download from `PyPI
<https://pypi.python.org/pypi/handroll>`_.  You can install it with ``pip``.
handroll is currently supported on Python 2.6, 2.7, 3.3, 3.4, and PyPy.

.. code-block:: bash

   $ pip install handroll

Usage
-----

When inside a website's source directory, the following command will generate
results and store them in ``output``. Use ``handroll -h`` to see all the
options.

.. code-block:: bash

    $ handroll
    Complete.

Features
--------

handroll follows a *"batteries included"* philosophy for generating static
websites. One goal is to support a wide range of tools to cater to many diverse
interests. The list below isn't exhaustive, but it provides a good idea of
what handroll is capable of doing.

* Copy static assets like CSS or JavaScript.
* Convert `Markdown <http://daringfireball.net/projects/markdown/>`_ to HTML.
* Convert `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ to
  HTML.
* Convert `Textile <http://en.wikipedia.org/wiki/Textile>`_ to HTML.
* Generate a proper `Atom XML
  <http://en.wikipedia.org/wiki/Atom_%28standard%29>`_ feed from metadata
  stored in JSON.
* Find the site source root so you don't have to. If you're anywhere in your
  site's source, calling ``handroll`` without the site input parameter will
  trigger handroll to look for your site's root directory.
* Store global configuration in a configuration file (see
  :ref:`configuration`). You'll never need to specify the output directory
  again.
* Keep extra data for templates in a separate front matter section in YAML
  format (see :ref:`frontmatter`).
* Templates can use the Jinja2 template engine.
* Content is only updated when either a template or the source file is newer
  than the existing output file. This eliminates wasted regeneration on
  unchanged content.
* Be extensible for users who want to write their own plugins (see
  :ref:`composers`).
* Provide timing information to see file processing time.

The remaining documentation provides additional details about all listed
features.

Documentation
-------------

.. toctree::
    :maxdepth: 2

    configuration
    composers
    templates
    i18n
    releases

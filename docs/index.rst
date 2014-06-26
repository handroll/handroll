handroll - A website generator for software artisans
====================================================

handroll is a static website generator that uses markup languages like
Markdown, reStructuredText, and Textile.

handroll development is on `GitHub <https://github.com/mblayman/handroll>`_.

Installation
------------

handroll is available for download from `PyPI
<https://pypi.python.org/pypi/handroll>`_.  You can install it with ``pip``.
handroll is currently supported on Python 2.6, 2.7, 3.3, 3.4, and PyPy.

.. code-block:: bash

   $ pip install handroll

Usage
-----

When ``site`` is the source of a website, the following command will generate
results and store them in ``site/output``. Use ``handroll -h`` to see all the
options.

.. code-block:: bash

    $ handroll site
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
* Be extensible for users who want to write their own plugins.
* Provide timing information to see file processing time.
* Find the site source root so you don't have to. If you're anywhere in your
  site's source, calling ``handroll`` without the site input parameter will
  trigger handroll to look for your site's root directory.

The remaining documentation provides additional details about all listed
features.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   composers
   releases

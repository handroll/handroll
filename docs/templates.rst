Templates
=========

handroll supports multiple template systems. Templates are stored in a
``templates`` directory at the root of your site. Alternatively, if you have
very simple needs, you can use a ``template.html`` file at your site's root.

Any template used from the ``templates`` directory must be specified using
front matter (see :ref:`frontmatter`) or the default ``template.html`` will be
used. This sample Markdown file uses a string template.

.. literalinclude:: ../sample/use_different.md

String templates
----------------

Any template using the ``.html`` extension (including the default
``template.html``) will uses Python's `built-in string templates
<https://docs.python.org/library/string.html#template-strings>`_. String
templates are limited to the capabilities of the standard library, but they
can support basic needs.

Jinja2 templates
----------------

Any template using the ``.j2`` extension will use the `Jinja2
<http://jinja.pocoo.org/docs/dev/>`_ template language. handroll works with
Jinja's template inheritance system and the majority of Jinja's other features.

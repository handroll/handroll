.. _configuration:

Configuration
=============

handroll supports an optional ``handroll.conf`` file that can be stored at the
root of the site's directory. This ``ini`` style file provides configuration
information that handroll will use while generating the output. For example:

.. code-block:: ini

    [site]
    outdir = ~/mblayman.github.io

Arguments provided on the command line will override the equivalent
configuration file option.

``site`` section
----------------

The ``outdir`` option will determine the output directory. If a tilde character
(``~``) is supplied, it will be expanded to the user's home directory.

The ``with_blog`` option set to ``true``, ``on``, ``yes``, or ``1`` will
enable the blog extension.
See :ref:`blogextension` for setup information.

.. _frontmatter:

Front matter
============

Source documents like Markdown files can have additional data added to them.
This data is stored in a front matter section at the top of a source document.
handroll will read the extra data and pass it along to the template. In the
template, the data will be accessible by whatever name was provided. An
example Markdown source document would look like:

.. literalinclude:: ../sample/frontmatter.md
   :lines: 2-

You may also include the YAML directive (e.g., ``%YAML 1.1``).
The following example is equally valid.

.. literalinclude:: ../sample/frontmatter.md

Note: When using front matter, handroll does not infer the title from the first
line of the document. If a title is desired, the attribute must be explicitly
added to the front matter.

.. _extensions:

Extensions
==========

In addition to :ref:`composers`, handroll has an extension system
to plug in other functionality.
Users enable extensions
by adding ``with_* = true`` to their ``site`` section
in the configuration file,
where ``*`` is the name of the extension.
For example, the blog extension is named ``blog``,
and ``with_blog = true`` will enable it.

Extension authors can use the base ``Extension``
to create new extensions.
Extensions are never directly called,
but an extension can connect to one of handroll's :ref:`signals`.

.. autoclass:: handroll.extensions.base.Extension
   :members:

Extension authors can include new extensions by adding to the
``handroll.extensions`` entry point. For example, handroll includes
the following entry point in ``setup.py``:

.. code-block:: python

   entry_points={
       'handroll.extensions': [
           'blog = handroll.extensions.blog:BlogExtension',
       ]
   }

Built-in extensions
===================

.. _blogextension:

Blog extension
--------------

The blog extension allows you to automatically generate an atom feed
of blog entries.
It can also create an entry list for one of your pages.

Enable the blog extension by adding ``with_blog = True`` to
the ``site`` section of your configuration file.

The extension requires some additional information
to create a valid atom feed.
Add a ``blog`` section to your configruation file
with the following fields:

* ``atom_author`` - The author of the blog
* ``atom_id`` - A unique identifier for the atom feed.
  One suggestion is to use the URL *of the feed itself*.
  For example, ``http://www.mattlayman.com/feed.xml``.
* ``atom_title`` - The title of the blog
* ``atom_url`` - The URL for the feed.
  For example, ``http://www.mattlayman.com/archive.html``.

To create the atom feed, you need to specify an output path
using the ``atom_output`` option.
The path provided is relative to the output directory.

.. code-block:: ini

    [blog]
    atom_output = feed.xml

In this example, the atom feed would be stored
in the root of the output directory
with a filename of ``feed.xml``.

TODO: Document the entry list template handling.

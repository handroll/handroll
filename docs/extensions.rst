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

.. autoclass:: handroll.extensions.blog.BlogExtension

.. _composers:

Composers
=========

``handroll`` uses a plugin system to decide how to process each file type. The
plugins are called composers. A composer is provided a source file and can
produce whatever output it desires.  ``handroll`` will load each available
composer using ``setuptools`` entry points. ``handroll`` loads the class and
constructs a ``Composer`` instance by invoking a no parameter constructor.

.. autoclass:: handroll.composers.Composer
   :members:

A plugin should be added to the ``handroll.composers`` entry point group. For
example, the ``MarkdownComposer`` plugin included by default defines its entry
point in ``setup.py`` as:

.. code-block:: python

   entry_points={
       'handroll.composers': [
           '.md = handroll.composers.md:MarkdownComposer',
       ]
   }

This entry point registers the ``MarkdownComposer`` class in the
``handroll.composers.md`` module for the ``.md`` file extension. The example is
slightly confusing because the entry point name and the package are the same so
here is a fictious example.

A composer class called ``FoobarComposer`` defined in ``another.package`` for
the ``.foobar`` file extension would need the following entry point.

.. code-block:: python

   entry_points={
       'handroll.composers': [
           '.foobar = another.package:FoobarComposer',
       ]
   }

Built-in composers
==================

.. autoclass:: handroll.composers.atom.AtomComposer

.. autoclass:: handroll.composers.CopyComposer

.. autoclass:: handroll.composers.md.MarkdownComposer

.. autoclass:: handroll.composers.rst.ReStructuredTextComposer

.. autoclass:: handroll.composers.sass.SassComposer

.. autoclass:: handroll.composers.txt.TextileComposer

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

Atom feed
~~~~~~~~~

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

List page
~~~~~~~~~

To create a blog list page,
add a ``list_template`` option to your ``blog`` section.
If you include ``list_template``,
then you must also include ``list_output``.
``list_output`` is a path relative to the output directory.

When the blog extension generates the list page,
the context will receive a ``blog_list``.
The ``blog_list`` is an HTML fragment of list item tags.
There is one list item tag for every post.

Here is a possible sample template.

.. code-block:: html+jinja

    <html>
    <body>
      <ul>
        {{ blog_list }}
      </ul>
    </body>
    </html>

And here is some possible output.

.. code-block:: html

    <html>
    <body>
      <ul>
        <li><a href="/another_post.html">Another post</a></li>
        <li><a href="/a_post.html">First post!</a></li>
      </ul>
    </body>
    </html>

For more complex formatting,
the actual blog posts are provided
in the context
as ``posts``.

Blog post frontmatter
~~~~~~~~~~~~~~~~~~~~~

A source file is marked as a blog post by setting ``blog: True``
in the front matter.
The blog front matter has required and optional fields.

Required fields:

* ``title`` - The title of the post
* ``date`` - The published date of the post.
  The date should be in RfC 3339 format
  (e.g., ``2015-07-15T12:00:00Z``).

Optional fields:

* ``summary`` - A summary of the post.

.. _sitemapextension:

Sitemap extension
-----------------

The sitemap extension generates a sitemap
of your site's HTML content.
The generated file will be stored
in the root
of the output directory
as ``sitemap.txt``.

Enable the sitemap extension by adding ``with_sitemap = True`` to
the ``site`` section of your configuration file.

.. _opengrapheextension:

Open Graph extension
--------------------

The Open Graph extension reads blog post frontmatter
and adds ``open_graph_metadata`` to the template context.
The data can be added to the ``head`` section of the HTML output.

Enable the Open Graph extension by adding ``with_open_graph = True``
to the ``site`` section of your configuration file.

The extension produces the metadata for an Open Graph ``article``.
As the ``article`` type requires an image,
additional configuration is required so that an image is always available.

You must include an ``open_graph`` section
with a ``default_image``.
The ``default_image`` is a full URL
to an image file.
This default image will be used
whenever an ``image`` is not specified
in a blog post's frontmatter.

.. code-block:: ini

    [open_graph]
    default_image = http://www.example.com/images/og.jpg

When ``image`` is provided
in the frontmatter,
the value produces a URL that is related to the source file.
For example,
if you have a post in your site at a path of ``posts/my-topic.md``
and the frontmatter includes ``image: butterfly.jpg``,
then the included image URL would become
``http://www.example.com/posts/butterfly.jpg``.

``image`` can also use an absolute path.
If the frontmatter sets ``image: /images/ladybug.jpg``,
the final URL would be ``http://www.example.com/images/ladybug.jpg``
regardless of where the blog post is
in your site structure.

To include the metadata,
add it to your template:

.. code-block:: jinja

    <html>
     <head>
       {{ open_graph_metadata }}
     </head>
     <body>
     </body>
    </html>

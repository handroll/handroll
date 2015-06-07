.. _signals:

Signals
=======

handroll fires various signals while running. These signals provide hooks
for extensions to execute additional code. The list of signals is provided
below.

frontmatter_loaded
------------------

``frontmatter_loaded`` fires whenever a file contains a front matter section
(see :ref:`frontmatter`). Any handler function that connects to the signal
will be called with:

* ``source_file`` - The absolute path to the file containing front matter.
* ``frontmatter`` - The front matter dictionary that was loaded.

pre_composition
----------------

``pre_composition`` fires before processing the entire site. When the
watcher is running (see :ref:`devserver`), the signal will fire before
handling any file or directory change.
Any handler function that connects to the signal will be called with:

* ``director`` - The director instance that processed the site.

post_composition
----------------

``post_composition`` fires after processing the entire site. When the
watcher is running (see :ref:`devserver`), the signal will fire after
handling any file or directory change.
Any handler function that connects to the signal will be called with:

* ``director`` - The director instance that processed the site.

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

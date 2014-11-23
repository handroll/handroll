.. _devserver:

Development server
==================

handroll comes with a built-in development server. The server helps develop
websites even faster by watching the changes you make. As files in your site
are created, modified, or moved, the server will update your output with each
change.

The development server is available with the ``w`` or ``watch`` flag. The
server will make your site accessible on ``http://localhost:8000``.

Here is an example:

.. code-block:: bash

    matt@eden:~/handroll/sample$ handroll -w
    Serving /home/matt/handroll/sample/output at http://localhost:8000/.
    Press Ctrl-C to quit.
    Generating HTML for /home/matt/handroll/sample/index.md ...

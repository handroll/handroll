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

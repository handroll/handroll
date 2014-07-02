Releases
========

Version 1.2, July 2, 2014
-------------------------

* Add a basic configuration file to specify the output directory.
* A search for the site root is done when no site path is provided.
* Add timing reporting to find slow composers.
* Update Textile version to enable Python 3 support.
* Generate Atom feeds.
* Drop 3.2 support. Too many dependencies do not support it.

Version 1.1, Released June 1, 2014
----------------------------------

* Skip undesirable file types (e.g., Vim .swp files).
* Use Markdown code highlighting (via Pygments) and fenced code extensions.
* All input and output is handled as UTF-8 for better character encoding.
* Run against Python versions 2.6 through 3.4 using Travis CI.
* Add a plugin architecture to support composers for any file type.
* Provide HTML docs at Read the Docs.
* Textile support for ``.textile`` files.
* ReStructuredText support for ``.rst`` files.
* Support PyPy.

Version 1.0, Released May 4, 2014
---------------------------------

* Initial release of ``handroll``
* Copy all file types.
* Convert Markdown to HTML.


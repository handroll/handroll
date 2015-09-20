Releases
========

Version 2.1, In Development
---------------------------

* Use the SmartyPants library to generate better quotation
  marks for Markdown.
* Composers can be forced to compose with the ``--force`` flag.
* Translated to Arabic.
* Relax the frontmatter requirement and don't force the
  inclusion of the YAML directive (e.g., ``%YAML 1.1``).

Version 2.0, Released July 25, 2015
-----------------------------------

* Added an extension interface for plugin authors to integrate
  with various events.
* Added a blog extension to automatically generate an Atom XML
  feed and blog listing page.
* Translated to Greek.

Version 1.5, Released February 24, 2015
---------------------------------------

* Translated to Dutch.

Version 1.4, Released December 1, 2014
--------------------------------------

* A development server (accessible from the ``watch`` flag) will monitor a site
  and generate new output files as the source is modified.
* Sass support for ``.scss`` and ``.sass`` files.
* Add internationalization (i18n).
* Translated to French, German, Italian, Portuguese, and Spanish.
* Skip certain directories that should not be in output (like a Sass cache).
* Moved project to a GitHub organization to separate from a personal account.
* Include documentation in the release.
* Massive unit test improvements (100% coverage).

Version 1.3, Released September 3, 2014
---------------------------------------

* Update the appropriate output only when a template or content was modified.
* Use Jinja templates or standard Python string templates.
* Provide YAML formatted front matter to add any data to a template.

Version 1.2, Released July 2, 2014
----------------------------------

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


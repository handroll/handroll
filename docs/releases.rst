Releases
========

Version 3.1, In Development
---------------------------

* Processs Jinja 2 templates for any file with a ``.j2`` extension
  with the built-in ``Jinja2Composer``.
* Add ``SitemapExtension`` to generate sitemaps.
* Move version information into the ``handroll`` package
  so it is available at runtime.
* Perform continuous integration testing on OS X.
* Include ``posts`` in the blog feed list
  to permit more complex list rendering.

Version 3.0, Released March 7, 2016
-----------------------------------

* Replaced all flag based commands with sub-commands.
  This change means all interaction now happens through
  ``handroll build``, ``handroll watch``, and ``handroll scaffold``.

Version 2.1, Released October 18, 2015
--------------------------------------

* Create a site quickly with the new scaffold command
  (e.g., ``handroll -s default new_site``)
* Use the SmartyPants library to generate better quotation
  marks for Markdown.
* Composers can be forced to compose with the ``--force`` flag.
* Translated to Arabic.
* Relax the frontmatter requirement and don't force the
  inclusion of the YAML directive (e.g., ``%YAML 1.1``).
* Support Python 3.5.
* An output directory can be a relative path.

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


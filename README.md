handroll
========

[![PyPI version][pypishield]](https://pypi.python.org/pypi/handroll)
[![BSD license][license]](https://raw.githubusercontent.com/handroll/handroll/master/LICENSE)
[![Build Status][travis]](https://travis-ci.org/handroll/handroll)
[![Coverage Status][coverage]](https://codecov.io/github/handroll/handroll)

Website development is a finely crafted art.

You need simple. You know what you're doing. You don't want to waste time.

`handroll` knows you are the boss. With one command, you gracefully blend your
theme and content into one precise result.

```bash
$ pip install handroll
...
Successfully installed handroll
$ handroll build site
Complete.
```

Just the facts
--------------

`handroll` walks your website source (i.e. `site` as shown above), copying
everything that it can find. When it encounters:

1.  anything ending in `.md`, the file will be read, the first line of the file
    will become the `title`, and the remainder will be converted from Markdown
    into HTML to become the `content`. `title` and `content` will be combined
    with a template to produce the final HTML file.
2.  any other "known" extension will be handled by a corresponding composer.
    `handroll` works with Markdown, reStructuredText, and Textile out of the
    box.
3.  a template (either `template.html` or anything in `templates`), the file
    will be skipped.

Everything else
---------------

Check out
[the feature list](http://handroll.readthedocs.io/en/latest/#features)
to see if handroll meets your needs.
If not, please tell us with a GitHub issue or on the mailing list.

All the other stuff you may be interested in regarding `handroll`
(e.g., writing a plugin for your favorite markup language)
is found at [Read the Docs](http://handroll.readthedocs.io/en/latest/).

If you want to share some ideas or find announcements,
check out the [Google Group](https://groups.google.com/forum/#!forum/handroll).

handroll is
[BSD licensed](https://github.com/handroll/handroll/blob/master/LICENSE)
and tested on Linux and OS X.

Get Involved
------------

Bring an idea to the table! Implement it in a fork or submit an issue to have
some discussion about it.

handroll needs a better identity. If you're a web developer or
designer, please consider helping with a
[logo](https://github.com/handroll/handroll/issues/14).

Translators can join the fun by translating at the
[Transifex project](https://www.transifex.com/projects/p/handroll/).
Additional translation details are in the[translation
documentation](http://handroll.readthedocs.io/en/latest/i18n.html).

Want to write some code?
Running these commands should set up your environment
with all the tools you need to contribute.

```bash
$ # Start from the root of a handroll clone.
$ virtualenv venv                            # Create your virtual environment.
$ source venv/bin/activate                   # Activate it.
(venv)$ pip install -r requirements-dev.txt  # Install developer tools.
(venv)$ pip install -e .                     # Install handroll in editable mode.
(venv)$ py.test                              # Run the test suite.
```

[pypishield]: https://img.shields.io/pypi/v/handroll.svg
[license]: https://img.shields.io/pypi/l/handroll.svg
[travis]: https://travis-ci.org/handroll/handroll.png?branch=master
[coverage]: https://img.shields.io/codecov/c/github/handroll/handroll.svg

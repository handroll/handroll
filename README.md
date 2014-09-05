handroll
========

[![PyPI version][fury]](https://pypi.python.org/pypi/handroll)
[![Downloads][pypip]](https://warehouse.python.org/project/handroll/)
[![Build Status][travis]](https://travis-ci.org/mblayman/handroll)

Website development is a finely crafted art.

You need simple. You know what you're doing. You don't want to waste time.

`handroll` knows you are the boss. With one command, you gracefully blend your
theme and content into one precise result.

```bash
$ pip install handroll
...
Successfully installed handroll
$ handroll site
Complete.
```

Just the facts
--------------

`handroll` walks your website source (i.e. `site` as shown above), copying
everything that it can find. When it encounters:

1.  a template (either `template.html` or anything in `templates`), the file
    will be skipped.
2.  anything ending in `.md`, the file will be read, the first line of the file
    will become the `title`, and the remainder will be converted from Markdown
    into HTML to become the `content`. `title` and `content` will be combined
    with a template to produce the final HTML file.
3.  any other "known" extension will be handled by a corresponding composer.
    `handroll` works with Markdown, reStructuredText, and Textile out of the
    box.

Everything else
---------------

Check out [the feature
list](http://handroll.readthedocs.org/en/latest/#features) to see if handroll
meets your needs. If not, please tell us with a GitHub issue or on the mailing
list.

All the other stuff you may be interested in regarding `handroll` (e.g.,
writing a plugin for your favorite markup language) is found at [Read the
Docs](http://handroll.readthedocs.org/en/latest/).

If you want to share some ideas or find announcements, check out the [Google
Group](https://groups.google.com/forum/#!forum/handroll).

handroll is [BSD
licensed](https://github.com/mblayman/handroll/blob/master/LICENSE).

[fury]: https://badge.fury.io/py/handroll.png
[pypip]: https://pypip.in/d/handroll/badge.png
[travis]: https://travis-ci.org/mblayman/handroll.png?branch=master

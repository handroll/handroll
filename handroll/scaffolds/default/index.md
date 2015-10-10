---
title: Congratulations and welcome!
template: base.j2

---
This is your first handroll site! Congratulations.

You'll notice that things are a little sparse around here.
We think that your content is your own.
What we've included here is enough to get you on your feet
without burying you in details.

When you look around,
you'll find a `handroll.conf` configuration file,
a [Jinja](http://jinja.pocoo.org/) template,
a CSS file,
and a [Markdown](http://daringfireball.net/projects/markdown/) file
with the content of this page.
With these examples to guide you,
create some new content
or change the style!

If you aren't ready to begin,
that's ok.
Let's walk you through how to work
using handroll.

## Working with handroll

handroll has two main methods
of building your website.
handroll can build a site
by scanning over the source,
generating the content,
and then stopping.
Alternatively,
handroll can build a site
by watching the source directory
and building each piece of content
as it changes.

The more convenient way to work
is with the watcher.
When handroll is using the watcher,
the tool will also run a small web server.
This web server allows you to see your changes right away.
To play with this site
using the watcher, run:

```console
$ handroll -w mysite/source
```

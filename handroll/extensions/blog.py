# Copyright (c) 2015, Matt Layman

import os

try:
    import ConfigParser as configparser
except ImportError:  # pragma: no cover
    import configparser

from werkzeug.contrib.atom import AtomFeed, FeedEntry

from handroll.exceptions import AbortError
from handroll.extensions.base import Extension
from handroll.i18n import _


class BlogPost(object):

    def __init__(self, **kwargs):
        self.source_file = kwargs['source_file']
        self.title = kwargs['title']


class BlogExtension(Extension):
    """Track files marked as blog entries and generate a feed."""

    handle_frontmatter_loaded = True
    handle_pre_composition = True
    handle_post_composition = True

    required_metadata = {
        'author': 'atom_author',
        'id': 'atom_id',
        'title': 'atom_title',
        'url': 'atom_url',
    }

    def __init__(self, config):
        super(BlogExtension, self).__init__(config)
        self.posts = []
        self.atom_metadata = {}
        self.atom_output = ''

    def on_pre_composition(self, director):
        """Check that all the required configuration exists."""
        if not self._config.parser.has_section('blog'):
            raise AbortError(
                _('A blog section is missing in the configuration file.'))
        for metadata, option in self.required_metadata.items():
            self._add_atom_metadata(metadata, option)
        self.atom_output = self._get_option('atom_output')

    def on_frontmatter_loaded(self, source_file, frontmatter):
        """Scan for blog posts.

        If a post is found, record it.
        """
        is_post = frontmatter.get('blog', False)
        if type(is_post) != bool:
            raise AbortError(
                _('Invalid blog frontmatter (expects True or False): '
                  '{blog_value}').format(blog_value=is_post))
        if is_post:
            self.posts.append(BlogPost(
                source_file=source_file,
                title=frontmatter['title'],
            ))

    def on_post_composition(self, director):
        """Generate the atom feed."""
        builder = FeedBuilder(self.atom_metadata)
        for post in self.posts:
            builder.add(post)
        output_file = os.path.join(director.outdir, self.atom_output)
        builder.write_to(output_file)

    def _add_atom_metadata(self, name, option):
        """Add atom metadata from the config parser."""
        self.atom_metadata[name] = self._get_option(option)

    def _get_option(self, option):
        """Get an option out of the blog section."""
        try:
            return self._config.parser.get('blog', option)
        except configparser.NoOptionError:
            raise AbortError(
                _('The blog extension requires the {option} option.').format(
                    option=option))


class FeedBuilder(object):
    """Transform blog metadata and posts into an Atom feed."""

    def __init__(self, metadata):
        self.metadata = metadata
        self._feed = AtomFeed(**metadata)

    def add(self, post):
        """Add a blog post to the feed."""
        import datetime
        entry = FeedEntry(
            title=post.title,
            # TODO: Dynamically generate a URL.
            url='foo.html',
            # TODO: Get the date from the frontmatter.
            updated=datetime.datetime.now(),
        )
        self._feed.add(entry)

    def write_to(self, filepath):
        """Write the feed to the provided filepath."""
        with open(filepath, 'wb') as out:
            out.write(self._feed.to_string().encode('utf-8'))
            out.write(b'<!-- handrolled for excellence -->\n')

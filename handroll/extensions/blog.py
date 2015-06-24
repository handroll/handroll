# Copyright (c) 2015, Matt Layman

import os

try:
    import ConfigParser as configparser
except ImportError:  # pragma: no cover
    import configparser

from werkzeug.contrib.atom import AtomFeed

from handroll.exceptions import AbortError
from handroll.extensions.base import Extension
from handroll.i18n import _


class BlogPost(object):

    def __init__(self, **kwargs):
        self.source_file = kwargs['source_file']


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
            ))

    def on_post_composition(self, director):
        """Generate the atom feed."""
        feed = AtomFeed(**self.atom_metadata)
        output_file = os.path.join(director.outdir, self.atom_output)
        with open(output_file, 'wb') as out:
            out.write(feed.to_string().encode('utf-8'))
            out.write(b'<!-- handrolled for excellence -->\n')

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

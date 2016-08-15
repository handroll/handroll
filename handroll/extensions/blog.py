# Copyright (c) 2016, Matt Layman

import os

try:
    import ConfigParser as configparser
except ImportError:  # pragma: no cover
    import configparser

import smartypants
from werkzeug.contrib.atom import AtomFeed, FeedEntry

from handroll import logger
from handroll.exceptions import AbortError
from handroll.extensions.base import Extension
from handroll.i18n import _


class BlogPost(object):

    def __init__(self, **kwargs):
        self.date = kwargs['date']
        self.source_file = kwargs['source_file']
        self.summary = kwargs['summary']
        self.title = kwargs['title']
        self.route = kwargs['route']
        self.url = kwargs['url']

    def __eq__(self, other):
        if other is None:
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


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
        self.posts = {}
        self.atom_metadata = {}
        self.atom_output = ''
        self.list_template = None
        self.list_output = None
        self._resolver = None
        self._should_generate = True

    def on_pre_composition(self, director):
        """Check that all the required configuration exists."""
        if not self._config.parser.has_section('blog'):
            raise AbortError(
                _('A blog section is missing in the configuration file.'))

        # Collect atom feed configuration.
        for metadata, option in self.required_metadata.items():
            self._add_atom_metadata(metadata, option)
        self.atom_output = self._get_option('atom_output')

        # Collect HTML listing configuration.
        if self._config.parser.has_option('blog', 'list_template'):
            self.list_template = self._get_option('list_template')
            self.list_output = self._get_option('list_output')

        # Grab the resolver from the director for determining URLs for posts.
        self._resolver = director.resolver

    def on_frontmatter_loaded(self, source_file, frontmatter):
        """Record any new blog posts."""
        if not self._is_post(frontmatter):
            return
        self._validate_post(source_file, frontmatter)
        post = BlogPost(
            date=frontmatter['date'],
            source_file=source_file,
            summary=frontmatter.get('summary'),
            title=frontmatter['title'],
            route=self._resolver.as_route(source_file),
            url=self._resolver.as_url(source_file),
        )
        if post != self.posts.get(source_file):
            self.posts[source_file] = post
            self._should_generate = True

    def on_post_composition(self, director):
        """Generate blog output."""
        if not self._should_generate:
            return
        blog_posts = sorted(
            self.posts.values(), key=lambda p: p.date, reverse=True)
        self._generate_atom_feed(director, blog_posts)
        if self.list_template is not None:
            self._generate_list_page(director, blog_posts)
        self._should_generate = False

    def _is_post(self, frontmatter):
        """Check if the front matter looks like a blog post."""
        is_post = frontmatter.get('blog', False)
        if type(is_post) != bool:
            raise AbortError(
                _('Invalid blog frontmatter (expects True or False): '
                  '{blog_value}').format(blog_value=is_post))
        return is_post

    def _validate_post(self, source_file, frontmatter):
        """Validate that the post contains all the required fields."""
        required = set([
            'date',
            'title',
        ])
        fields = set(frontmatter.keys())
        missing = required - fields
        if missing:
            raise AbortError(_(
                'The blog post, {filename}, '
                'is missing required fields: {missing_fields}'.format(
                    filename=source_file, missing_fields=', '.join(missing))))

    def _generate_atom_feed(self, director, blog_posts):
        """Generate the atom feed."""
        logger.info(_('Generating Atom XML feed ...'))
        builder = FeedBuilder(self.atom_metadata)
        builder.add(blog_posts)
        output_file = os.path.join(director.outdir, self.atom_output)
        builder.write_to(output_file)

    def _generate_list_page(self, director, blog_posts):
        """Generate the list page."""
        logger.info(_('Generating blog list page ...'))
        template = director.catalog.get_template(self.list_template)
        builder = ListPageBuilder(template)
        builder.add(blog_posts)
        output_file = os.path.join(director.outdir, self.list_output)
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


class BlogBuilder(object):
    """A template pattern class for generating output related to a blog."""

    def _generate_output(self):
        """Generate output that belongs in the destination file.

        Subclasses must implement this method.
        """
        raise NotImplementedError()

    def write_to(self, filepath):
        """Write the output to the provided filepath."""
        output = self._generate_output()
        with open(filepath, 'wb') as out:
            out.write(output.encode('utf-8'))
            out.write(b'<!-- handrolled for excellence -->\n')


class FeedBuilder(BlogBuilder):
    """Transform blog metadata and posts into an Atom feed."""

    def __init__(self, metadata):
        self.metadata = metadata
        self._feed = AtomFeed(**metadata)

    def add(self, posts):
        """Add blog posts to the feed."""
        for post in posts:
            self._feed.add(FeedEntry(
                summary=post.summary,
                title=post.title,
                title_type='html',
                url=post.url,
                updated=post.date,
            ))

    def _generate_output(self):
        return self._feed.to_string()


class ListPageBuilder(BlogBuilder):
    """Transform blog posts into a list page."""

    def __init__(self, template):
        self._template = template
        self._blog_list = ''
        self._posts = None

    def add(self, posts):
        """Add the posts and generate a blog list."""
        li_html = []
        for post in posts:
            # Put the smartified title back into the post.
            post.title = title = smartypants.smartypants(post.title)
            li_html.append(
                u'<li><a href="{route}">{title}</a></li>'.format(
                    route=post.route, title=title))
        self._blog_list = u'\n'.join(li_html)
        self._posts = posts

    def _generate_output(self):
        context = {
            'blog_list': self._blog_list,
            'posts': self._posts,
        }
        return self._template.render(context)

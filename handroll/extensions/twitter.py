# Copyright (c) 2017, Matt Layman

from handroll.exceptions import AbortError
from handroll.extensions.base import Extension
from handroll.i18n import _
from handroll.resolver import URLResolver


class TwitterExtension(Extension):
    """Inject Twitter metadata into the template context."""

    handle_frontmatter_loaded = True
    handle_pre_composition = True

    def on_pre_composition(self, director):
        if not self._config.parser.has_section('twitter'):
            raise AbortError(_(
                'An twitter section is missing in the configuration file.'))

        if not self._config.parser.has_option('twitter', 'default_image'):
            raise AbortError(_(
                'A default image URL is missing in the configuration file.'))

        if not self._config.parser.has_option('twitter', 'site_username'):
            raise AbortError(_(
                'A site username is missing in the configuration file.'))

        self._resolver = director.resolver
        self._url_resolver = URLResolver(
            self._config,
            self._config.parser.get('twitter', 'default_image'))
        self._site = self._config.parser.get('twitter', 'site_username')

    def on_frontmatter_loaded(self, source_file, frontmatter):
        if frontmatter.get('blog'):
            self.add_metadata(source_file, frontmatter)
        else:
            frontmatter['twitter_metadata'] = ''

    def add_metadata(self, source_file, frontmatter):
        metadata = [
            '<meta name="twitter:card" content="summary" />',
            '<meta name="twitter:site" content="{}" />'.format(self._site),
        ]

        url = self._resolver.as_url(source_file)
        image = self._url_resolver.resolve(url, frontmatter.get('image'))
        metadata.append(
            u'<meta name="twitter:image" content="{}" />'.format(image))

        title = frontmatter.get('title', '')
        title = title.replace('"', '\'')
        metadata.append(
            u'<meta name="twitter:title" content="{}" />'.format(title))

        if frontmatter.get('summary'):
            summary = frontmatter.get('summary', '')
            summary = summary.replace('"', '\'')
            metadata.append(
                u'<meta name="twitter:description" content="{}" />'.format(
                    summary))

        frontmatter['twitter_metadata'] = '\n'.join(metadata)

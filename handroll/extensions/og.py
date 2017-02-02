# Copyright (c) 2017, Matt Layman

from handroll.exceptions import AbortError
from handroll.extensions.base import Extension
from handroll.i18n import _


class OpenGraphExtension(Extension):
    """Inject Open Graph metadata into the template context."""

    handle_frontmatter_loaded = True
    handle_pre_composition = True

    def on_pre_composition(self, director):
        if not self._config.parser.has_section('open_graph'):
            raise AbortError(_(
                'An open_graph section is missing in the configuration file.'))

        if not self._config.parser.has_option('open_graph', 'default_image'):
            raise AbortError(_(
                'A default image URL is missing in the configuration file.'))

        self._resolver = director.resolver

    def on_frontmatter_loaded(self, source_file, frontmatter):
        if frontmatter.get('blog'):
            self.add_blog_metadata(source_file, frontmatter)
        else:
            frontmatter['open_graph_metadata'] = ''

    def add_blog_metadata(self, source_file, frontmatter):
        url = self._resolver.as_url(source_file)
        metadata = [
            '<meta property="og:type" content="article" />',
            '<meta property="og:url" content="{}" />'.format(url),
        ]

        image = self.get_image_path(url, frontmatter)
        metadata.append(
            u'<meta property="og:image" content="{}" />'.format(image))

        title = frontmatter.get('title', '')
        title = title.replace('"', '\'')
        metadata.append(
            u'<meta property="og:title" content="{}" />'.format(title))

        if frontmatter.get('summary'):
            summary = frontmatter.get('summary', '')
            summary = summary.replace('"', '\'')
            metadata.append(
                u'<meta property="og:description" content="{}" />'.format(
                    summary))

        frontmatter['open_graph_metadata'] = '\n'.join(metadata)

    def get_image_path(self, url, frontmatter):
        image_path = frontmatter.get('image')
        if image_path:
            if image_path.startswith('/'):
                return self._config.domain + image_path
            else:
                url_parts = url.split('/')
                url_parts[-1] = image_path
                return '/'.join(url_parts)
        return self._config.parser.get('open_graph', 'default_image')

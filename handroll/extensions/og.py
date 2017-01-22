# Copyright (c) 2017, Matt Layman

from handroll.extensions.base import Extension


class OpenGraphExtension(Extension):
    """Inject Open Graph metadata into the template context."""

    handle_frontmatter_loaded = True
    handle_pre_composition = True

    def on_pre_composition(self, director):
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
            '<meta property="og:image" content="" />',
        ]
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

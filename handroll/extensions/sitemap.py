# Copyright (c) 2016, Matt Layman

import os

from handroll.extensions.base import Extension


class SitemapExtension(Extension):
    """Generate a sitemap from the HTML pages of the site."""

    handle_frontmatter_loaded = True
    handle_pre_composition = True
    handle_post_composition = True

    def __init__(self, config):
        super(SitemapExtension, self).__init__(config)
        self.urls = set()
        self._composers = None
        self._resolver = None

    def on_pre_composition(self, director):
        self._resolver = director.resolver
        self._composers = director.composers

    def on_frontmatter_loaded(self, source_file, frontmatter):
        composer = self._composers.select_composer_for(source_file)
        if composer.output_extension == '.html':
            self.urls.add(self._resolver.as_url(source_file))

    def on_post_composition(self, director):
        sitemap_path = os.path.join(director.outdir, 'sitemap.txt')
        with open(sitemap_path, 'w') as sitemap:
            for url in sorted(self.urls):
                sitemap.write(url + '\n')

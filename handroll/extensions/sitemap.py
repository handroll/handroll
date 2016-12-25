# Copyright (c) 2016, Matt Layman

import os

from handroll import logger
from handroll.extensions.base import Extension
from handroll.i18n import _


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
        # Assume that the sitemap needs to be generated at startup.
        self._dirty = True

    def on_pre_composition(self, director):
        self._composers = director.composers
        self._resolver = director.resolver

    def on_frontmatter_loaded(self, source_file, frontmatter):
        composer = self._composers.select_composer_for(source_file)
        if composer.get_output_extension(source_file) == '.html':
            url = self._resolver.as_url(source_file)
            if url not in self.urls:
                self.urls.add(url)
                self._dirty = True

    def on_post_composition(self, director):
        if not self._dirty:
            return
        logger.info(_('Generating sitemap ...'))
        sitemap_path = os.path.join(director.outdir, 'sitemap.txt')
        with open(sitemap_path, 'w') as sitemap:
            for url in sorted(self.urls):
                sitemap.write(url + '\n')
        self._dirty = False

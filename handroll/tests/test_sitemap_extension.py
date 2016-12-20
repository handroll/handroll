# Copyright (c) 2016, Matt Layman

import os

from handroll import signals
from handroll.extensions.sitemap import SitemapExtension
from handroll.tests import TestCase


class TestSitemapExtention(TestCase):

    def tearDown(self):
        super(TestSitemapExtention, self).tearDown()
        # Clean up any attached extension instance.
        signals.frontmatter_loaded.receivers.clear()
        signals.pre_composition.receivers.clear()
        signals.post_composition.receivers.clear()

    def _make_one(self, director):
        director.config.parser.add_section('sitemap')
        extension = SitemapExtension(director.config)
        extension.on_pre_composition(director)
        return extension

    def test_handles_frontmatter_loaded(self):
        extension = SitemapExtension(None)
        self.assertTrue(extension.handle_frontmatter_loaded)

    def test_handles_pre_composition(self):
        extension = SitemapExtension(None)
        self.assertTrue(extension.handle_pre_composition)

    def test_handles_post_composition(self):
        extension = SitemapExtension(None)
        self.assertTrue(extension.handle_post_composition)

    def test_records_html_url(self):
        director = self.factory.make_director()
        extension = self._make_one(director)
        extension._dirty = False
        path = os.path.join(director.site.path, 'path/to/sample.md')
        extension.on_frontmatter_loaded(path, {})
        self.assertIn(
            'http://www.example.com/path/to/sample.html', extension.urls)
        self.assertTrue(extension._dirty)

    def test_ignores_non_html_url(self):
        director = self.factory.make_director()
        extension = self._make_one(director)
        path = os.path.join(director.site.path, 'path/to/sample.png')
        extension.on_frontmatter_loaded(path, {})
        self.assertFalse(extension.urls)

    def test_generates_sitemap_output(self):
        director = self.factory.make_director()
        os.mkdir(director.outdir)
        extension = self._make_one(director)
        path_a = os.path.join(director.site.path, 'path/to/a.md')
        path_b = os.path.join(director.site.path, 'path/to/b.md')
        extension.on_frontmatter_loaded(path_b, {})
        extension.on_frontmatter_loaded(path_a, {})
        extension.on_post_composition(director)
        content = open(os.path.join(director.outdir, 'sitemap.txt')).read()
        self.assertEqual(
            'http://www.example.com/path/to/a.html\n'
            'http://www.example.com/path/to/b.html\n',
            content)
        self.assertFalse(extension._dirty)

    def test_not_dirty_when_url_already_recorded(self):
        director = self.factory.make_director()
        extension = self._make_one(director)
        path_a = os.path.join(director.site.path, 'path/to/a.md')
        extension.on_frontmatter_loaded(path_a, {})
        extension._dirty = False
        extension.on_frontmatter_loaded(path_a, {})
        self.assertFalse(extension._dirty)

    def test_no_sitemap_when_not_dirty(self):
        director = self.factory.make_director()
        os.mkdir(director.outdir)
        extension = self._make_one(director)
        extension._dirty = False
        extension.on_post_composition(director)
        self.assertFalse(
            os.path.exists(os.path.join(director.outdir, 'sitemap.txt')))

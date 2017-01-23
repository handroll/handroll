# Copyright (c) 2017, Matt Layman

import os

from handroll import signals
from handroll.exceptions import AbortError
from handroll.extensions.og import OpenGraphExtension
from handroll.tests import TestCase


class TestOpenGraphExtension(TestCase):

    def tearDown(self):
        super(TestOpenGraphExtension, self).tearDown()
        # Clean up any attached extension instance.
        signals.frontmatter_loaded.receivers.clear()
        signals.pre_composition.receivers.clear()

    def _make_one(self, director):
        director.config.parser.add_section('open_graph')
        extension = OpenGraphExtension(director.config)
        extension.on_pre_composition(director)
        return extension

    def test_handles_frontmatter_loaded(self):
        extension = OpenGraphExtension(None)
        self.assertTrue(extension.handle_frontmatter_loaded)

    def test_handles_pre_composition(self):
        extension = OpenGraphExtension(None)
        self.assertTrue(extension.handle_pre_composition)

    def test_no_open_graph_data(self):
        extension = OpenGraphExtension(None)
        frontmatter = {}
        extension.on_frontmatter_loaded('page.md', frontmatter)
        self.assertEqual('', frontmatter['open_graph_metadata'])

    def test_blog_entry(self):
        director = self.factory.make_director()
        extension = self._make_one(director)
        frontmatter = {
            'blog': True,
            'title': 'A blog post',
            'summary': 'The summary',
        }
        path = os.path.join(director.site.path, 'post.md')
        extension.on_frontmatter_loaded(path, frontmatter)
        self.assertEqual(
            '<meta property="og:type" content="article" />\n'
            '<meta property="og:url" '
            'content="http://www.example.com/post.html" />\n'
            '<meta property="og:image" content="" />\n'
            '<meta property="og:title" content="A blog post" />\n'
            '<meta property="og:description" content="The summary" />',
            frontmatter['open_graph_metadata'])

    def test_convert_title_double_to_single_quotes(self):
        director = self.factory.make_director()
        extension = self._make_one(director)
        frontmatter = {
            'blog': True,
            'title': 'A "quoted" blog post',
            'summary': 'The summary',
        }
        extension.on_frontmatter_loaded('path.md', frontmatter)
        self.assertIn(
            '<meta property="og:title" content="A \'quoted\' blog post" />',
            frontmatter['open_graph_metadata'])

    def test_convert_summary_double_to_single_quotes(self):
        director = self.factory.make_director()
        extension = self._make_one(director)
        frontmatter = {
            'blog': True,
            'title': 'A "quoted" blog post',
            'summary': 'The "summary"',
        }
        extension.on_frontmatter_loaded('path.md', frontmatter)
        self.assertIn(
            '<meta property="og:description" content="The \'summary\'" />',
            frontmatter['open_graph_metadata'])

    def test_has_open_graph_section(self):
        director = self.factory.make_director()
        extension = OpenGraphExtension(director.config)
        with self.assertRaises(AbortError):
            extension.on_pre_composition(director)

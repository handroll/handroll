# Copyright (c) 2017, Matt Layman

import os

from handroll import signals
from handroll.exceptions import AbortError
from handroll.extensions.twitter import TwitterExtension
from handroll.tests import TestCase


class TestTwitterExtension(TestCase):

    def tearDown(self):
        super(TestTwitterExtension, self).tearDown()
        # Clean up any attached extension instance.
        signals.frontmatter_loaded.receivers.clear()
        signals.pre_composition.receivers.clear()

    def _make_one(self, director):
        director.config.parser.add_section('twitter')
        director.config.parser.set(
            'twitter', 'default_image',
            'http://www.example.com/images/twitter.png')
        director.config.parser.set('twitter', 'site_username', '@mblayman')
        extension = TwitterExtension(director.config)
        extension.on_pre_composition(director)
        return extension

    def test_handles_frontmatter_loaded(self):
        extension = TwitterExtension(None)
        self.assertTrue(extension.handle_frontmatter_loaded)

    def test_handles_pre_composition(self):
        extension = TwitterExtension(None)
        self.assertTrue(extension.handle_pre_composition)

    def test_no_twitter_data(self):
        extension = TwitterExtension(None)
        frontmatter = {}
        extension.on_frontmatter_loaded('page.md', frontmatter)
        self.assertEqual('', frontmatter['twitter_metadata'])

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
            '<meta name="twitter:card" content="summary" />\n'
            '<meta name="twitter:site" content="@mblayman" />\n'
            '<meta name="twitter:image" '
            'content="http://www.example.com/images/twitter.png" />\n'
            '<meta name="twitter:title" content="A blog post" />\n'
            '<meta name="twitter:description" content="The summary" />',
            frontmatter['twitter_metadata'])

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
            '<meta name="twitter:title" content="A \'quoted\' blog post" />',
            frontmatter['twitter_metadata'])

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
            '<meta name="twitter:description" content="The \'summary\'" />',
            frontmatter['twitter_metadata'])

    def test_has_twitter_section(self):
        director = self.factory.make_director()
        extension = TwitterExtension(director.config)
        with self.assertRaises(AbortError):
            extension.on_pre_composition(director)

    def test_default_image_required(self):
        director = self.factory.make_director()
        extension = self._make_one(director)
        director.config.parser.remove_option('twitter', 'default_image')
        with self.assertRaises(AbortError):
            extension.on_pre_composition(director)

    def test_site_username_required(self):
        director = self.factory.make_director()
        extension = self._make_one(director)
        director.config.parser.remove_option('twitter', 'site_username')
        with self.assertRaises(AbortError):
            extension.on_pre_composition(director)

# Copyright (c) 2015, Matt Layman

import mock

from handroll import signals
from handroll.extensions.base import Extension
from handroll.extensions.blog import BlogExtension
from handroll.extensions.loader import ExtensionLoader
from handroll.tests import TestCase


class TestExtensionLoader(TestCase):

    def test_loads_available_extensions(self):
        loader = ExtensionLoader()
        loader.load()
        self.assertEqual(BlogExtension, loader._available_extensions['blog'])


class TestExtension(TestCase):

    @mock.patch('handroll.extensions.base.signals.frontmatter_loaded')
    def test_frontmatter_loaded_connection_default(self, frontmatter_loaded):
        Extension()
        self.assertFalse(frontmatter_loaded.connect.called)

    def test_connects_to_frontmatter_loaded(self):
        Extension.handle_frontmatter_loaded = True
        Extension()
        self.assertRaises(
            NotImplementedError, signals.frontmatter_loaded.send,
            'a_source_file', frontmatter={})
        Extension.handle_frontmatter_loaded = False

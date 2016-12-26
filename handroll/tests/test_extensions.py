# Copyright (c) 2016, Matt Layman

import mock

from handroll import signals
from handroll.configuration import Configuration
from handroll.extensions.base import Extension
from handroll.extensions.blog import BlogExtension
from handroll.extensions.loader import ExtensionLoader
from handroll.tests import TestCase


class TestExtensionLoader(TestCase):

    def tearDown(self):
        super(TestExtensionLoader, self).tearDown()
        # Clean up any attached extension instance.
        signals.frontmatter_loaded.receivers.clear()
        signals.pre_composition.receivers.clear()
        signals.post_composition.receivers.clear()

    def test_loads_available_extensions(self):
        loader = ExtensionLoader()
        loader.load()
        self.assertEqual(BlogExtension, loader._available_extensions['blog'])

    def test_gets_active_extensions(self):
        config = Configuration()
        config.active_extensions.add('blog')
        loader = ExtensionLoader()
        loader.load()

        extensions = loader.get_active_extensions(config)

        self.assertEqual(1, len(extensions))
        self.assertTrue(isinstance(extensions[0], BlogExtension))


class TestExtension(TestCase):

    @mock.patch('handroll.extensions.base.signals.frontmatter_loaded')
    def test_frontmatter_loaded_connection_default(self, frontmatter_loaded):
        Extension(None)
        self.assertFalse(frontmatter_loaded.connect.called)

    def test_connects_to_frontmatter_loaded(self):
        class FrontmatterLoader(Extension):
            handle_frontmatter_loaded = True
        extension = FrontmatterLoader(None)
        self.assertTrue(extension.handle_frontmatter_loaded)
        with self.assertRaises(NotImplementedError):
            signals.frontmatter_loaded.send('a_source_file', frontmatter={})
        signals.frontmatter_loaded.receivers.clear()

    @mock.patch('handroll.extensions.base.signals.post_composition')
    def test_post_composition_connection_default(self, post_composition):
        Extension(None)
        self.assertFalse(post_composition.connect.called)

    def test_connects_to_post_composition(self):
        class PostComposer(Extension):
            handle_post_composition = True
        director = mock.Mock()
        extension = PostComposer(None)
        self.assertTrue(extension.handle_post_composition)
        with self.assertRaises(NotImplementedError):
            signals.post_composition.send(director)
        signals.post_composition.receivers.clear()

    @mock.patch('handroll.extensions.base.signals.pre_composition')
    def test_pre_composition_connection_default(self, pre_composition):
        Extension(None)
        self.assertFalse(pre_composition.connect.called)

    def test_connects_to_pre_composition(self):
        class PreComposer(Extension):
            handle_pre_composition = True
        director = mock.Mock()
        extension = PreComposer(None)
        self.assertTrue(extension.handle_pre_composition)
        with self.assertRaises(NotImplementedError):
            signals.pre_composition.send(director)
        signals.pre_composition.receivers.clear()

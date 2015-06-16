# Copyright (c) 2015, Matt Layman

import mock

from handroll import signals
from handroll.configuration import Configuration
from handroll.exceptions import AbortError
from handroll.extensions.base import Extension
from handroll.extensions.blog import BlogExtension
from handroll.extensions.loader import ExtensionLoader
from handroll.tests import TestCase


class TestExtensionLoader(TestCase):

    def tearDown(self):
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
        self.assertRaises(
            NotImplementedError, signals.frontmatter_loaded.send,
            'a_source_file', frontmatter={})
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
        self.assertRaises(
            NotImplementedError, signals.post_composition.send, director)
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
        self.assertRaises(
            NotImplementedError, signals.pre_composition.send, director)
        signals.pre_composition.receivers.clear()


class TestBlogExtension(TestCase):

    def tearDown(self):
        # Clean up any attached extension instance.
        signals.frontmatter_loaded.receivers.clear()
        signals.pre_composition.receivers.clear()
        signals.post_composition.receivers.clear()

    def _add_blog_section(self, parser, exclude=None):
        parser.add_section('blog')
        metadata = {
            'atom_author': 'Nikola Tesla',
            'atom_id': 'https://www.example.com/feed.xml',
            'atom_title': 'Amazing blog',
            'atom_url': 'https://www.example.com/archive.html',
        }
        for option, value in metadata.items():
            if option == exclude:
                continue
            parser.set('blog', option, value)

    def test_handles_frontmatter_loaded(self):
        extension = BlogExtension(None)
        self.assertTrue(extension.handle_frontmatter_loaded)

    def test_handles_post_composition(self):
        extension = BlogExtension(None)
        self.assertTrue(extension.handle_post_composition)

    def test_registers_blog_post(self):
        extension = BlogExtension(None)
        extension.on_frontmatter_loaded('thundercats.md', {'blog': True})
        post = extension.posts[0]
        self.assertEqual('thundercats.md', post.source_file)

    def test_ignores_non_blog_post(self):
        extension = BlogExtension(None)
        extension.on_frontmatter_loaded('exosquad.md', {})
        self.assertEqual(0, len(extension.posts))

    def test_blog_must_be_boolean(self):
        extension = BlogExtension(None)
        self.assertRaises(
            AbortError, extension.on_frontmatter_loaded, 'animaniacs.md',
            {'blog': 'crazy'})

    def test_handles_pre_composition(self):
        extension = BlogExtension(None)
        self.assertTrue(extension.handle_pre_composition)

    def test_requires_blog_section(self):
        """A config with no blog section aborts."""
        director = self.factory.make_director()
        extension = BlogExtension(director.config)
        self.assertRaises(AbortError, extension.on_pre_composition, director)

    def test_requires_atom_title(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser, exclude='atom_title')
        extension = BlogExtension(director.config)
        try:
            extension.on_pre_composition(director)
            self.fail()
        except AbortError as ae:
            self.assertTrue('atom_title' in str(ae))

    def test_has_atom_title_in_metadata(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertEqual('Amazing blog', extension.atom_metadata['title'])

    def test_requires_atom_author(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser, exclude='atom_author')
        extension = BlogExtension(director.config)
        try:
            extension.on_pre_composition(director)
            self.fail()
        except AbortError as ae:
            self.assertTrue('atom_author' in str(ae))

    def test_has_atom_author_in_metadata(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertEqual('Nikola Tesla', extension.atom_metadata['author'])

    def test_requires_atom_id(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser, exclude='atom_id')
        extension = BlogExtension(director.config)
        try:
            extension.on_pre_composition(director)
            self.fail()
        except AbortError as ae:
            self.assertTrue('atom_id' in str(ae))

    def test_has_atom_id_in_metadata(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertEqual(
            'https://www.example.com/feed.xml', extension.atom_metadata['id'])

    def test_requires_atom_url(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser, exclude='atom_url')
        extension = BlogExtension(director.config)
        try:
            extension.on_pre_composition(director)
            self.fail()
        except AbortError as ae:
            self.assertTrue('atom_url' in str(ae))

    def test_has_atom_url_in_metadata(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertEqual(
            'https://www.example.com/archive.html',
            extension.atom_metadata['url'])

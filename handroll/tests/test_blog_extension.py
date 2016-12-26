# Copyright (c) 2016, Matt Layman

import datetime
import os

import mock

from handroll import signals
from handroll.exceptions import AbortError
from handroll.extensions.blog import (
    BlogExtension, BlogBuilder, FeedBuilder, ListPageBuilder)
from handroll.resolver import FileResolver
from handroll.tests import TestCase


class TestBlogExtension(TestCase):

    def tearDown(self):
        super(TestBlogExtension, self).tearDown()
        # Clean up any attached extension instance.
        signals.frontmatter_loaded.receivers.clear()
        signals.pre_composition.receivers.clear()
        signals.post_composition.receivers.clear()

    def _add_blog_section(self, parser, exclude=None):
        parser.add_section('blog')
        configuration = {
            'atom_author': 'Nikola Tesla',
            'atom_id': 'https://www.example.com/feed.xml',
            'atom_output': 'feed.xml',
            'atom_title': 'Amazing blog',
            'atom_url': 'https://www.example.com/archive.html',
            'list_template': 'archive.j2',
            'list_output': 'archive.html',
        }
        for option, value in configuration.items():
            if option == exclude:
                continue
            parser.set('blog', option, value)

    def _make_preprocessed_one(self, director=None, exclude=None):
        """Make an instance that has all default metadata already parsed."""
        if director is None:
            director = self.factory.make_director()
        self._add_blog_section(director.config.parser, exclude=exclude)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        templates = os.path.join(director.site.path, 'templates')
        os.mkdir(templates)
        open(os.path.join(templates, 'archive.j2'), 'w').close()
        return extension

    def _make_blog_post_frontmatter(self):
        frontmatter = {
            'blog': True,
            'date': datetime.datetime(2015, 6, 25, 12, 0, 0),
            'title': 'A Blog Post',
        }
        return frontmatter

    def test_handles_frontmatter_loaded(self):
        extension = BlogExtension(None)
        self.assertTrue(extension.handle_frontmatter_loaded)

    def test_handles_post_composition(self):
        extension = BlogExtension(None)
        self.assertTrue(extension.handle_post_composition)

    def test_registers_blog_post(self):
        extension = self._make_preprocessed_one()
        frontmatter = self._make_blog_post_frontmatter()
        extension.on_frontmatter_loaded('thundercats.md', frontmatter)
        post = extension.posts['thundercats.md']
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
        with self.assertRaises(AbortError) as error:
            extension.on_pre_composition(director)
        self.assertTrue('atom_title' in str(error.exception))

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
        with self.assertRaises(AbortError) as error:
            extension.on_pre_composition(director)
        self.assertTrue('atom_author' in str(error.exception))

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
        with self.assertRaises(AbortError) as error:
            extension.on_pre_composition(director)
        self.assertTrue('atom_id' in str(error.exception))

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
        with self.assertRaises(AbortError) as error:
            extension.on_pre_composition(director)
        self.assertTrue('atom_url' in str(error.exception))

    def test_has_atom_url_in_metadata(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertEqual(
            'https://www.example.com/archive.html',
            extension.atom_metadata['url'])

    def test_requires_atom_output(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser, exclude='atom_output')
        extension = BlogExtension(director.config)
        with self.assertRaises(AbortError) as error:
            extension.on_pre_composition(director)
        self.assertTrue('atom_output' in str(error.exception))

    def test_has_atom_output_in_metadata(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertEqual('feed.xml', extension.atom_output)

    def test_post_composition_generates_feed(self):
        director = self.factory.make_director()
        os.mkdir(director.outdir)
        extension = self._make_preprocessed_one(director)
        extension.on_post_composition(director)
        feed = os.path.join(director.outdir, extension.atom_output)
        self.assertTrue(os.path.exists(feed))

    @mock.patch.object(FeedBuilder, 'add')
    def test_adds_post(self, builder_add):
        director = self.factory.make_director()
        os.mkdir(director.outdir)
        extension = self._make_preprocessed_one(director)
        post = self.factory.make_blog_post()
        extension.posts[post.source_file] = post
        extension.on_post_composition(director)
        received_post = builder_add.call_args[0][0][0]
        self.assertEqual(post, received_post)

    def test_date_in_post(self):
        extension = self._make_preprocessed_one()
        frontmatter = self._make_blog_post_frontmatter()
        extension.on_frontmatter_loaded('thundercats.md', frontmatter)
        post = extension.posts['thundercats.md']
        expected_date = datetime.date(2015, 6, 25)
        self.assertEqual(expected_date, post.date.date())

    def test_obtains_resolver(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertTrue(isinstance(extension._resolver, FileResolver))

    @mock.patch.object(FeedBuilder, 'add')
    def test_posts_added_to_builder_by_date(self, builder_add):
        current = self.factory.make_blog_post()
        current.source_file = 'current.md'
        older = self.factory.make_blog_post()
        older.source_file = 'older.md'
        older.date = older.date - datetime.timedelta(days=-1)
        director = self.factory.make_director()
        extension = self._make_preprocessed_one(director=director)
        extension.posts['current.md'] = current
        extension.posts['older.md'] = older
        os.mkdir(director.outdir)
        extension.on_post_composition(director)
        posts = builder_add.call_args[0][0]
        self.assertEqual(older, posts[0])
        self.assertEqual(current, posts[1])

    def test_list_template_not_required(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser, exclude='list_template')
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertIsNone(extension.list_template)

    def test_has_list_template_in_extension(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertEqual('archive.j2', extension.list_template)

    def test_has_list_output_in_extension(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        extension.on_pre_composition(director)
        self.assertEqual('archive.html', extension.list_output)

    def test_list_output_required_with_list_template(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser, exclude='list_output')
        extension = BlogExtension(director.config)
        with self.assertRaises(AbortError) as error:
            extension.on_pre_composition(director)
        self.assertTrue('list_output' in str(error.exception))

    @mock.patch.object(ListPageBuilder, 'write_to')
    def test_builds_list_page(self, write_to):
        director = self.factory.make_director()
        os.mkdir(director.outdir)
        extension = self._make_preprocessed_one(director=director)
        extension.on_post_composition(director)
        expected_output = os.path.join(director.outdir, 'archive.html')
        write_to.assert_called_once_with(expected_output)

    @mock.patch.object(ListPageBuilder, 'write_to')
    def test_skip_list_page_building_when_no_template_exists(self, write_to):
        director = self.factory.make_director()
        os.mkdir(director.outdir)
        extension = self._make_preprocessed_one(
            director=director, exclude='list_template')
        extension.on_post_composition(director)
        self.assertFalse(write_to.called)

    def test_should_generate_output_at_start(self):
        director = self.factory.make_director()
        self._add_blog_section(director.config.parser)
        extension = BlogExtension(director.config)
        self.assertTrue(extension._should_generate)

    def test_post_composition_signals_stop_generation(self):
        director = self.factory.make_director()
        os.mkdir(director.outdir)
        extension = self._make_preprocessed_one(director=director)
        extension.on_post_composition(director)
        self.assertFalse(extension._should_generate)

    @mock.patch.object(ListPageBuilder, 'write_to')
    def test_does_not_generate(self, write_to):
        director = self.factory.make_director()
        os.mkdir(director.outdir)
        extension = self._make_preprocessed_one(director=director)
        extension._should_generate = False
        extension.on_post_composition(director)
        self.assertFalse(write_to.called)

    def test_new_post_triggers_need_for_generation(self):
        extension = self._make_preprocessed_one()
        extension._should_generate = False
        frontmatter = self._make_blog_post_frontmatter()
        extension.on_frontmatter_loaded('thundercats.md', frontmatter)
        self.assertTrue(extension._should_generate)

    def test_same_post_does_not_signal_generation(self):
        extension = self._make_preprocessed_one()
        frontmatter = self._make_blog_post_frontmatter()
        extension.on_frontmatter_loaded('thundercats.md', frontmatter)
        extension._should_generate = False
        extension.on_frontmatter_loaded('thundercats.md', frontmatter)
        self.assertFalse(extension._should_generate)

    def test_post_requires_date(self):
        extension = self._make_preprocessed_one()
        frontmatter = self._make_blog_post_frontmatter()
        del frontmatter['date']
        with self.assertRaises(AbortError) as error:
            extension.on_frontmatter_loaded('thundercats.md', frontmatter)
        self.assertTrue('date' in str(error.exception))

    def test_post_requires_title(self):
        extension = self._make_preprocessed_one()
        frontmatter = self._make_blog_post_frontmatter()
        del frontmatter['title']
        with self.assertRaises(AbortError) as error:
            extension.on_frontmatter_loaded('thundercats.md', frontmatter)
        self.assertTrue('title' in str(error.exception))

    def test_post_requires_error_includes_post_filename(self):
        extension = self._make_preprocessed_one()
        frontmatter = self._make_blog_post_frontmatter()
        del frontmatter['title']
        with self.assertRaises(AbortError) as error:
            extension.on_frontmatter_loaded('thundercats.md', frontmatter)
        self.assertTrue('thundercats.md' in str(error.exception))


class TestBlogBuilder(TestCase):

    def test_generate_output_not_implemented(self):
        builder = BlogBuilder()
        with self.assertRaises(NotImplementedError):
            builder.write_to('doesnotmatter.html')


class TestFeedBuilder(TestCase):

    def _make_one(self):
        self.atom_metadata = {
            'id': 'http://www.example.com/feed.xml',
            'title': 'Awesome sauce',
        }
        return FeedBuilder(self.atom_metadata)

    def test_has_metadata(self):
        builder = self._make_one()
        self.assertEqual(self.atom_metadata, builder.metadata)

    def test_post_creates_feed_entry(self):
        builder = self._make_one()
        post = self.factory.make_blog_post()
        builder.add([post])
        self.assertEqual(1, len(builder._feed.entries))

    def test_feed_entry_has_post_url(self):
        builder = self._make_one()
        post = self.factory.make_blog_post()
        builder.add([post])
        self.assertEqual(post.url, builder._feed.entries[0].url)

    def test_feed_entry_has_summary(self):
        builder = self._make_one()
        post = self.factory.make_blog_post()
        builder.add([post])
        self.assertEqual(post.summary, builder._feed.entries[0].summary)

    def test_title_type_is_html(self):
        """The title type is HTML.

        The title frontmatter is automatically HTML escaped so the
        title type should be HTML to handle that escaped title.
        """
        builder = self._make_one()
        post = self.factory.make_blog_post()
        builder.add([post])
        self.assertEqual('html', builder._feed.entries[0].title_type)


class TestListPageBuilder(TestCase):

    def test_output_is_rendered(self):
        mock_template = mock.Mock()
        mock_template.render.return_value = 'fake HTML'
        builder = ListPageBuilder(mock_template)
        output = builder._generate_output()
        self.assertEqual('fake HTML', output)

    def test_blog_list_in_context(self):
        mock_template = mock.Mock()
        builder = ListPageBuilder(mock_template)
        builder._blog_list = 'fake li items'
        builder._generate_output()
        context = mock_template.render.call_args[0][0]
        self.assertEqual('fake li items', context['blog_list'])

    def test_adds_posts_to_blog_list_html(self):
        post = self.factory.make_blog_post()
        another = self.factory.make_blog_post()
        another.title = 'Another Blog Post'
        builder = ListPageBuilder(None)
        builder.add([post, another])
        self.assertEqual(
            '<li><a href="/a_source_file.html">A Blog Post</a></li>\n'
            '<li><a href="/a_source_file.html">Another Blog Post</a></li>',
            builder._blog_list)

    def test_smartypants_conversion_on_title(self):
        post = self.factory.make_blog_post()
        post.title = 'Emdash -- Post'
        builder = ListPageBuilder(None)
        builder.add([post])
        self.assertEqual(
            '<li><a href="/a_source_file.html">Emdash &#8212; Post</a></li>',
            builder._blog_list)

    def test_holds_posts(self):
        post = self.factory.make_blog_post()
        posts = [post]
        builder = ListPageBuilder(None)
        builder.add(posts)
        self.assertEqual(posts, builder._posts)

    def test_posts_in_context(self):
        mock_template = mock.Mock()
        builder = ListPageBuilder(mock_template)
        builder._posts = ['fake post']
        builder._generate_output()
        context = mock_template.render.call_args[0][0]
        self.assertEqual(['fake post'], context['posts'])

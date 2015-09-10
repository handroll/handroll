# Copyright (c) 2015, Matt Layman

import inspect
import os
import stat
import tempfile

import mock

from handroll.composers import Composer
from handroll.composers import Composers
from handroll.composers import CopyComposer
from handroll.composers.atom import AtomComposer
from handroll.composers.generic import GenericHTMLComposer
from handroll.composers.md import MarkdownComposer
from handroll.composers.rst import ReStructuredTextComposer
from handroll.composers.sass import SassComposer
from handroll.composers.txt import TextileComposer
from handroll.exceptions import AbortError
from handroll.tests import TestCase


class TestComposer(TestCase):

    def test_compose_not_implemented(self):
        composer = Composer()
        self.assertRaises(
            NotImplementedError, composer.compose, None, None, None)

    def test_output_extension_not_implemented(self):
        composer = Composer()
        self.assertRaises(
            NotImplementedError, lambda: composer.output_extension)


class TestComposers(TestCase):

    def _make_one(self):
        config = self.factory.make_configuration()
        return Composers(config)

    def test_selects_composer(self):
        composers = self._make_one()
        composer = composers.select_composer_for('sample.md')
        self.assertTrue(isinstance(composer, MarkdownComposer))

    def test_has_config(self):
        config = self.factory.make_configuration()
        composers = Composers(config)
        self.assertEqual(config, composers._config)


class TestAtomComposer(TestCase):

    def setUp(self):
        site = tempfile.mkdtemp()
        self.source_file = os.path.join(site, 'feed.atom')
        open(self.source_file, 'w').close()
        self.outdir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.outdir, 'feed.xml')

    def test_composes_feed(self):
        source = """{
            "title": "Fakity Fake",
            "id": "let's pretend this is unique",
            "entries": [{
                "title": "Sample A",
                "updated": "2014-02-23T00:00:00",
                "published": "2014-02-22T00:00:00",
                "url": "http://some.website.com/a.html",
                "summary": "A summary of the sample post"
            }]
        }"""
        with open(self.source_file, 'w') as f:
            f.write(source)
        composer = AtomComposer()
        composer.compose(None, self.source_file, self.outdir)
        self.assertTrue(os.path.exists(self.output_file))

    def test_must_have_entries(self):
        source = """{
            "title": "Fakity Fake",
            "id": "let's pretend this is unique"
        }"""
        with open(self.source_file, 'w') as f:
            f.write(source)
        composer = AtomComposer()
        self.assertRaises(
            AbortError, composer.compose, None, self.source_file, self.outdir)

    @mock.patch('handroll.composers.atom.json')
    def test_skips_up_to_date(self, json):
        open(self.output_file, 'w').close()
        composer = AtomComposer()
        composer.compose(None, self.source_file, self.outdir)
        self.assertFalse(json.loads.called)

    def test_output_extension(self):
        composer = AtomComposer()
        self.assertEqual('.xml', composer.output_extension)


class TestCopyComposer(TestCase):

    @mock.patch('handroll.composers.shutil')
    def test_skips_same_files(self, shutil):
        marker = 'marker.txt'
        source = tempfile.mkdtemp()
        source_file = os.path.join(source, marker)
        outdir = tempfile.mkdtemp()
        open(source_file, 'w').close()
        open(os.path.join(outdir, marker), 'w').close()
        composer = CopyComposer()
        composer.compose(None, source_file, outdir)
        self.assertFalse(shutil.copy.called)

    @mock.patch('handroll.composers.shutil')
    def test_copies_when_content_differs(self, shutil):
        marker = 'marker.txt'
        source = tempfile.mkdtemp()
        source_file = os.path.join(source, marker)
        outdir = tempfile.mkdtemp()
        open(source_file, 'w').close()
        with open(os.path.join(outdir, marker), 'w') as f:
            f.write('something different')
        composer = CopyComposer()
        composer.compose(None, source_file, outdir)
        self.assertTrue(shutil.copy.called)

    def test_output_extension(self):
        """The copy composer takes the extension of the source file.

        This composer is the fallback composer and resolution should
        never rely on this composer's output extension.
        """
        composer = CopyComposer()
        self.assertRaises(AttributeError, lambda: composer.output_extension)


class TestGenericHTMLComposer(TestCase):

    def test_composes_file(self):
        catalog = mock.MagicMock()
        site = tempfile.mkdtemp()
        source_file = os.path.join(site, 'sample.generic')
        open(source_file, 'w').close()
        outdir = ''
        composer = GenericHTMLComposer()
        self.assertRaises(
            NotImplementedError,
            composer.compose, catalog, source_file, outdir)

    def test_selects_default_template(self):
        catalog = mock.MagicMock()
        default = mock.PropertyMock()
        type(catalog).default = default
        composer = GenericHTMLComposer()
        composer.select_template(catalog, {})
        self.assertTrue(default.called)

    def test_selects_specified_template(self):
        catalog = mock.MagicMock()
        composer = GenericHTMLComposer()
        composer.select_template(catalog, {'template': 'base.j2'})
        catalog.get_template.assert_called_once_with('base.j2')

    def test_gets_frontmatter(self):
        source = inspect.cleandoc("""%YAML 1.1
        ---
        title: A Fake Title
        ---
        The Content
        """)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(source.encode('utf-8'))
        composer = GenericHTMLComposer()
        data, source = composer._get_data(f.name)
        self.assertEqual('A Fake Title', data['title'])
        self.assertEqual('The Content', source)

    @mock.patch('handroll.composers.generic.signals')
    def test_fires_frontmatter_loaded(self, signals):
        source = inspect.cleandoc("""%YAML 1.1
        ---
        title: A Fake Title
        ---
        The Content
        """)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(source.encode('utf-8'))
        composer = GenericHTMLComposer()
        data, source = composer._get_data(f.name)
        signals.frontmatter_loaded.send.assert_called_once_with(
            f.name, frontmatter={'title': 'A Fake Title'})

    def test_needs_update(self):
        site = tempfile.mkdtemp()
        output_file = os.path.join(site, 'output.md')
        open(output_file, 'w').close()
        future = os.path.getmtime(output_file) + 1
        source_file = os.path.join(site, 'test.md')
        open(source_file, 'w').close()
        os.utime(source_file, (future, future))
        template = mock.MagicMock()
        template.last_modified = future

        composer = GenericHTMLComposer()
        self.assertTrue(composer._needs_update(None, source_file, output_file))

        past = future - 10
        os.utime(source_file, (past, past))
        self.assertTrue(
            composer._needs_update(template, source_file, output_file))

        template.last_modified = past
        self.assertFalse(
            composer._needs_update(template, source_file, output_file))

    def test_output_extension(self):
        composer = GenericHTMLComposer()
        self.assertEqual('.html', composer.output_extension)


class TestMarkdownComposer(TestCase):

    def test_generates_html(self):
        source = '**bold**'
        composer = MarkdownComposer()
        html = composer._generate_content(source)
        self.assertEqual('<p><strong>bold</strong></p>', html)

    def test_composes_no_update(self):
        site = tempfile.mkdtemp()
        source_file = os.path.join(site, 'test.md')
        open(source_file, 'w').close()
        source_mtime = os.path.getmtime(source_file)
        future = source_mtime + 1
        outdir = tempfile.mkdtemp()
        output_file = os.path.join(outdir, 'test.html')
        open(output_file, 'w').close()
        os.utime(output_file, (future, future))
        template = mock.MagicMock()
        template.last_modified = source_mtime
        catalog = mock.MagicMock()
        catalog.default = template

        composer = MarkdownComposer()
        composer.compose(catalog, source_file, outdir)
        self.assertFalse(template.render.called)

    def test_uses_smartypants(self):
        source = '"quoted"'
        composer = MarkdownComposer()
        html = composer._generate_content(source)
        self.assertEqual('<p>&ldquo;quoted&rdquo;</p>', html)


class TestReStructuredTextComposer(TestCase):

    def test_generates_html(self):
        source = '**bold**'
        composer = ReStructuredTextComposer()
        html = composer._generate_content(source)
        expected = '<div class="document">\n' \
                   '<p><strong>bold</strong></p>\n' \
                   '</div>\n'
        self.assertEqual(expected, html)


class TestSassComposer(TestCase):

    def _make_fake_sass_bin(self):
        fake_bin = tempfile.mkdtemp()
        fake_sass = os.path.join(fake_bin, 'sass')
        with open(fake_sass, 'w') as f:
            f.write('#!/usr/bin/env python')
        st = os.stat(fake_sass)
        os.chmod(fake_sass, st.st_mode | stat.S_IEXEC)
        return fake_bin

    def test_abort_with_no_sass(self):
        """Test that handroll aborts if ``sass`` is not installed."""
        # The fake bin directory has no sass executable.
        fake_bin = tempfile.mkdtemp()
        self.assertRaises(AbortError, SassComposer, fake_bin)

    def test_create(self):
        fake_bin = self._make_fake_sass_bin()
        composer = SassComposer(fake_bin)
        self.assertTrue(isinstance(composer, SassComposer))

    def test_build_command(self):
        fake_bin = self._make_fake_sass_bin()
        composer = SassComposer(fake_bin)
        source_file = '/in/sassy.scss'
        output_file = '/out/sass.css'
        expected = [
            os.path.join(fake_bin, 'sass'), '--style', 'compressed',
            source_file, output_file]
        actual = composer.build_command(source_file, output_file)
        self.assertEqual(expected, actual)

    @mock.patch('handroll.composers.sass.subprocess')
    def test_failed_sass_aborts(self, subprocess):
        fake_bin = self._make_fake_sass_bin()
        composer = SassComposer(fake_bin)
        source_file = '/in/sassy.scss'
        output_dir = '/out'
        subprocess.Popen.return_value.communicate.return_value = ('boom', '')
        subprocess.Popen.return_value.returncode = 1
        self.assertRaises(
            AbortError, composer.compose, None, source_file, output_dir)

    def test_output_extension(self):
        fake_bin = self._make_fake_sass_bin()
        composer = SassComposer(fake_bin)
        self.assertEqual('.css', composer.output_extension)


class TestTextileComposer(TestCase):

    def test_generates_html(self):
        source = '*bold*'
        composer = TextileComposer()
        html = composer._generate_content(source)
        self.assertEqual('\t<p><strong>bold</strong></p>', html)

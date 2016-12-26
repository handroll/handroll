# Copyright (c) 2016, Matt Layman

import inspect
import os
import stat
import tempfile

import mock

from handroll.composers import Composer
from handroll.composers import Composers
from handroll.composers import CopyComposer
from handroll.composers.mixins import FrontmatterComposerMixin
from handroll.composers.atom import AtomComposer
from handroll.composers.generic import GenericHTMLComposer
from handroll.composers.j2 import Jinja2Composer
from handroll.composers.md import MarkdownComposer
from handroll.composers.rst import ReStructuredTextComposer
from handroll.composers.sass import SassComposer
from handroll.composers.txt import TextileComposer
from handroll.exceptions import AbortError
from handroll.tests import TestCase


class TestComposer(TestCase):

    def _make_one(self):
        config = self.factory.make_configuration()
        return Composer(config)

    def test_compose_not_implemented(self):
        composer = self._make_one()
        with self.assertRaises(NotImplementedError):
            composer.compose(None, None, None)

    def test_get_output_extension_not_implemented(self):
        composer = self._make_one()
        with self.assertRaises(NotImplementedError):
            composer.get_output_extension('file.txt')

    def test_has_config(self):
        config = self.factory.make_configuration()
        composer = Composer(config)
        self.assertEqual(config, composer._config)


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

    def test_get_output_extension(self):
        composers = self._make_one()
        extension = composers.get_output_extension('sample.md')
        self.assertEqual('.html', extension)


class TestAtomComposer(TestCase):

    def _make_one(self):
        config = self.factory.make_configuration()
        return AtomComposer(config)

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
        composer = self._make_one()
        composer.compose(None, self.source_file, self.outdir)
        self.assertTrue(os.path.exists(self.output_file))

    def test_must_have_entries(self):
        source = """{
            "title": "Fakity Fake",
            "id": "let's pretend this is unique"
        }"""
        with open(self.source_file, 'w') as f:
            f.write(source)
        composer = self._make_one()
        with self.assertRaises(AbortError):
            composer.compose(None, self.source_file, self.outdir)

    @mock.patch('handroll.composers.atom.json')
    def test_skips_up_to_date(self, json):
        open(self.output_file, 'w').close()
        composer = self._make_one()
        composer.compose(None, self.source_file, self.outdir)
        self.assertFalse(json.loads.called)

    def test_output_extension(self):
        composer = self._make_one()
        self.assertEqual('.xml', composer.get_output_extension('source.atom'))

    @mock.patch('handroll.composers.atom.json')
    def test_forces_update(self, json):
        json.loads.return_value = {
            'title': 'Fakity Fake',
            'id': "let's pretend this is unique",
            'entries': [{
                'title': 'Sample A',
                'updated': '2014-02-23T00:00:00',
                'published': '2014-02-22T00:00:00',
                'url': 'http://some.website.com/a.html',
                'summary': 'A summary of the sample post'
            }]
        }
        open(self.output_file, 'w').close()
        composer = self._make_one()
        composer._config.force = True
        composer.compose(None, self.source_file, self.outdir)
        self.assertTrue(json.loads.called)


class TestCopyComposer(TestCase):

    def _make_one(self):
        config = self.factory.make_configuration()
        return CopyComposer(config)

    @mock.patch('handroll.composers.shutil')
    def test_skips_same_files(self, shutil):
        marker = 'marker.txt'
        source = tempfile.mkdtemp()
        source_file = os.path.join(source, marker)
        outdir = tempfile.mkdtemp()
        open(source_file, 'w').close()
        open(os.path.join(outdir, marker), 'w').close()
        composer = self._make_one()
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
        composer = self._make_one()
        composer.compose(None, source_file, outdir)
        self.assertTrue(shutil.copy.called)

    def test_output_extension(self):
        """The copy composer takes the extension of the source file."""
        composer = self._make_one()
        self.assertEqual('.png', composer.get_output_extension('photo.png'))

    @mock.patch('handroll.composers.shutil')
    def test_copies_when_forced(self, shutil):
        marker = 'marker.txt'
        source = tempfile.mkdtemp()
        source_file = os.path.join(source, marker)
        outdir = tempfile.mkdtemp()
        open(source_file, 'w').close()
        open(os.path.join(outdir, marker), 'w').close()
        composer = self._make_one()
        composer._config.force = True
        composer.compose(None, source_file, outdir)
        self.assertTrue(shutil.copy.called)


class TestGenericHTMLComposer(TestCase):

    def _make_one(self):
        config = self.factory.make_configuration()
        return GenericHTMLComposer(config)

    def test_composes_file(self):
        catalog = mock.MagicMock()
        site = tempfile.mkdtemp()
        source_file = os.path.join(site, 'sample.generic')
        open(source_file, 'w').close()
        outdir = ''
        composer = self._make_one()
        with self.assertRaises(NotImplementedError):
            composer.compose(catalog, source_file, outdir)

    def test_selects_default_template(self):
        catalog = mock.MagicMock()
        default = mock.PropertyMock()
        type(catalog).default = default
        composer = self._make_one()
        composer.select_template(catalog, {})
        self.assertTrue(default.called)

    def test_selects_specified_template(self):
        catalog = mock.MagicMock()
        composer = self._make_one()
        composer.select_template(catalog, {'template': 'base.j2'})
        catalog.get_template.assert_called_once_with('base.j2')

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

        composer = self._make_one()
        self.assertTrue(composer._needs_update(None, source_file, output_file))

        past = future - 10
        os.utime(source_file, (past, past))
        self.assertTrue(
            composer._needs_update(template, source_file, output_file))

        template.last_modified = past
        self.assertFalse(
            composer._needs_update(template, source_file, output_file))

    def test_output_extension(self):
        composer = self._make_one()
        self.assertEqual('.html', composer.get_output_extension('source.rst'))

    def test_forces_update(self):
        site = tempfile.mkdtemp()
        output_file = os.path.join(site, 'output.md')
        open(output_file, 'w').close()
        past = os.path.getmtime(output_file) - 10
        source_file = os.path.join(site, 'test.md')
        open(source_file, 'w').close()
        os.utime(source_file, (past, past))
        template = mock.MagicMock(last_modified=past)
        composer = self._make_one()
        composer._config.force = True
        self.assertTrue(
            composer._needs_update(template, source_file, output_file))


class TestMarkdownComposer(TestCase):

    def _make_one(self):
        config = self.factory.make_configuration()
        return MarkdownComposer(config)

    def test_generates_html(self):
        source = '**bold**'
        composer = self._make_one()
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

        composer = self._make_one()
        composer.compose(catalog, source_file, outdir)
        self.assertFalse(template.render.called)

    def test_uses_smartypants(self):
        source = '"quoted"'
        composer = self._make_one()
        html = composer._generate_content(source)
        self.assertEqual('<p>&ldquo;quoted&rdquo;</p>', html)


class TestReStructuredTextComposer(TestCase):

    def _make_one(self):
        config = self.factory.make_configuration()
        return ReStructuredTextComposer(config)

    def test_generates_html(self):
        source = '**bold**'
        composer = self._make_one()
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
        with self.assertRaises(AbortError):
            SassComposer(fake_bin)

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
        with self.assertRaises(AbortError):
            composer.compose(None, source_file, output_dir)

    def test_output_extension(self):
        fake_bin = self._make_fake_sass_bin()
        composer = SassComposer(fake_bin)
        self.assertEqual('.css', composer.get_output_extension('source.sass'))


class TestTextileComposer(TestCase):

    def test_generates_html(self):
        source = '*bold*'
        config = self.factory.make_configuration()
        composer = TextileComposer(config)
        html = composer._generate_content(source)
        self.assertEqual('\t<p><strong>bold</strong></p>', html)


class TestFrontmatterComposerMixin(TestCase):

    def test_looks_like_frontmatter(self):
        mixin = FrontmatterComposerMixin()
        self.assertTrue(mixin._has_frontmatter('%YAML 1.1'))
        self.assertTrue(mixin._has_frontmatter('---'))

    def test_gets_frontmatter(self):
        source = inspect.cleandoc("""%YAML 1.1
        ---
        title: A Fake Title
        ---
        The Content
        """)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(source.encode('utf-8'))
        mixin = FrontmatterComposerMixin()
        data, source = mixin.get_data(f.name)
        self.assertEqual('A Fake Title', data['title'])
        self.assertEqual('The Content', source)

    def test_gets_frontmatter_no_directive(self):
        source = inspect.cleandoc("""---
        title: A Fake Title
        ---
        The Content
        """)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(source.encode('utf-8'))
        mixin = FrontmatterComposerMixin()
        data, source = mixin.get_data(f.name)
        self.assertEqual('A Fake Title', data['title'])
        self.assertEqual('The Content', source)

    @mock.patch('handroll.composers.mixins.signals')
    def test_fires_frontmatter_loaded(self, signals):
        source = inspect.cleandoc("""%YAML 1.1
        ---
        title: A Fake Title
        ---
        The Content
        """)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(source.encode('utf-8'))
        mixin = FrontmatterComposerMixin()
        data, source = mixin.get_data(f.name)
        signals.frontmatter_loaded.send.assert_called_once_with(
            f.name, frontmatter={'title': 'A Fake Title'})

    def test_malformed_yaml(self):
        source = inspect.cleandoc("""%YAML 1.1
        ---
        title: A Fake Title
        The Content
        """)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(source.encode('utf-8'))
        mixin = FrontmatterComposerMixin()
        with self.assertRaises(AbortError):
            mixin.get_data(f.name)

    def test_malformed_document_with_frontmatter(self):
        source = inspect.cleandoc("""%YAML 1.1
        ---
        title: A Fake Title
        """)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(source.encode('utf-8'))
        mixin = FrontmatterComposerMixin()
        with self.assertRaises(AbortError):
            mixin.get_data(f.name)


class TestJinja2Composer(TestCase):

    def _make_one(self):
        config = self.factory.make_configuration()
        config.outdir = tempfile.mkdtemp()
        return Jinja2Composer(config)

    def test_get_output_extension(self):
        composer = self._make_one()
        extension = composer.get_output_extension('source.xyz.j2')
        self.assertEqual('.xyz', extension)

    def test_composes(self):
        source = inspect.cleandoc("""%YAML 1.1
        ---
        title: A Fake Title
        ---
        title: {{ title }}
        domain: {{ config.domain }}
        """)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt.j2') as f:
            f.write(source.encode('utf-8'))
        composer = self._make_one()
        output_file = os.path.join(
            composer._config.outdir, os.path.basename(f.name.rstrip('.j2')))
        composer.compose(None, f.name, composer._config.outdir)
        content = open(output_file, 'r').read()
        self.assertEqual(
            'title: A Fake Title\ndomain: http://www.example.com\n',
            content)

    def test_composes_no_frontmatter(self):
        source = inspect.cleandoc("""First row
        domain: {{ config.domain }}
        """)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt.j2') as f:
            f.write(source.encode('utf-8'))
        composer = self._make_one()
        output_file = os.path.join(
            composer._config.outdir, os.path.basename(f.name.rstrip('.j2')))
        composer.compose(None, f.name, composer._config.outdir)
        content = open(output_file, 'r').read()
        self.assertEqual(
            'First row\ndomain: http://www.example.com\n', content)

    def test_needs_update(self):
        site = tempfile.mkdtemp()
        output_file = os.path.join(site, 'output.md')
        open(output_file, 'w').close()
        future = os.path.getmtime(output_file) + 1
        source_file = os.path.join(site, 'test.md')
        open(source_file, 'w').close()
        os.utime(source_file, (future, future))

        composer = self._make_one()
        self.assertTrue(composer._needs_update(source_file, output_file))

        past = future - 10
        os.utime(source_file, (past, past))
        self.assertFalse(composer._needs_update(source_file, output_file))

    def test_forces_update(self):
        site = tempfile.mkdtemp()
        output_file = os.path.join(site, 'output.md')
        open(output_file, 'w').close()
        past = os.path.getmtime(output_file) - 10
        source_file = os.path.join(site, 'test.md')
        open(source_file, 'w').close()
        os.utime(source_file, (past, past))
        composer = self._make_one()
        composer._config.force = True
        self.assertTrue(composer._needs_update(source_file, output_file))

    @mock.patch('handroll.composers.j2.jinja2.Template.render')
    def test_skips_up_to_date(self, render):
        site = tempfile.mkdtemp()
        source_file = os.path.join(site, 'source.txt.j2')
        open(source_file, 'w').close()
        output_file = os.path.join(site, 'source.txt')
        open(output_file, 'w').close()
        composer = self._make_one()
        composer.compose(None, source_file, site)
        self.assertFalse(render.called)

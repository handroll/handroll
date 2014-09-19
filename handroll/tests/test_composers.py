# Copyright (c) 2014, Matt Layman

import os
import stat
import tempfile
import unittest

import mock

from handroll.composers import Composers
from handroll.composers import CopyComposer
from handroll.composers.atom import AtomComposer
from handroll.composers.md import MarkdownComposer
from handroll.composers.rst import ReStructuredTextComposer
from handroll.composers.sass import SassComposer
from handroll.composers.txt import TextileComposer
from handroll.exceptions import AbortError


class TestComposers(unittest.TestCase):

    def test_selects_composer(self):
        composers = Composers()
        composer = composers.select_composer_for('sample.md')
        self.assertTrue(isinstance(composer, MarkdownComposer))


class TestAtomComposer(unittest.TestCase):

    def test_creates(self):
        composer = AtomComposer()
        self.assertTrue(isinstance(composer, AtomComposer))


class TestCopyComposer(unittest.TestCase):

    @mock.patch('handroll.composers.shutil')
    def test_skips_same_files(self, shutil):
        marker = 'marker.txt'
        source = tempfile.mkdtemp()
        source_file = os.path.join(source, marker)
        outdir = tempfile.mkdtemp()
        open(os.path.join(source, marker), 'w').close()
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
        open(os.path.join(source, marker), 'w').close()
        with open(os.path.join(outdir, marker), 'w') as f:
            f.write('something different')
        composer = CopyComposer()
        composer.compose(None, source_file, outdir)
        self.assertTrue(shutil.copy.called)

class TestMarkdownComposer(unittest.TestCase):

    def test_generates_html(self):
        source = '**bold**'
        composer = MarkdownComposer()
        html = composer._generate_content(source)
        self.assertEqual('<p><strong>bold</strong></p>', html)


class TestReStructuredTextComposer(unittest.TestCase):

    def test_generates_html(self):
        source = '**bold**'
        composer = ReStructuredTextComposer()
        html = composer._generate_content(source)
        expected = '<div class="document">\n' \
                   '<p><strong>bold</strong></p>\n' \
                   '</div>\n'
        self.assertEqual(expected, html)


class TestSassComposer(unittest.TestCase):

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
        expected = [os.path.join(fake_bin, 'sass'), source_file, output_file]
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


class TestTextileComposer(unittest.TestCase):

    def test_generates_html(self):
        source = '*bold*'
        composer = TextileComposer()
        html = composer._generate_content(source)
        self.assertEqual('\t<p><strong>bold</strong></p>', html)

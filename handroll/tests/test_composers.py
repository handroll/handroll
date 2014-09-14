# Copyright (c) 2014, Matt Layman

import os
import stat
import tempfile
import unittest

import mock

from handroll.composers.sass import SassComposer
from handroll.exceptions import AbortError


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

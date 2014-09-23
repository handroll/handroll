# Copyright (c) 2014, Matt Layman

import os
import tempfile
import unittest

import mock

from handroll.configuration import Configuration
from handroll.site import Site


class TestSite(unittest.TestCase):

    def _make_valid_site(self):
        site = tempfile.mkdtemp()
        open(os.path.join(site, 'template.html'), 'w').close()
        return Site(site)

    def test_generates_with_user_specified_outdir(self):
        site = self._make_valid_site()
        marker = 'marker.txt'
        open(os.path.join(site.path, marker), 'w').close()
        config = Configuration()
        config.outdir = tempfile.mkdtemp()

        site.generate(config)

        out_marker = os.path.join(config.outdir, marker)
        self.assertTrue(os.path.exists(out_marker))

    def test_cleans_output(self):
        site = self._make_valid_site()
        os.mkdir(site.output_root)

        site._clean_output()

        self.assertFalse(os.path.exists(site.output_root))

    def test_skips_file_with_skip_extension(self):
        site = self._make_valid_site()
        skip = 'to_my_lou.swp'
        open(os.path.join(site.path, skip), 'w').close()
        config = Configuration()

        site.generate(config)

        out_skip = os.path.join(site.output_root, skip)
        self.assertFalse(os.path.exists(out_skip))

    def test_skips_file_in_skip_list(self):
        site = self._make_valid_site()
        skip = Site.CONFIG
        open(os.path.join(site.path, skip), 'w').close()
        config = Configuration()

        site.generate(config)

        out_skip = os.path.join(site.output_root, skip)
        self.assertFalse(os.path.exists(out_skip))

    def test_skips_templates_directory(self):
        site = self._make_valid_site()
        templates = os.path.join(site.path, 'templates')
        os.mkdir(templates)
        config = Configuration()

        site.generate(config)

        out_templates = os.path.join(site.output_root, 'templates')
        self.assertFalse(os.path.exists(out_templates))

    def test_finds_valid_site_root_from_templates(self):
        original = os.getcwd()
        valid_site = tempfile.mkdtemp()
        open(os.path.join(valid_site, 'template.html'), 'w').close()
        os.chdir(valid_site)

        site = Site()

        self.assertEqual(valid_site, site.path)
        os.chdir(original)

    def test_finds_valid_site_root_from_conf(self):
        original = os.getcwd()
        valid_site = tempfile.mkdtemp()
        open(os.path.join(valid_site, Site.CONFIG), 'w').close()
        os.chdir(valid_site)

        site = Site()

        self.assertEqual(valid_site, site.path)
        os.chdir(original)

    def test_generates_output_directory(self):
        site = self._make_valid_site()
        another = os.path.join(site.path, 'another')
        os.mkdir(another)
        config = Configuration()

        site.generate(config)

        another_out = os.path.join(site.output_root, 'another')
        self.assertTrue(os.path.isdir(another_out))

    def test_does_timing(self):
        mock_time = mock.Mock()
        mock_time.return_value = 42.0  # Return float so that format works.
        site = self._make_valid_site()
        open(os.path.join(site.path, 'fake.md'), 'w').close()
        config = Configuration()
        config.timing = True

        with mock.patch('handroll.site.time.time', mock_time):
            site.generate(config)

        self.assertTrue(mock_time.called)

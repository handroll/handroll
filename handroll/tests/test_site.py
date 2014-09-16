# Copyright (c) 2014, Matt Layman

import os
import tempfile
import unittest

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

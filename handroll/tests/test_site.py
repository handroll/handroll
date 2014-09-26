# Copyright (c) 2014, Matt Layman

import os
import tempfile

from handroll.site import Site
from handroll.tests import TestCase


class TestSite(TestCase):

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

# Copyright (c) 2014, Matt Layman

import tempfile

from handroll.configuration import Configuration
from handroll.director import Director
from handroll.handlers import SiteHandler
from handroll.tests import TestCase


class TestSiteHandler(TestCase):

    def setUp(self):
        config = Configuration()
        config.outdir = tempfile.mkdtemp()
        self.site = self.factory.make_site()
        self.director = Director(config, self.site)

    def test_create(self):
        handler = SiteHandler(self.director)
        self.assertTrue(isinstance(handler, SiteHandler))

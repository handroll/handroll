# Copyright (c) 2016, Matt Layman

import os

from handroll.composers import Composers
from handroll.resolver import FileResolver
from handroll.tests import TestCase


class TestFileResolver(TestCase):

    def test_as_url(self):
        site = self.factory.make_site()
        config = self.factory.make_configuration()
        composers = Composers(config)
        resolver = FileResolver(site.path, composers, config)
        md_file = os.path.join(site.path, 'a_dir', 'test.md')
        url = resolver.as_url(md_file)
        self.assertEqual('http://www.example.com/a_dir/test.html', url)

    def test_as_route(self):
        site = self.factory.make_site()
        config = self.factory.make_configuration()
        composers = Composers(config)
        resolver = FileResolver(site.path, composers, config)
        md_file = os.path.join(site.path, 'a_dir', 'test.md')
        route = resolver.as_route(md_file)
        self.assertEqual('/a_dir/test.html', route)

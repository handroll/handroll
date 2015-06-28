# Copyright (c) 2015, Matt Layman

import os

from handroll.composers import Composers
from handroll.resolver import FileResolver
from handroll.tests import TestCase


class TestFileResolver(TestCase):

    def test_as_url(self):
        site = self.factory.make_site()
        composers = Composers()
        config = self.factory.make_configuration()
        resolver = FileResolver(site.path, composers, config)
        md_file = os.path.join(site.path, 'a_dir', 'test.md')
        url = resolver.as_url(md_file)
        self.assertEqual('http://www.example.com/a_dir/test.html', url)

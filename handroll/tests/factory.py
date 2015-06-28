# Copyright (c) 2015, Matt Layman

import datetime
import os
import tempfile

from handroll.configuration import Configuration
from handroll.director import Director
from handroll.extensions.blog import BlogPost
from handroll.site import Site


class Factory(object):
    """A factory to produce commonly needed objects"""

    def make_blog_post(self):
        kwargs = {
            'date': datetime.datetime.today(),
            'source_file': 'a_source_file.md',
            'title': 'A Blog Post',
        }
        return BlogPost(**kwargs)

    def make_configuration(self):
        config = Configuration()
        config._domain = 'http://www.example.com'
        return config

    def make_director(self):
        config = Configuration()
        site = self.make_site()
        return Director(config, site, [])

    def make_site(self):
        """Make a valid site instance."""
        site = tempfile.mkdtemp()
        open(os.path.join(site, 'template.html'), 'w').close()
        return Site(site)

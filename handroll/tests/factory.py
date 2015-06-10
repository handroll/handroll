# Copyright (c) 2015, Matt Layman

import os
import tempfile

from handroll.configuration import Configuration
from handroll.director import Director
from handroll.site import Site


class Factory(object):
    """A factory to produce commonly needed objects"""

    def make_director(self):
        config = Configuration()
        site = self.make_site()
        return Director(config, site, [])

    def make_site(self):
        """Make a valid site instance."""
        site = tempfile.mkdtemp()
        open(os.path.join(site, 'template.html'), 'w').close()
        return Site(site)

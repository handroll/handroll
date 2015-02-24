# Copyright (c) 2015, Matt Layman

import os
import tempfile

from handroll.site import Site


class Factory(object):
    """A factory to produce commonly needed objects"""

    def make_site(self):
        """Make a valid site instance."""
        site = tempfile.mkdtemp()
        open(os.path.join(site, 'template.html'), 'w').close()
        return Site(site)

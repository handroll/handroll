# Copyright (c) 2014, Matt Layman
"""The website model"""

import os


class Site(object):

    TEMPLATE = 'template.html'

    def __init__(self, path):
        self.path = path

    @property
    def template(self):
        return os.path.join(self.path, self.TEMPLATE)

    def is_valid(self):
        if not os.path.isdir(self.path):
            print('{0} is not a directory.'.format(self.path))
            return False

        if not os.path.exists(self.template):
            print('{0} is missing.'.format(self.template))
            return False

        return True

# Copyright (c) 2016, Matt Layman
"""The website model"""

import os

from handroll import template
from handroll.exceptions import AbortError
from handroll.i18n import _


class Site(object):

    CONFIG = 'handroll.conf'
    OUTPUT = 'output'

    def __init__(self, path=None):
        self.path = path
        if self.path is None:
            self.path = self._find_site_root_from(os.getcwd())

        # Make sure that the path is absolute.
        if os.path.isdir(self.path):
            self.path = os.path.abspath(self.path)

    @classmethod
    def build(cls, args):
        """Build a validated site."""
        site = cls(args.site)
        valid, message = site.is_valid()
        if not valid:
            raise AbortError(_('Invalid site source: {0}').format(message))
        return site

    @property
    def config_file(self):
        return os.path.join(self.path, self.CONFIG)

    @property
    def output_root(self):
        """The default output root directory"""
        return os.path.join(self.path, self.OUTPUT)

    def is_valid(self):
        if not os.path.isdir(self.path):
            return False, _('{path} is not a directory.').format(
                path=self.path)

        return True, ''

    def _find_site_root_from(self, cwd):
        """Ascend through the current working directory provided to find
        something that looks like the root of a handroll site and return that
        path. Assumes that ``cwd`` is a valid directory path."""
        candidate = cwd
        while True:
            if self._is_site_root(candidate):
                return candidate

            parent = os.path.realpath(os.path.join(candidate, os.pardir))
            if candidate == parent:
                # When the next candidate is equal to the previous one, then
                # the root of the filesystem has been reached and tested.
                break

            candidate = parent

        raise AbortError(
            _('A handroll site was not found in {current_directory}'
              ' or any of its parents.').format(current_directory=cwd))

    def _is_site_root(self, path):
        """Check if the path provided is the handroll site's root."""
        # It looks like a site root if it has the config file.
        if os.path.exists(os.path.join(path, self.CONFIG)):
            return True
        # It looks like a site root if it has templates.
        elif template.has_templates(path):
            return True

        return False

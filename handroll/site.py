# Copyright (c) 2017, Matt Layman
"""The website model"""

import os

from handroll import template
from handroll.exceptions import AbortError
from handroll.i18n import _


class Site(object):
    """A Site represents a handroll site source.

    This class contains validation logic to confirm that a directory
    is a valid handroll site.
    """

    CONFIG = 'handroll.conf'
    OUTPUT = 'output'

    SKIP_DIRECTORIES = set([
        '.sass-cache',
    ])

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

    def walk(self):
        """Walk the site source, skipping items that should be skipped."""
        for dirpath, dirnames, filenames in os.walk(self.path):
            # Prevent work on the output or templates directory.
            # Skip the template.
            if dirpath == self.path:
                if self.OUTPUT in dirnames:
                    dirnames.remove(self.OUTPUT)
                if template.TEMPLATES_DIR in dirnames:
                    dirnames.remove(template.TEMPLATES_DIR)
                if template.DEFAULT_TEMPLATE in filenames:
                    filenames.remove(template.DEFAULT_TEMPLATE)

            self._prune_skip_directories(dirnames)

            yield dirpath, dirnames, filenames

    def _prune_skip_directories(self, dirnames):
        """Prune out any directories that should be skipped from the provided
        list of directories.
        """
        for directory in dirnames:
            if directory in self.SKIP_DIRECTORIES:
                dirnames.remove(directory)

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

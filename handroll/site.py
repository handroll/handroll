# Copyright (c) 2014, Matt Layman
"""The website model"""

import os
import shutil
import time

from handroll import logger
from handroll import template
from handroll.composers import Composers
from handroll.exceptions import AbortError
from handroll.i18n import _
from handroll.template import catalog


class Site(object):

    CONFIG = 'handroll.conf'
    OUTPUT = 'output'
    SKIP_EXTENSION = [
        '.swp',
    ]
    SKIP_FILES = [
        CONFIG,
    ]

    def __init__(self, path=None):
        self.path = path
        if self.path is None:
            self.path = self._find_site_root_from(os.getcwd())

        self.catalog = catalog.TemplateCatalog(self.path)
        self.composers = Composers()

    @property
    def config_file(self):
        return os.path.join(self.path, self.CONFIG)

    @property
    def output_root(self):
        """The default output root directory"""
        return os.path.join(self.path, self.OUTPUT)

    def generate(self, config):
        """Walk the site tree and generate the output."""
        self._clean_output()

        # When no output directory is given, the default will be used.
        if config.outdir is None:
            outdir = self.output_root
        else:
            outdir = config.outdir

        self._generate_output(outdir, config.timing)

    def is_valid(self):
        if not os.path.isdir(self.path):
            return False, _('{path} is not a directory.').format(
                path=self.path)

        return True, ''

    def _clean_output(self):
        if os.path.exists(self.output_root):
            logger.info(_('Removing the old {output_root} ...').format(
                output_root=self.output_root))
            shutil.rmtree(self.output_root)

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

    def _generate_output(self, outdir, timing):
        if os.path.exists(outdir):
            logger.info('Updating {0} ...'.format(outdir))
        else:
            logger.info('Creating {0} ...'.format(outdir))
            os.mkdir(outdir)

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

            output_dirpath = self._get_output_dirpath(dirpath, outdir)
            logger.info('Populating {0} ...'.format(output_dirpath))

            # Create new directories in output.
            for dirname in dirnames:
                out_dir = os.path.join(output_dirpath, dirname)
                # The directory may already exist for updates.
                if not os.path.exists(out_dir):
                    logger.info('Creating directory {0} ...'.format(out_dir))
                    os.mkdir(out_dir)

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                self._process_file(filepath, output_dirpath, timing)

    def _get_output_dirpath(self, dirpath, outdir):
        """Convert an input directory path rooted at the site path into the
        name destined for the output directory."""
        # Only split once to prevent the list from splitting multiple times on
        # a common word like 'site'.
        remainder = dirpath.split(self.path, 1)[1]
        if remainder:
            # Make sure the remainder doesn't look like an abs path.
            return os.path.join(outdir, remainder.lstrip(os.sep))
        else:
            return outdir

    def _process_file(self, filepath, output_dirpath, timing):
        """Process the file according to its type."""
        filename = os.path.basename(filepath)
        if self._should_skip(filename):
            return

        if timing:
            start = time.time()

        composer = self.composers.select_composer_for(filename)
        composer.compose(self.catalog, filepath, output_dirpath)

        if timing:
            end = time.time()
            # Put at warn level to be independent of the verbose option.
            logger.warn('[{:.3f}s]'.format(end - start))

    def _should_skip(self, filename):
        """Determine if the file type should be skipped."""
        for skip_type in self.SKIP_EXTENSION:
            if filename.endswith(skip_type):
                logger.debug(
                    'Skipping {0} with skipped file type \'{1}\' ...'.format(
                        filename, skip_type))
                return True

        for skip_file in self.SKIP_FILES:
            if filename.endswith(skip_file):
                logger.debug('Skipping special file {0} ...'.format(filename))
                return True

        return False

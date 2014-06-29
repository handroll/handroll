# Copyright (c) 2014, Matt Layman
"""The website model"""

import os
import shutil
from string import Template
import time

from handroll import logger
from handroll.composers import Composers
from handroll.exceptions import AbortError


class Site(object):

    CONFIG = 'handroll.conf'
    OUTPUT = 'output'
    TEMPLATE = 'template.html'
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

        self.composers = Composers()
        self._template = None

    @property
    def config_file(self):
        return os.path.join(self.path, self.CONFIG)

    @property
    def output_root(self):
        """The default output root directory"""
        return os.path.join(self.path, self.OUTPUT)

    @property
    def template_name(self):
        return os.path.join(self.path, self.TEMPLATE)

    @property
    def template(self):
        if self._template is None:
            with open(self.template_name, 'r') as t:
                self._template = Template(t.read())

        return self._template

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
            return False, '{0} is not a directory.'.format(self.path)

        if not os.path.exists(self.template_name):
            return False, '{0} is missing.'.format(self.template_name)

        return True, ''

    def _clean_output(self):
        if os.path.exists(self.output_root):
            logger.info('Removing the old {0} ...'.format(self.output_root))
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
            'A handroll site was not found in {0}'
            ' or any of its parents.'.format(cwd))

    def _is_site_root(self, path):
        """Check if the path provided is the handroll site's root."""
        # It looks like a site root if it has the config file.
        if os.path.exists(os.path.join(path, self.CONFIG)):
            return True
        # It looks like a site root if it has a template.
        elif os.path.exists(os.path.join(path, self.TEMPLATE)):
            return True

        return False

    def _generate_output(self, outdir, timing):
        if os.path.exists(outdir):
            logger.info('Updating {0} ...'.format(outdir))
        else:
            logger.info('Creating {0} ...'.format(outdir))
            os.mkdir(outdir)

        for (dirpath, dirnames, filenames) in os.walk(self.path):
            # Do not walk the output.
            if dirpath.startswith(outdir):
                continue

            # Prevent work on the output directory.
            # Skip the template.
            if dirpath == self.path:
                dirnames = [name for name in dirnames if name != self.OUTPUT]
                filenames = [f for f in filenames if f != self.TEMPLATE]

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
        composer.compose(self.template, filepath, output_dirpath)

        if timing:
            end = time.time()
            # Put at warn level to be independent of the verbose option.
            logger.warn('[{:.3f}s]'.format(end - start))

    def _should_skip(self, filename):
        """Determine if the file type should be skipped."""
        for skip_type in self.SKIP_EXTENSION:
            if filename.endswith(skip_type):
                logger.info(
                    'Skipping {0} with skipped file type \'{1}\' ...'.format(
                        filename, skip_type))
                return True

        for skip_file in self.SKIP_FILES:
            if filename.endswith(skip_file):
                logger.info('Skipping special file {0} ...'.format(filename))
                return True

        return False

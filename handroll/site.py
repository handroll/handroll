# Copyright (c) 2014, Matt Layman
"""The website model"""

import os
import shutil
from string import Template

from handroll import logger
from handroll.composers import Composers


class Site(object):

    OUTPUT = 'output'
    TEMPLATE = 'template.html'
    SKIP_EXTENSION = [
        '.swp',
    ]

    def __init__(self, path):
        self.path = path
        self.composers = Composers()
        self._template = None

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

    def generate(self, outdir):
        """Walk the site tree and generate the output."""
        self._clean_output()

        # When no output directory is given, the default will be used.
        if outdir is None:
            outdir = self.output_root

        self._generate_output(outdir)

    def is_valid(self):
        if not os.path.isdir(self.path):
            print('{0} is not a directory.'.format(self.path))
            return False

        if not os.path.exists(self.template_name):
            print('{0} is missing.'.format(self.template_name))
            return False

        return True

    def _clean_output(self):
        if os.path.exists(self.output_root):
            logger.info('Removing the old {0} ...'.format(self.output_root))
            shutil.rmtree(self.output_root)

    def _generate_output(self, outdir):
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
                self._process_file(filepath, output_dirpath)

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

    def _process_file(self, filepath, output_dirpath):
        """Process the file according to its type."""
        filename = os.path.basename(filepath)
        if self._should_skip(filename):
            return

        composer = self.composers.select_composer_for(filename)
        composer.compose(self.template, filepath, output_dirpath)

    def _should_skip(self, filename):
        """Determine if the file type should be skipped."""
        for skip_type in self.SKIP_EXTENSION:
            if filename.endswith(skip_type):
                logger.info(
                    'Skipping {0} with skipped file type \'{1}\' ...'.format(
                        filename, skip_type))
                return True

        return False

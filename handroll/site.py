# Copyright (c) 2014, Matt Layman
"""The website model"""

import os
import shutil
from string import Template

from handroll import logger
from handroll.composers import MarkdownComposer


class Site(object):

    OUTPUT = 'output'
    TEMPLATE = 'template.html'

    def __init__(self, path):
        self.path = path
        self.composer = MarkdownComposer()
        self._template = None

    @property
    def output_root(self):
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

    def generate(self):
        """Walk the site tree and generate the output."""
        self._clean_output()
        os.mkdir(self.output_root)
        self._generate_output()

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

    def _generate_output(self):
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            # Do not walk the output.
            if dirpath.startswith(self.output_root):
                continue

            # Prevent work on the output directory.
            # Skip the template.
            if dirpath == self.path:
                dirnames = [name for name in dirnames if name != self.OUTPUT]
                filenames = [f for f in filenames if f != self.TEMPLATE]

            output_dirpath = self._get_output_dirpath(dirpath)
            logger.info('Populating {0} ...'.format(output_dirpath))

            # Create new directories in output.
            if dirnames:
                for dirname in dirnames:
                    out_dir = os.path.join(output_dirpath, dirname)
                    logger.info('Creating directory {0} ...'.format(out_dir))
                    os.mkdir(out_dir)

            # Handle files.
            for file_ in filenames:
                filepath = os.path.join(dirpath, file_)
                if file_.endswith('.md'):
                    self.composer.compose(
                        self.template, filepath, output_dirpath)
                else:
                    logger.info(
                        'Copying {0} to {1} ...'.format(file_, output_dirpath))
                    shutil.copy(filepath, output_dirpath)

    def _get_output_dirpath(self, dirpath):
        """Convert an input directory path rooted at the site path into the
        name destined for the output directory."""
        # Only split once to prevent the list from splitting multiple times on
        # a common word like 'site'.
        remainder = dirpath.split(self.path, 1)[1]
        if remainder:
            # Make sure the remainder doesn't look like an abs path.
            return os.path.join(self.output_root, remainder.lstrip(os.sep))
        else:
            return self.output_root

# Copyright (c) 2014, Matt Layman
"""The website model"""

import os
import shutil

from handroll import logger


class Site(object):

    OUTPUT = 'output'
    TEMPLATE = 'template.html'

    def __init__(self, path):
        self.path = path

    @property
    def output_root(self):
        return os.path.join(self.path, self.OUTPUT)

    @property
    def template(self):
        return os.path.join(self.path, self.TEMPLATE)

    def generate(self):
        """Walk the site tree and generate the output."""
        self._clean_output()
        os.mkdir(self.output_root)
        self._generate_output()

    def is_valid(self):
        if not os.path.isdir(self.path):
            print('{0} is not a directory.'.format(self.path))
            return False

        if not os.path.exists(self.template):
            print('{0} is missing.'.format(self.template))
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
                if file_.endswith('.md'):
                    # TODO: The real work of generating html.
                    logger.info('Generating HTML for {0} ...'.format(file_))
                else:
                    logger.info(
                        'Copying {0} to {1} ...'.format(file_, output_dirpath))
                    shutil.copy(os.path.join(dirpath, file_), output_dirpath)

    def _get_output_dirpath(self, dirpath):
        """Convert an input directory path rooted at the site path into the
        name destined for the output directory."""
        # Only split once to prevent the list from splitting multiple times on
        # a common word like 'site'.
        remainder = dirpath.split(self.path, 1)[1]
        if remainder:
            return os.path.join(self.output_root, remainder)
        else:
            return self.output_root

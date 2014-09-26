# Copyright (c) 2014, Matt Layman

import os
import time

from handroll import logger
from handroll import template
from handroll.composers import Composers
from handroll.i18n import _
from handroll.site import Site
from handroll.template import catalog


class Director(object):
    """The director is responsible for producing the generated content from the
    site input. Each site file is delegated to a composer to generate content.
    """

    SKIP_EXTENSION = [
        '.swp',
    ]
    SKIP_FILES = [
        Site.CONFIG,
    ]

    def __init__(self, config, site):
        self.config = config
        self.site = site
        self.catalog = catalog.TemplateCatalog(site.path)
        self.composers = Composers()

    def produce(self):
        """Walk the site tree and generate the output."""
        # When no output directory is given, the default will be used.
        if self.config.outdir is None:
            outdir = self.site.output_root
        else:
            outdir = self.config.outdir

        self._generate_output(outdir, self.config.timing)

    def _generate_output(self, outdir, timing):
        if os.path.exists(outdir):
            logger.info(_('Updating {outdir} ...').format(outdir=outdir))
        else:
            logger.info(_('Creating {outdir} ...').format(outdir=outdir))
            os.mkdir(outdir)

        for dirpath, dirnames, filenames in os.walk(self.site.path):
            # Prevent work on the output or templates directory.
            # Skip the template.
            if dirpath == self.site.path:
                if self.site.OUTPUT in dirnames:
                    dirnames.remove(self.site.OUTPUT)
                if template.TEMPLATES_DIR in dirnames:
                    dirnames.remove(template.TEMPLATES_DIR)
                if template.DEFAULT_TEMPLATE in filenames:
                    filenames.remove(template.DEFAULT_TEMPLATE)

            output_dirpath = self._get_output_dirpath(dirpath, outdir)
            logger.info(_('Populating {dirpath} ...').format(
                dirpath=output_dirpath))

            # Create new directories in output.
            for dirname in dirnames:
                out_dir = os.path.join(output_dirpath, dirname)
                # The directory may already exist for updates.
                if not os.path.exists(out_dir):
                    logger.info(_('Creating directory {out_dir} ...').format(
                        out_dir=out_dir))
                    os.mkdir(out_dir)

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                self._process_file(filepath, output_dirpath, timing)

    def _get_output_dirpath(self, dirpath, outdir):
        """Convert an input directory path rooted at the site path into the
        name destined for the output directory."""
        # Only split once to prevent the list from splitting multiple times on
        # a common word like 'site'.
        remainder = dirpath.split(self.site.path, 1)[1]
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
            logger.warn('[{0:.3f}s]'.format(end - start))

    def _should_skip(self, filename):
        """Determine if the file type should be skipped."""
        for skip_type in self.SKIP_EXTENSION:
            if filename.endswith(skip_type):
                logger.debug(
                    _('Skipping {filename} with skipped file type'
                      ' \'{skip_type}\' ...').format(
                        filename=filename, skip_type=skip_type))
                return True

        for skip_file in self.SKIP_FILES:
            if filename.endswith(skip_file):
                logger.debug(_('Skipping special file {filename} ...').format(
                    filename=filename))
                return True

        return False

# Copyright (c) 2016, Matt Layman

import os
import time

from handroll import logger, signals, template
from handroll.composers import Composers
from handroll.i18n import _
from handroll.resolver import FileResolver
from handroll.site import Site
from handroll.template import catalog


class Director(object):
    """The director is responsible for producing the generated content from the
    site input. Each site file is delegated to a composer to generate content.
    """

    SKIP_EXTENSION = (
        '~',
        '.swo',
        '.swp',
        '.swpx',
        '.swx',
        '4913',  # Vim makes a '4913' file for file system checking. Seriously.
    )
    SKIP_DIRECTORIES = set([
        '.sass-cache',
    ])
    SKIP_FILES = (
        Site.CONFIG,
    )

    def __init__(self, config, site, extensions):
        self.config = config
        self.site = site
        self.extensions = extensions
        self.catalog = catalog.TemplateCatalog(site.path)
        self.composers = Composers(config)
        self.resolver = FileResolver(site.path, self.composers, config)

    @property
    def outdir(self):
        """Look up the output directory based on what configuration is
        available.
        """
        # When no output directory is given, the default will be used.
        if self.config.outdir is None:
            return self.site.output_root
        else:
            return self.config.outdir

    def process_file(self, filepath):
        """Process a site source file, determine its output location, and
        trigger its composer.

        This is primarily used for the watchdog handler and would be slow if
        used in the main ``produce`` method.
        """
        if self._should_skip(filepath):
            return
        # Skip files in the output directory.
        if self.is_in_output(filepath):
            return
        # Skip templates.
        if self.catalog.is_template(filepath):
            return

        signals.pre_composition.send(self)
        dirname = os.path.dirname(filepath)
        output_dirpath = self._get_output_dirpath(dirname, self.outdir)
        self._process_file(filepath, output_dirpath, self.config.timing)
        signals.post_composition.send(self)

    def process_directory(self, directory):
        """Process a site directory by creating its equivalent in output.

        This is used by the watchdog.
        """
        # Skip files in the output directory.
        if self.is_in_output(directory):
            return
        # Skip templates.
        if self.catalog.is_template(directory):
            return

        signals.pre_composition.send(self)
        dirname, basedir = os.path.split(directory)
        output_dirpath = self._get_output_dirpath(dirname, self.outdir)
        os.mkdir(os.path.join(output_dirpath, basedir))
        signals.post_composition.send(self)

    def is_in_output(self, path):
        """Check if the file or directory path is in the output directory.

        Files or directories that are in the output but are also in the source
        (for the corner case where the source is in the output directory) are
        ignored.
        """
        # Because all paths should be absolute, it should be simple to find out
        # if this path is in the output directory.
        outdir = self.outdir
        source_is_in_outdir = self.site.path.startswith(outdir)
        if source_is_in_outdir and path.startswith(self.site.path):
            return False

        return path.startswith(outdir)

    def produce(self):
        """Walk the site tree and generate the output."""
        signals.pre_composition.send(self)
        self._generate_output(self.outdir, self.config.timing)
        signals.post_composition.send(self)

    def prune_skip_directories(self, dirnames):
        """Prune out any directories that should be skipped from the provided
        list of directories.
        """
        for directory in dirnames:
            if directory in self.SKIP_DIRECTORIES:
                dirnames.remove(directory)

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

            self.prune_skip_directories(dirnames)

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
        if filename.endswith(self.SKIP_EXTENSION):
            logger.debug(
                _('Skipping {filename} with skipped file type ...').format(
                    filename=filename))
            return True

        if filename.endswith(self.SKIP_FILES):
            logger.debug(_('Skipping special file {filename} ...').format(
                filename=filename))
            return True

        return False

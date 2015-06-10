# Copyright (c) 2015, Matt Layman

try:
    from ConfigParser import ConfigParser
except ImportError:  # pragma: no cover
    from configparser import ConfigParser
import os

from handroll.exceptions import AbortError
from handroll.i18n import _


class Configuration(object):
    """Configuration data used by handroll"""

    def __init__(self):
        self.active_extensions = set()
        # The output directory should be absolute. That constraint will make it
        # easy to check if a filepath is in the output directory.
        self.outdir = None
        self.timing = None

        # Keep the parser to allow extensions to get configuration file data.
        self.parser = ConfigParser()

    def load_from_arguments(self, args):
        """Load any configuration attributes from the provided command line
        arguments. Arguments have the highest precedent so overwrite any other
        value if a value exists."""
        if args.outdir is not None:
            self.outdir = os.path.abspath(args.outdir)

        if args.timing is not None:
            self.timing = args.timing

    def load_from_file(self, config_file):
        """Load any configuration attributes from the provided config file."""
        with open(config_file, 'r') as f:
            self.parser.readfp(f)
            if self.parser.has_option('site', 'outdir'):
                self.outdir = os.path.abspath(os.path.expanduser(
                    self.parser.get('site', 'outdir')))
            if self.parser.has_section('site'):
                self._find_extensions(self.parser)

    def _find_extensions(self, parser):
        """Check if the site options have extensions to enable."""
        for option in parser.options('site'):
            if option.startswith('with_'):
                try:
                    extension = option.split('with_', 1)[1] or option
                    enabled = parser.getboolean('site', option)
                    if enabled:
                        self.active_extensions.add(extension)
                except ValueError:
                    raise AbortError(_(
                        'Cannot determine if {extension} is enabled.').format(
                            extension=extension))


def build_config(config_file, args):
    """Build a ``Configuration`` instance and populate it with file data and
    user inputs."""
    config = Configuration()
    if os.path.exists(config_file):
        config.load_from_file(config_file)

    config.load_from_arguments(args)
    return config

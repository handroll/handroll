# Copyright (c) 2014, Matt Layman

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
import os


class Configuration(object):
    """Configuration data used by handroll"""

    def __init__(self):
        self.outdir = None
        self.timing = None

    def load_from_arguments(self, args):
        """Load any configuration attributes from the provided command line
        arguments. Arguments have the highest precedent so overwrite any other
        value if a value exists."""
        if args.outdir is not None:
            self.outdir = args.outdir

        if args.timing is not None:
            self.timing = args.timing

    def load_from_file(self, config_file):
        """Load any configuration attributes from the provided config file."""
        with open(config_file, 'r') as f:
            parser = ConfigParser()
            parser.readfp(f)
            if parser.has_option('site', 'outdir'):
                self.outdir = os.path.expanduser(parser.get('site', 'outdir'))


def build_config(config_file, args):
    """Build a ``Configuration`` instance and populate it with file data and
    user inputs."""
    config = Configuration()
    if os.path.exists(config_file):
        config.load_from_file(config_file)

    config.load_from_arguments(args)
    return config

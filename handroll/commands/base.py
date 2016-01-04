# Copyright (c) 2016, Matt Layman

import sys

from handroll.configuration import build_config
from handroll.director import Director
from handroll.extensions.loader import ExtensionLoader
from handroll.i18n import _


def prepare_director(args, site):
    """Prepare the director to produce a site."""
    loader = ExtensionLoader()
    loader.load()
    config = build_config(site.config_file, args)
    extensions = loader.get_active_extensions(config)
    return Director(config, site, extensions)


def finish():
    print(_('Complete.'))
    sys.exit()


class Command(object):
    """A command class with the minimal interface required for each command."""

    @classmethod
    def register(cls, parser):
        """Register required options.

        The provided parser is a subparser from ``subparsers.add_parser``.
        """
        raise NotImplementedError()

    def run(self, args):
        """Run whatever action the command intends."""
        raise NotImplementedError()

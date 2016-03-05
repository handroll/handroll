# Copyright (c) 2016, Matt Layman
"""The main entry point for the tool"""

import argparse
import logging
import os
import sys

from handroll import logger
from handroll.commands.builtins import COMMANDS
from handroll.exceptions import AbortError
from handroll.i18n import _


def main(argv=sys.argv):
    args = parse(argv)

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        args.func(args)
    except AbortError as abort:
        logger.error(str(abort))
        sys.exit(_('Incomplete.'))


def parse(argv):
    """Parse the user arguments."""
    parser = build_parser()

    # argparse expects the executable to be removed from argv.
    args = parser.parse_args(argv[1:])

    # Normalize the site path so that all sites are handled consistently.
    # Not every command will have the site argument, but the normalization
    # occurs here to keep the check in one place.
    if 'site' in vars(args) and args.site:
        args.site = args.site.rstrip(os.sep)

    return args


def build_parser():
    """Build the parser that will have all available commands and options."""
    description = _('A website generator for software artisans')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-v', '--verbose', action='store_true', help=_('use verbose messages'))
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help=_('show debug level messages'))
    parser.add_argument(
        '-t', '--timing', action='store_true', help=_('time the execution'))
    parser.add_argument(
        '-f', '--force', action='store_true',
        help=_('force composers to write output'))

    subparsers = parser.add_subparsers(title=_('available commands'))
    [command.register(subparsers) for command in COMMANDS]
    return parser

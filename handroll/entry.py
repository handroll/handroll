# Copyright (c) 2016, Matt Layman
"""The main entry point for the tool"""

import argparse
import logging
import os
import sys

from handroll import logger, scaffolder
from handroll.commands.base import finish, prepare_director
from handroll.exceptions import AbortError
from handroll.i18n import _
from handroll.server import serve
from handroll.site import Site


def main(argv=sys.argv):
    args = parse(argv)

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        if args.scaffold:
            scaffolder.make(args.scaffold, args.site)
            finish()

        site = Site.build(args)
        director = prepare_director(args, site)
        director.produce()

        if args.watch:
            serve(site, director)
        else:
            finish()
    except AbortError as abort:
        logger.error(str(abort))
        sys.exit(_('Incomplete.'))


def parse(argv):
    """Parse the user arguments."""
    parser = build_parser()

    # argparse expects the executable to be removed from argv.
    args = parser.parse_args(argv[1:])

    # Normalize the site path so that all sites are handled consistently.
    if args.site:
        args.site = args.site.rstrip(os.sep)

    return args


def build_parser():
    """Build the parser that will have all available commands and options."""
    description = _('A website generator for software artisans')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('site', nargs='?', help=_('the path to your website'))
    parser.add_argument(
        'outdir', nargs='?', help=_('an optional output directory to create or'
                                    ' update if it already exists'))
    parser.add_argument(
        '-w', '--watch', action='store_true',
        help=_('watch the site for changes and'
               ' run a web server in the output directory'))
    parser.add_argument(
        '-s', '--scaffold', action='store',
        nargs='?', const=scaffolder.LIST_SCAFFOLDS, metavar='scaffold',
        help=_('make a new handroll site from a scaffold '
               'or list the available scaffolds'))
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
    return parser

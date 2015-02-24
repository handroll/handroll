# Copyright (c) 2015, Matt Layman
"""The main entry point for the tool"""

import argparse
import logging
import os
import sys

from handroll import logger
from handroll.configuration import build_config
from handroll.director import Director
from handroll.exceptions import AbortError
from handroll.i18n import _
from handroll.server import serve
from handroll.site import Site


def main(argv=sys.argv):
    args = parse_args(argv)

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        site = Site(args.site)
        valid, message = site.is_valid()
        if not valid:
            raise AbortError(_('Invalid site source: {0}').format(message))

        config = build_config(site.config_file, args)
        director = Director(config, site)
        director.produce()

        if not args.watch:
            print(_('Complete.'))
    except AbortError as abort:
        logger.error(str(abort))
        sys.exit(_('Incomplete.'))

    if args.watch:
        serve(site, director)


def parse_args(argv):
    description = _('A website generator for software artisans')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('site', nargs='?', help=_('the path to your website'))
    parser.add_argument(
        'outdir', nargs='?', help=_('an optional output directory to create or'
                                    ' update if it already exists'))
    parser.add_argument(
        '-v', '--verbose', action='store_true', help=_('use verbose messages'))
    parser.add_argument(
        '-t', '--timing', action='store_true', help=_('time the execution'))
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help=_('show debug level messages'))
    parser.add_argument(
        '-w', '--watch', action='store_true',
        help=_('watch the site for changes and'
               ' run a web server in the output directory'))

    # argparse expects the executable to be removed from argv.
    args = parser.parse_args(argv[1:])

    # Normalize the site path so that all sites are handled consistently.
    if args.site:
        args.site = args.site.rstrip(os.sep)

    return args

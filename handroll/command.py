# Copyright (c) 2014, Matt Layman
"""The main entry point for the tool"""

import argparse
import logging
import sys

from handroll import logger
from handroll.configuration import build_config
from handroll.exceptions import AbortError
from handroll.i18n import _
from handroll.site import Site


def main():
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
    args = parser.parse_args()

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
        site.generate(config)
        print(_('Complete.'))
    except AbortError as abort:
        logger.error(abort.message)
        sys.exit(_('Incomplete.'))

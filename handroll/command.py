# Copyright (c) 2014, Matt Layman
"""The main entry point for the tool"""

import argparse
import logging
import sys

from handroll import logger
from handroll.configuration import build_config
from handroll.exceptions import AbortError
from handroll.site import Site


def main():
    description = 'A website generator for software artisans'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('site', nargs='?', help='the path to your website')
    parser.add_argument(
        'outdir', nargs='?', help='an optional output directory to create or'
        ' update if it already exists')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='use verbose messages')
    parser.add_argument(
        '-t', '--timing', action='store_true', help='time the execution')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)

    try:
        site = Site(args.site)
        valid, message = site.is_valid()
        if not valid:
            raise AbortError('Invalid site source: {0}'.format(message))

        config = build_config(site.config_file, args)
        site.generate(config)
        print('Complete.')
    except AbortError as abort:
        logger.error(abort.message)
        sys.exit('Incomplete.')

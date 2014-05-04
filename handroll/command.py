# Copyright (c) 2014, Matt Layman
"""The main entry point for the tool"""

import argparse
import logging
import sys

from handroll import logger
from handroll.site import Site


def main():
    description = 'A website generator for software artisans'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('site', help='the path to your website')
    parser.add_argument(
        'outdir', nargs='?', help='an optional output directory to create or'
        ' update if it already exists')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='use verbose messages')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)

    site = Site(args.site)
    if not site.is_valid():
        sys.exit('Incomplete.')

    site.generate(args.outdir)
    print('Complete.')

# Copyright (c) 2014, Matt Layman
"""The main entry point for the tool"""

import argparse
import sys

from handroll.site import Site


def main():
    description = 'A website generator for software artisans'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('site', help='The path to your website')
    args = parser.parse_args()

    site = Site(args.site)
    if not site.is_valid():
        sys.exit('Incomplete.')

    print('Complete.')

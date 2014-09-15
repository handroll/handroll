# Copyright (c) 2014, Matt Layman

import logging
import os
import tempfile
import unittest

from handroll import logger
from handroll import command


class TestArguments(unittest.TestCase):

    def setUp(self):
        # argv will always start with the command.
        self.arguments = ['/fake/bin/handroll']

    def test_verbose_argument(self):
        args = command.parse_args(self.arguments)
        self.assertFalse(args.verbose)

        argv = list(self.arguments)
        argv.append('-v')
        args = command.parse_args(argv)
        self.assertTrue(args.verbose)

        argv = list(self.arguments)
        argv.append('--verbose')
        args = command.parse_args(argv)
        self.assertTrue(args.verbose)

    def test_debug_argument(self):
        args = command.parse_args(self.arguments)
        self.assertFalse(args.debug)

        argv = list(self.arguments)
        argv.append('-d')
        args = command.parse_args(argv)
        self.assertTrue(args.debug)

        argv = list(self.arguments)
        argv.append('--debug')
        args = command.parse_args(argv)
        self.assertTrue(args.debug)

    def test_timing_argument(self):
        args = command.parse_args(self.arguments)
        self.assertFalse(args.timing)

        argv = list(self.arguments)
        argv.append('-t')
        args = command.parse_args(argv)
        self.assertTrue(args.timing)

        argv = list(self.arguments)
        argv.append('--timing')
        args = command.parse_args(argv)
        self.assertTrue(args.timing)

    def test_site_argument(self):
        site = 'fake_site'
        self.arguments.append(site)
        args = command.parse_args(self.arguments)
        self.assertEqual(site, args.site)

    def test_outdir_argument(self):
        outdir = 'fake_outdir'
        self.arguments.extend(['fake_site', outdir])
        args = command.parse_args(self.arguments)
        self.assertEqual(outdir, args.outdir)


class TestMain(unittest.TestCase):

    def setUp(self):
        self.arguments = ['/fake/bin/handroll']

    def _make_valid_site(self):
        site = tempfile.mkdtemp()
        open(os.path.join(site, 'template.html'), 'w').close()
        return site

    def test_verbose_sets_logging(self):
        logger.setLevel(logging.CRITICAL)
        self.arguments.append('-v')
        self.assertRaises(SystemExit, command.main, self.arguments)
        self.assertEqual(logging.INFO, logger.getEffectiveLevel())

    def test_debug_sets_logging(self):
        logger.setLevel(logging.CRITICAL)
        self.arguments.append('-d')
        self.assertRaises(SystemExit, command.main, self.arguments)
        self.assertEqual(logging.DEBUG, logger.getEffectiveLevel())

    def test_site_directory_is_file(self):
        site = tempfile.mkdtemp()
        file_site = os.path.join(site, 'fake')
        self.arguments.append(file_site)
        self.assertRaises(SystemExit, command.main, self.arguments)

    def test_complete_site_generation(self):
        site = self._make_valid_site()
        self.arguments.append(site)
        try:
            command.main(self.arguments)
        except SystemExit:
            self.fail('Failed to completely generate site.')

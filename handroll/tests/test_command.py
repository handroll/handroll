# Copyright (c) 2014, Matt Layman

import unittest

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

# Copyright (c) 2014, Matt Layman

import logging
import os
import tempfile

import mock

from handroll import logger
from handroll import command
from handroll.tests import TestCase


class TestArguments(TestCase):

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

    def test_watch_argument(self):
        args = command.parse_args(self.arguments)
        self.assertFalse(args.watch)

        argv = list(self.arguments)
        argv.append('-w')
        args = command.parse_args(argv)
        self.assertTrue(args.watch)

        argv = list(self.arguments)
        argv.append('--watch')
        args = command.parse_args(argv)
        self.assertTrue(args.watch)

    def test_site_argument(self):
        site = 'fake_site'
        self.arguments.append(site)
        args = command.parse_args(self.arguments)
        self.assertEqual(site, args.site)

    def test_site_argument_is_normalized(self):
        """Test that trailing path separator is removed so that a site is
        consistently handled."""
        site = 'fake_site' + os.sep
        self.arguments.append(site)
        args = command.parse_args(self.arguments)
        self.assertEqual('fake_site', args.site)

    def test_outdir_argument(self):
        outdir = 'fake_outdir'
        self.arguments.extend(['fake_site', outdir])
        args = command.parse_args(self.arguments)
        self.assertEqual(outdir, args.outdir)


class TestMain(TestCase):

    def setUp(self):
        self.arguments = ['/fake/bin/handroll']

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
        site = self.factory.make_site()
        self.arguments.append(site.path)
        try:
            command.main(self.arguments)
        except SystemExit:
            self.fail('Failed to completely generate site.')

    @mock.patch('handroll.command.serve')
    def test_development_server_served(self, serve):
        site = self.factory.make_site()
        self.arguments.extend(['-w', site.path])

        command.main(self.arguments)

        self.assertTrue(serve.called)

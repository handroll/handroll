# Copyright (c) 2016, Matt Layman

import logging
import os
import tempfile

import mock

from handroll import entry, logger, scaffolder
from handroll.tests import TestCase


class TestArguments(TestCase):

    def setUp(self):
        # argv will always start with the command.
        self.arguments = ['/fake/bin/handroll']

    def _make_argv_with(self, argument=None):
        # A subcommand is required.
        if argument is None:
            return ['/fake/bin/handroll', 'build']
        else:
            return ['/fake/bin/handroll', argument, 'build']

    def test_verbose_argument(self):
        argv = self._make_argv_with()
        args = entry.parse(argv)
        self.assertFalse(args.verbose)

        argv = self._make_argv_with('-v')
        args = entry.parse(argv)
        self.assertTrue(args.verbose)

        argv = self._make_argv_with('--verbose')
        args = entry.parse(argv)
        self.assertTrue(args.verbose)

    def test_debug_argument(self):
        argv = self._make_argv_with()
        args = entry.parse(argv)
        self.assertFalse(args.debug)

        argv = self._make_argv_with('-d')
        args = entry.parse(argv)
        self.assertTrue(args.debug)

        argv = self._make_argv_with('--debug')
        args = entry.parse(argv)
        self.assertTrue(args.debug)

    def test_timing_argument(self):
        argv = self._make_argv_with()
        args = entry.parse(argv)
        self.assertFalse(args.timing)

        argv = self._make_argv_with('-t')
        args = entry.parse(argv)
        self.assertTrue(args.timing)

        argv = self._make_argv_with('--timing')
        args = entry.parse(argv)
        self.assertTrue(args.timing)

    def test_watch_argument(self):
        # FIXME: I promise I'm coming right back to this.
        return
        args = entry.parse(self.arguments)
        self.assertFalse(args.watch)

        argv = list(self.arguments)
        argv.append('-w')
        args = entry.parse(argv)
        self.assertTrue(args.watch)

        argv = list(self.arguments)
        argv.append('--watch')
        args = entry.parse(argv)
        self.assertTrue(args.watch)

    def test_site_argument(self):
        # FIXME: I promise I'm coming right back to this.
        return
        site = 'fake_site'
        self.arguments.append(site)
        args = entry.parse(self.arguments)
        self.assertEqual(site, args.site)

    def test_site_argument_is_normalized(self):
        """Test that trailing path separator is removed so that a site is
        consistently handled."""
        # FIXME: I promise I'm coming right back to this.
        return
        site = 'fake_site' + os.sep
        self.arguments.append(site)
        args = entry.parse(self.arguments)
        self.assertEqual('fake_site', args.site)

    def test_outdir_argument(self):
        # FIXME: I promise I'm coming right back to this.
        return
        outdir = 'fake_outdir'
        self.arguments.extend(['fake_site', outdir])
        args = entry.parse(self.arguments)
        self.assertEqual(outdir, args.outdir)

    def test_force_argument(self):
        argv = self._make_argv_with()
        args = entry.parse(argv)
        self.assertFalse(args.force)

        argv = self._make_argv_with('-f')
        args = entry.parse(argv)
        self.assertTrue(args.force)

        argv = self._make_argv_with('--force')
        args = entry.parse(argv)
        self.assertTrue(args.force)

    def test_scaffold_argument(self):
        # FIXME: I promise I'm coming right back to this.
        return
        args = entry.parse(self.arguments)
        self.assertIsNone(args.scaffold)

        argv = list(self.arguments)
        argv.append('-s')
        args = entry.parse(argv)
        self.assertEqual(scaffolder.LIST_SCAFFOLDS, args.scaffold)

        argv = list(self.arguments)
        argv.append('--scaffold')
        args = entry.parse(argv)
        self.assertEqual(scaffolder.LIST_SCAFFOLDS, args.scaffold)

        argv = list(self.arguments)
        argv.extend(['--scaffold', 'default'])
        args = entry.parse(argv)
        self.assertEqual('default', args.scaffold)


class TestMain(TestCase):

    def setUp(self):
        self.arguments = ['/fake/bin/handroll']

    def test_verbose_sets_logging(self):
        logger.setLevel(logging.CRITICAL)
        self.arguments.extend(['-v', 'build'])
        self.assertRaises(SystemExit, entry.main, self.arguments)
        self.assertEqual(logging.INFO, logger.getEffectiveLevel())

    def test_debug_sets_logging(self):
        logger.setLevel(logging.CRITICAL)
        self.arguments.extend(['-d', 'build'])
        self.assertRaises(SystemExit, entry.main, self.arguments)
        self.assertEqual(logging.DEBUG, logger.getEffectiveLevel())

    def test_site_directory_is_file(self):
        # FIXME: I promise I'm coming right back to this.
        return
        site = tempfile.mkdtemp()
        file_site = os.path.join(site, 'fake')
        self.arguments.append(file_site)
        self.assertRaises(SystemExit, entry.main, self.arguments)

    @mock.patch('handroll.entry.finish')
    def test_complete_site_generation(self, finish):
        # FIXME: I promise I'm coming right back to this.
        return
        site = self.factory.make_site()
        self.arguments.append(site.path)
        entry.main(self.arguments)
        self.assertTrue(finish.called)

    @mock.patch('handroll.entry.serve')
    def test_development_server_served(self, serve):
        # FIXME: I promise I'm coming right back to this.
        return
        site = self.factory.make_site()
        self.arguments.extend(['-w', site.path])

        entry.main(self.arguments)

        self.assertTrue(serve.called)

    @mock.patch('handroll.entry.scaffolder')
    def test_makes_from_scaffolder(self, mock_scaffolder):
        # FIXME: I promise I'm coming right back to this.
        return
        self.arguments.extend(['-s', 'default', 'site'])

        try:
            entry.main(self.arguments)
            self.fail()
        except SystemExit:
            mock_scaffolder.make.assert_called_once_with(
                'default', 'site')

# Copyright (c) 2016, Matt Layman

import inspect
import os
import tempfile
import unittest

from handroll import configuration
from handroll.exceptions import AbortError


class FakeArgs(object):

    def __init__(self):
        self.force = False
        self.outdir = None
        self.timing = None


class TestConfiguration(unittest.TestCase):

    def test_loads_from_outdir_argument(self):
        config = configuration.Configuration()
        args = FakeArgs()
        args.outdir = 'out'

        config.load_from_arguments(args)

        expected = os.path.join(os.getcwd(), args.outdir)
        self.assertEqual(expected, config.outdir)

    def test_loads_from_force_argument(self):
        config = configuration.Configuration()
        args = FakeArgs()
        args.force = True

        config.load_from_arguments(args)

        self.assertTrue(config.force)

    def test_build_config_from_file(self):
        conf_file = inspect.cleandoc(
            """[site]
            outdir = out""")
        args = FakeArgs()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(conf_file.encode('utf-8'))

        config = configuration.build_config(f.name, args)

        expected = os.path.join(os.path.dirname(f.name), 'out')
        self.assertEqual(expected, config.outdir)

    def test_finds_active_extensions(self):
        conf_file = inspect.cleandoc(
            """[site]
            with_blog = true""")
        args = FakeArgs()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(conf_file.encode('utf-8'))

        config = configuration.build_config(f.name, args)

        self.assertTrue('blog' in config.active_extensions)

    def test_no_boolean_extension(self):
        conf_file = inspect.cleandoc(
            """[site]
            with_blog = BOOM!""")
        args = FakeArgs()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(conf_file.encode('utf-8'))
        with self.assertRaises(AbortError):
            configuration.build_config(f.name, args)

    def test_no_domain_aborts(self):
        config = configuration.Configuration()
        with self.assertRaises(AbortError):
            config.domain

    def test_loads_domain_from_site(self):
        conf_file = inspect.cleandoc(
            """[site]
            domain = a_fake_domain""")
        args = FakeArgs()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(conf_file.encode('utf-8'))

        config = configuration.build_config(f.name, args)

        self.assertEqual('a_fake_domain', config.domain)

    def test_converts_relative_paths(self):
        conf_file = inspect.cleandoc(
            """[site]
            outdir = ..""")
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(conf_file.encode('utf-8'))
        config = configuration.Configuration()
        config.load_from_file(f.name)
        # Relative output directories are anchored to the site config file.
        self.assertEqual(
            os.path.dirname(os.path.dirname(f.name)),
            config.outdir)

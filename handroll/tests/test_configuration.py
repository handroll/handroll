# Copyright (c) 2014, Matt Layman

import inspect
import os
import tempfile
import unittest

from handroll import configuration


class FakeArgs(object):

    def __init__(self):
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

    def test_build_config_from_file(self):
        conf_file = inspect.cleandoc(
            """[site]
            outdir = out""")
        args = FakeArgs()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(conf_file.encode('utf-8'))

        config = configuration.build_config(f.name, args)

        expected = os.path.join(os.getcwd(), 'out')
        self.assertEqual(expected, config.outdir)

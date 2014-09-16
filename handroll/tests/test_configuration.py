# Copyright (c) 2014, Matt Layman

import inspect
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

        self.assertEqual(args.outdir, config.outdir)

    def test_build_config_from_file(self):
        conf_file = inspect.cleandoc(
            """[site]
            outdir = out""")
        print conf_file
        args = FakeArgs()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(conf_file)

        config = configuration.build_config(f.name, args)

        self.assertEqual('out', config.outdir)

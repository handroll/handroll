# Copyright (c) 2014, Matt Layman

import os
import tempfile

import mock

from handroll.configuration import Configuration
from handroll.director import Director
from handroll.site import Site
from handroll.tests import TestCase


class TestDirector(TestCase):

    def test_generates_with_user_specified_outdir(self):
        config = Configuration()
        config.outdir = tempfile.mkdtemp()
        site = self.factory.make_site()
        marker = 'marker.txt'
        open(os.path.join(site.path, marker), 'w').close()
        director = Director(config, site)

        director.produce()

        out_marker = os.path.join(config.outdir, marker)
        self.assertTrue(os.path.exists(out_marker))

    def test_skips_file_with_skip_extension(self):
        config = Configuration()
        site = self.factory.make_site()
        skip = 'to_my_lou.swp'
        open(os.path.join(site.path, skip), 'w').close()
        director = Director(config, site)

        director.produce()

        out_skip = os.path.join(site.output_root, skip)
        self.assertFalse(os.path.exists(out_skip))

    def test_skips_file_in_skip_list(self):
        config = Configuration()
        site = self.factory.make_site()
        skip = Site.CONFIG
        open(os.path.join(site.path, skip), 'w').close()
        director = Director(config, site)

        director.produce()

        out_skip = os.path.join(site.output_root, skip)
        self.assertFalse(os.path.exists(out_skip))

    def test_skips_templates_directory(self):
        config = Configuration()
        site = self.factory.make_site()
        templates = os.path.join(site.path, 'templates')
        os.mkdir(templates)
        director = Director(config, site)

        director.produce()

        out_templates = os.path.join(site.output_root, 'templates')
        self.assertFalse(os.path.exists(out_templates))

    def test_does_timing(self):
        mock_time = mock.Mock()
        mock_time.return_value = 42.0  # Return float so that format works.
        site = self.factory.make_site()
        open(os.path.join(site.path, 'fake.md'), 'w').close()
        config = Configuration()
        config.timing = True
        director = Director(config, site)

        with mock.patch('handroll.director.time.time', mock_time):
            director.produce()

        self.assertTrue(mock_time.called)

    def test_generates_output_directory(self):
        config = Configuration()
        site = self.factory.make_site()
        another = os.path.join(site.path, 'another')
        os.mkdir(another)
        director = Director(config, site)

        director.produce()

        another_out = os.path.join(site.output_root, 'another')
        self.assertTrue(os.path.isdir(another_out))

    def test_skips_directory(self):
        dirnames = ['keep', '.sass-cache', 'another_keeper']
        site = self.factory.make_site()
        config = Configuration()
        director = Director(config, site)

        director.prune_skip_directories(dirnames)

        self.assertEqual(2, len(dirnames))
        self.assertEqual('keep', dirnames[0])
        self.assertEqual('another_keeper', dirnames[1])

    def test_process_file_ignores_files_already_in_output(self):
        # This condition is checked because the output directory can be within
        # the source (e.g., the default of storing results in 'output'). If
        # the watcher is watching for any changes in site source, then
        # processing files in the output directory could lead the watcher into
        # an infinite loop.
        config = Configuration()
        site = self.factory.make_site()
        config.outdir = os.path.join(site.path, 'outdir')
        os.mkdir(config.outdir)
        marker = os.path.join(config.outdir, 'marker.md')
        open(marker, 'w').close()
        director = Director(config, site)

        director.process_file(marker)

        marker_output = os.path.join(config.outdir, 'marker.html')
        self.assertFalse(os.path.exists(marker_output))

    def test_process_directory_ignores_directories_already_in_output(self):
        # Avoid processing directories in output for the same reason that
        # file processing is skipped.
        config = Configuration()
        site = self.factory.make_site()
        config.outdir = os.path.join(site.path, 'outdir')
        os.mkdir(config.outdir)
        directory = os.path.join(config.outdir, 'directory')
        os.mkdir(directory)
        director = Director(config, site)

        director.process_directory(directory)

        directory_output = os.path.join(config.outdir, 'outdir', 'directory')
        self.assertFalse(os.path.exists(directory_output))

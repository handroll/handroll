# Copyright (c) 2016, Matt Layman

import os
import tempfile

from watchdog import events

from handroll.configuration import Configuration
from handroll.director import Director
from handroll.handlers import SiteHandler
from handroll.tests import TestCase


class TestSiteHandler(TestCase):

    def setUp(self):
        config = Configuration()
        config.outdir = tempfile.mkdtemp()
        self.site = self.factory.make_site()
        self.director = Director(config, self.site, [])

    def test_on_create_generates_output(self):
        markdown = os.path.join(self.site.path, 'index.md')
        open(markdown, 'w').close()
        handler = SiteHandler(self.director)
        event = events.FileCreatedEvent(markdown)

        handler.on_created(event)

        html = os.path.join(self.director.config.outdir, 'index.html')
        self.assertTrue(os.path.exists(html))

    def test_on_create_generates_directory(self):
        """Test that creation of a directory in the site source creates a
        directory in the output."""
        directory = os.path.join(self.site.path, 'directory')
        os.mkdir(directory)
        handler = SiteHandler(self.director)
        event = events.DirCreatedEvent(directory)

        handler.on_created(event)

        out_directory = os.path.join(self.director.config.outdir, 'directory')
        self.assertTrue(os.path.exists(out_directory))
        self.assertTrue(os.path.isdir(out_directory))

    def test_on_modified_regenerates_output(self):
        markdown = os.path.join(self.site.path, 'index.md')
        open(markdown, 'w').close()
        handler = SiteHandler(self.director)
        event = events.FileModifiedEvent(markdown)

        handler.on_modified(event)

        html = os.path.join(self.director.config.outdir, 'index.html')
        self.assertTrue(os.path.exists(html))

    def test_on_moved_for_file_regenerates_output(self):
        markdown = os.path.join(self.site.path, 'index.md')
        open(markdown, 'w').close()
        handler = SiteHandler(self.director)
        event = events.FileMovedEvent('', markdown)

        handler.on_moved(event)

        html = os.path.join(self.director.config.outdir, 'index.html')
        self.assertTrue(os.path.exists(html))

    def test_on_moved_for_directory_makes_new_directory(self):
        directory = os.path.join(self.site.path, 'directory')
        os.mkdir(directory)
        handler = SiteHandler(self.director)
        event = events.DirMovedEvent('', directory)

        handler.on_moved(event)

        out_directory = os.path.join(self.director.config.outdir, 'directory')
        self.assertTrue(os.path.exists(out_directory))
        self.assertTrue(os.path.isdir(out_directory))

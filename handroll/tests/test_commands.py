# Copyright (c) 2016, Matt Layman

import mock

from handroll.commands import Command
from handroll.commands.build import BuildCommand
from handroll.tests import TestCase


class TestCommand(TestCase):

    def test_register_not_implemented(self):
        parser = mock.Mock()
        self.assertRaises(NotImplementedError, Command.register, parser)

    def test_run_not_implemented(self):
        args = mock.Mock()
        command = Command()
        self.assertRaises(NotImplementedError, command.run, args)


class TestBuildCommand(TestCase):

    @mock.patch('handroll.commands.build.finish')
    def test_complete_build(self, finish):
        site = self.factory.make_site()
        args = mock.Mock(site=site.path, outdir='.')
        command = BuildCommand()
        command.run(args)
        self.assertTrue(finish.called)

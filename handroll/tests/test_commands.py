# Copyright (c) 2016, Matt Layman

import mock

from handroll.commands import Command
from handroll.commands.build import BuildCommand
from handroll.tests import TestCase


class TestCommand(TestCase):

    def test_register_returns_parser(self):
        subparsers = mock.Mock()
        expected_parser = mock.Mock()
        subparsers.add_parser.return_value = expected_parser
        command = Command()
        parser = command.register(subparsers)
        self.assertEqual(expected_parser, parser)

    def test_register_command_attributes(self):
        subparsers = mock.Mock()
        command = Command()
        command.register(subparsers)
        subparsers.add_parser.assert_called_once_with(
            'command', description='the command description',
            help='the command help')

    def test_register_run_as_func(self):
        subparsers = mock.Mock()
        command = Command()
        parser = command.register(subparsers)
        parser.set_defaults.assert_called_once_with(func=command.run)

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

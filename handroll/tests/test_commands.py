# Copyright (c) 2016, Matt Layman

import mock

from handroll.commands import Command
from handroll.commands.base import finish
from handroll.commands.build import BuildCommand
from handroll.commands.scaffold import ScaffoldCommand
from handroll.commands.watch import WatchCommand
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
        with self.assertRaises(NotImplementedError):
            command.run(args)

    def test_finish(self):
        with self.assertRaises(SystemExit):
            finish()


class TestBuildCommand(TestCase):

    def test_register_site(self):
        parser = mock.Mock()
        subparsers = mock.Mock()
        subparsers.add_parser.return_value = parser
        command = BuildCommand()
        command.register(subparsers)
        site_call = (('site',), {'nargs': '?', 'help': mock.ANY})
        self.assertIn(site_call, parser.add_argument.call_args_list)

    def test_register_outdir(self):
        parser = mock.Mock()
        subparsers = mock.Mock()
        subparsers.add_parser.return_value = parser
        command = BuildCommand()
        command.register(subparsers)
        outdir_call = (('outdir',), {'nargs': '?', 'help': mock.ANY})
        self.assertIn(outdir_call, parser.add_argument.call_args_list)

    @mock.patch('handroll.commands.build.finish')
    def test_complete_build(self, finish):
        site = self.factory.make_site()
        args = mock.Mock(site=site.path, outdir='.')
        command = BuildCommand()
        command.run(args)
        self.assertTrue(finish.called)


class TestWatchCommand(TestCase):

    def test_register_site(self):
        parser = mock.Mock()
        subparsers = mock.Mock()
        subparsers.add_parser.return_value = parser
        command = WatchCommand()
        command.register(subparsers)
        site_call = (('site',), {'nargs': '?', 'help': mock.ANY})
        self.assertIn(site_call, parser.add_argument.call_args_list)

    def test_register_outdir(self):
        parser = mock.Mock()
        subparsers = mock.Mock()
        subparsers.add_parser.return_value = parser
        command = WatchCommand()
        command.register(subparsers)
        outdir_call = (('outdir',), {'nargs': '?', 'help': mock.ANY})
        self.assertIn(outdir_call, parser.add_argument.call_args_list)

    @mock.patch('handroll.commands.watch.serve')
    def test_complete_watch(self, serve):
        site = self.factory.make_site()
        args = mock.Mock(site=site.path, outdir='.')
        command = WatchCommand()
        command.run(args)
        self.assertTrue(serve.called)


class TestScaffoldCommand(TestCase):

    def test_register_scaffold(self):
        parser = mock.Mock()
        subparsers = mock.Mock()
        subparsers.add_parser.return_value = parser
        command = ScaffoldCommand()
        command.register(subparsers)
        scaffold_call = (('scaffold',), {'nargs': '?', 'help': mock.ANY})
        self.assertIn(scaffold_call, parser.add_argument.call_args_list)

    def test_register_site(self):
        parser = mock.Mock()
        subparsers = mock.Mock()
        subparsers.add_parser.return_value = parser
        command = ScaffoldCommand()
        command.register(subparsers)
        site_call = (('site',), {
            'nargs': '?', 'help': mock.ANY, 'default': 'site'})
        self.assertIn(site_call, parser.add_argument.call_args_list)

    @mock.patch('handroll.commands.scaffold.scaffolder.list_scaffolds')
    def test_lists_scaffolds(self, list_scaffolds):
        args = mock.Mock(scaffold=None)
        command = ScaffoldCommand()
        command.run(args)
        self.assertTrue(list_scaffolds.called)

    @mock.patch('handroll.commands.scaffold.finish')
    @mock.patch('handroll.commands.scaffold.scaffolder.make')
    def test_complete_scaffold(self, make, finish):
        args = mock.Mock(scaffold='default', site='site')
        command = ScaffoldCommand()
        command.run(args)
        make.assert_called_once_with('default', 'site')

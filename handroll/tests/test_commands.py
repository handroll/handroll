# Copyright (c) 2016, Matt Layman

import mock

from handroll.commands import Command
from handroll.tests import TestCase


class TestCommand(TestCase):

    def test_register_not_implemented(self):
        parser = mock.Mock()
        self.assertRaises(NotImplementedError, Command.register, parser)

    def test_run_not_implemented(self):
        args = mock.Mock()
        command = Command()
        self.assertRaises(NotImplementedError, command.run, args)

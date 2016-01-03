# Copyright (c) 2016, Matt Layman


class Command(object):
    """A command class with the minimal interface required for each command."""

    @classmethod
    def register(cls, parser):
        """Register required options.

        The provided parser is a subparser from ``subparsers.add_parser``.
        """
        raise NotImplementedError()

    def run(self, args):
        """Run whatever action the command intends."""
        raise NotImplementedError()

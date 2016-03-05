# Copyright (c) 2016, Matt Layman

from handroll.commands.base import Command
from handroll.i18n import _


class ScaffoldCommand(Command):

    name = 'scaffold'
    description = _(
        'Make a new handroll site from a scaffold '
        'or list the available scaffolds')
    help = _('make a new handroll site')

    def register(self, subparsers):
        parser = super(ScaffoldCommand, self).register(subparsers)
        parser.add_argument(
            'site', nargs='?', help=_('the path to your website'))

    def run(self, args):
        # TODO: list the scaffolds
        # TODO: remove LIST_SCAFFOLDS constant
        # TODO: Make `make` simpler by putting switching logic in command.
        pass
        # scaffolder.make(args.scaffold, args.site)
        # finish()

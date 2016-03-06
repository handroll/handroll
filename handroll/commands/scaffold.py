# Copyright (c) 2016, Matt Layman

from handroll.commands.base import Command, finish
from handroll.i18n import _
from handroll import scaffolder


class ScaffoldCommand(Command):

    name = 'scaffold'
    description = _(
        'Make a new handroll site from a scaffold '
        'or list the available scaffolds')
    help = _('make a new handroll site')

    def register(self, subparsers):
        parser = super(ScaffoldCommand, self).register(subparsers)
        parser.add_argument(
            'scaffold', nargs='?', help=_('the scaffold to generate'))
        parser.add_argument(
            'site', nargs='?', default='site',
            help=_('the path to your website'))

    def run(self, args):
        if args.scaffold:
            scaffolder.make(args.scaffold, args.site)
            finish()
        else:
            scaffolder.list_scaffolds()

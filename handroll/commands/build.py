# Copyright (c) 2016, Matt Layman

from handroll.commands.base import Command, finish, prepare_director
from handroll.i18n import _
from handroll.site import Site


class BuildCommand(Command):

    name = 'build'
    description = _('Build a site in an output directory.')
    help = _('build a site')

    def register(self, subparsers):
        parser = super(BuildCommand, self).register(subparsers)
        parser.add_argument(
            'site', nargs='?', help=_('the path to your website'))
        parser.add_argument('outdir', nargs='?', help=_(
            'an optional output directory to create or'
            ' update if it already exists'))

    def run(self, args):
        site = Site.build(args)
        director = prepare_director(args, site)
        director.produce()
        finish()

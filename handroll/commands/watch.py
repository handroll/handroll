# Copyright (c) 2016, Matt Layman

from handroll.commands.base import Command, prepare_director
from handroll.i18n import _
from handroll.server import serve
from handroll.site import Site


class WatchCommand(Command):

    name = 'watch'
    description = _(
        'watch the site for changes and'
        ' run a web server in the output directory')
    help = _('watch a site and run a web server')

    def register(self, subparsers):
        parser = super(WatchCommand, self).register(subparsers)
        parser.add_argument(
            'site', nargs='?', help=_('the path to your website'))
        parser.add_argument('outdir', nargs='?', help=_(
            'an optional output directory to create or'
            ' update if it already exists'))

    def run(self, args):
        site = Site.build(args)
        director = prepare_director(args, site)
        director.produce()
        serve(site, director)

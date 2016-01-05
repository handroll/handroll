# Copyright (c) 2016, Matt Layman

from handroll.commands.base import Command, finish, prepare_director
from handroll.i18n import _
from handroll.site import Site


class BuildCommand(Command):

    name = 'build'
    description = _('Build a site in an output directory.')
    help = _('build a site')

    def run(self, args):
        site = Site.build(args)
        director = prepare_director(args, site)
        director.produce()
        finish()

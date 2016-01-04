# Copyright (c) 2016, Matt Layman

from handroll.commands.base import Command, finish, prepare_director
from handroll.site import Site


class BuildCommand(Command):

    def run(self, args):
        site = Site.build(args)
        director = prepare_director(args, site)
        director.produce()
        finish()

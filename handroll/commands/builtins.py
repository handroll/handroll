# Copyright (c) 2017, Matt Layman

from handroll.commands.build import BuildCommand
from handroll.commands.scaffold import ScaffoldCommand
from handroll.commands.watch import WatchCommand

COMMANDS = [
    BuildCommand(),
    WatchCommand(),
    ScaffoldCommand(),
]

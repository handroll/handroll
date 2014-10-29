# Copyright (c) 2014, Matt Layman

from watchdog.events import FileSystemEventHandler


class SiteHandler(FileSystemEventHandler):
    """The ``SiteHandler`` listens for file systems events and passes
    information to the director to generate the appropriate output based on
    changes.
    """

    def __init__(self, director):
        self.director = director

    def on_created(self, event):
        # TODO: handle the event
        print 'on created'

    def on_modified(self, event):
        # TODO: handle the event
        print 'on modified'

    def on_moved(self, event):
        # TODO: handle the event
        print 'on moved'

# Copyright (c) 2016, Matt Layman

from watchdog.events import FileSystemEventHandler


class SiteHandler(FileSystemEventHandler):
    """The ``SiteHandler`` listens for file systems events and passes
    information to the director to generate the appropriate output based on
    changes.
    """

    def __init__(self, director):
        self.director = director

    def on_created(self, event):
        if event.is_directory:
            self.director.process_directory(event.src_path)
        else:
            self.director.process_file(event.src_path)

    def on_modified(self, event):
        # Only pay attention to modified files, not directories.
        if not event.is_directory:
            self.director.process_file(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            self.director.process_directory(event.dest_path)
        else:
            self.director.process_file(event.dest_path)

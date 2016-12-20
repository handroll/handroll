# Copyright (c) 2016, Matt Layman

import logging
import os
try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:  # pragma: no cover
    # Python 3 moved the server.
    from http.server import SimpleHTTPRequestHandler
try:
    import SocketServer as socketserver
except ImportError:  # pragma: no cover
    # Python 3 renamed the SocketServer module.
    import socketserver

from watchdog.observers import Observer

from handroll import logger
from handroll.handlers import SiteHandler
from handroll.i18n import _

# Maybe the port should be configurable later. For now, go with a static value.
PORT = 8000


def serve(site, director):
    """Run a simple web server that serve the output directory and watches for
    changes to the site. When something is changed, it should be generated.
    """
    # Override the log level to display some interactive messages with the
    # user. With the dev server running, there's no sense in being silent.
    logger.setLevel(logging.INFO)

    # Start the watchdog.
    event_handler = SiteHandler(director)
    observer = Observer()
    observer.schedule(event_handler, site.path, recursive=True)
    observer.start()

    # The simple HTTP server is pretty dumb and does not even take a path to
    # serve. The only way to serve the right path is to change the directory.
    outdir = director.outdir
    os.chdir(outdir)

    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('', PORT), SimpleHTTPRequestHandler)

    logger.info(
        _('Serving {outdir} at http://localhost:{port}/.'
          '\nPress Ctrl-C to quit.').format(outdir=outdir, port=PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info(_('\nBye.'))
        observer.stop()

    observer.join()

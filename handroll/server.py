# Copyright (c) 2014, Matt Layman

import logging
import os
import SimpleHTTPServer
import SocketServer

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
    outdir = director.lookup_outdir()
    os.chdir(outdir)

    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(('', PORT), handler)

    logger.info(
        _('Serving {outdir} at http://localhost:{port}/.'
          ' Press Ctrl-C to quit.'.format(outdir=outdir, port=PORT)))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info(_('\nBye.'))
        observer.stop()

    observer.join()

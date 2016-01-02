# Copyright (c) 2016, Matt Layman

import tempfile

import mock

from handroll.configuration import Configuration
from handroll.director import Director
from handroll.server import serve
from handroll.tests import TestCase


class TestServer(TestCase):

    def setUp(self):
        config = Configuration()
        config.outdir = tempfile.mkdtemp()
        self.site = self.factory.make_site()
        self.director = Director(config, self.site, [])

    @mock.patch('handroll.server.Observer')
    @mock.patch('handroll.server.socketserver.TCPServer')
    def test_serves_forever(self, tcp_server, observer_cls):
        httpd = mock.MagicMock()
        tcp_server.return_value = httpd
        observer = mock.MagicMock()
        observer_cls.return_value = observer

        serve(self.site, self.director)

        self.assertTrue(httpd.serve_forever.called)
        self.assertTrue(observer.start.called)

    @mock.patch('handroll.server.Observer')
    @mock.patch('handroll.server.socketserver.TCPServer')
    def test_server_quits_on_keyboard_interrupt(
            self, tcp_server, observer_cls):
        httpd = mock.MagicMock()
        httpd.serve_forever.side_effect = KeyboardInterrupt
        tcp_server.return_value = httpd
        observer = mock.MagicMock()
        observer_cls.return_value = observer

        try:
            serve(self.site, self.director)
        except KeyboardInterrupt:
            self.fail('Server did not quit gracefully.')
        self.assertTrue(observer.stop.called)

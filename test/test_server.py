import os.path
import pytest
import sys

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestServer(object):
    def setup_method(self, method):
        from browsermobproxy.server import Server
        self.server = Server()

    def teardown_method(self, method):
        self.server.stop()

    def test_start_server_with_default_arguments(self):
        """
            Checks default arguments on starting the server
        """
        self.server.start()
        assert(len(self.server.command) == 2)
        assert(self.server.command[1].find('--port') >= 0)
        
    def test_start_server_with_legacy_implementations(self):
        """
            Checks the boolean true value in the legacy_mode key passed in options dictionary
        """
        from browsermobproxy.server import Server
        self.server = Server(options={'legacy_mode':True})
        self.server.start()
        assert(len(self.server.command) >= 3)
        assert(self.server.command[1].find('--use-littleproxy=False') >= 0)

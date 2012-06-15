import os.path
import pytest
import sys

def setup_module(module):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestClient(object):
    def setup_method(self, method):
        from browsermobproxy.client import Client
        self.client = Client("http://localhost:9090")
        
    def teardown_method(self, method):
        pass
        
    def test_headers_type(self):
        with pytest.raises(TypeError):
            self.client.headers(['foo'])

    def test_headers_content(self):
        s = self.client.headers({'User-Agent': 'rubber ducks floating in a row'})
        assert(s == 200)
    
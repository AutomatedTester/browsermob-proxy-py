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
        self.client.close()

    def test_headers_type(self):
        """
        /proxy/:port/headers needs to take a dictionary
        """
        with pytest.raises(TypeError):
            self.client.headers(['foo'])

    def test_headers_content(self):
        """
        /proxy/:port/headers needs to take a dictionary
        and returns 200 when its successful
        """
        s = self.client.headers({'User-Agent': 'rubber ducks floating in a row'})
        assert(s == 200)

    def test_hosts_type(self):
        """
        /proxy/:port/hosts needs to take a dictionary
        """
        with pytest.raises(TypeError):
            self.client.hosts(['foo'])

    def test_hosts_content(self):
        """
        /proxy/:port/hosts needs to take a dictionary
        and returns 200 when its successful
        """
        s = self.client.hosts({'www.example.com': '127.0.0.1'})
        assert(s == 200)

    def test_new_har(self):
        """
        /proxy/:port/har
        and returns 204 when creating a har with a particular name the first time
        and returns 200 and the previous har when creating one with the same name
        """
        status_code, har = self.client.new_har()
        assert(status_code == 204)
        assert(har is None)
        status_code, har = self.client.new_har()
        assert(status_code == 200)
        assert('log' in har)

    def test_new_har(self):
        """
        /proxy/:port/har
        and returns 204 when creating a har with a particular name the first time
        and returns 200 and the previous har when creating one with the same name
        """
        status_code, har = self.client.new_har("elephants")
        assert(status_code == 204)
        assert(har is None)
        status_code, har = self.client.new_har("elephants")
        assert(status_code == 200)
        assert('elephants' == har["log"]["pages"][0]['id'])

    def test_new_page_defaults(self):
        """
        /proxy/:port/pageRef
        adds a new page of 'Page N' when no page name is given
        """
        self.client.new_har()
        self.client.new_page()
        har = self.client.har
        assert(len(har["log"]["pages"]) == 2)
        assert(har["log"]["pages"][1]["id"] == "Page 2")

    def test_new_named_page(self):
        """
        /proxy/:port/pageRef
        adds a new page of 'buttress'
        """
        self.client.new_har()
        self.client.new_page('buttress')
        har = self.client.har
        assert(len(har["log"]["pages"]) == 2)
        assert(har["log"]["pages"][1]["id"] == "buttress")

    def test_single_whitelist(self):
        """
        /proxy/:port/whitelist
        adds a whitelist
        """
        status_code = self.client.whitelist("http://www\\.facebook\\.com/.*", 200)
        assert(status_code == 200)

    def test_multiple_whitelists(self):
        """
        /proxy/:port/whitelist
        adds a whitelist
        """
        status_code = self.client.whitelist("http://www\\.facebook\\.com/.*,http://cdn\\.twitter\\.com", 200)
        assert(status_code == 200)

    def test_blacklist(self):
        """
        /proxy/:port/blacklist
        adds a blacklist
        """
        status_code = self.client.blacklist("http://www\\.facebook\\.com/.*", 200)
        assert(status_code == 200)

    def test_limits_invalid_key(self):
        """
        /proxy/:port/limits
        pre-sending checking that the parameter is correct
        """
        with pytest.raises(KeyError):
            self.client.limits({"hurray": "explosions"})

    def test_limits_key_no_value(self):
        """
        /proxy/:port/limits
        pre-sending checking that a parameter exists
        """
        with pytest.raises(KeyError):
            self.client.limits({})

    def test_limits_key_no_value(self):
        """
        /proxy/:port/limits
        can send all 3 at once based on the proxy implementation
        """
        limits = {"upstream_kbps": 320, "downstream_kbps": 560, "latency": 30}
        status_code = self.client.limits(limits)
        assert(status_code == 200)

    def test_close(self):
        """
        /proxy/:port
        close the proxy port
        """
        status_code = self.client.close()
        assert(status_code == 200)
        status_code = self.client.close()
        assert(status_code == 500)

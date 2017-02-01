from os import environ

from selenium import webdriver
import selenium.webdriver.common.desired_capabilities
from selenium.webdriver.common.proxy import Proxy
import os
import sys
import copy
import pytest

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestWebDriver(object):
    def setup_method(self, method):
        from browsermobproxy.client import Client
        self.client = Client("localhost:9090")
        self.driver = None

    def teardown_method(self, method):
        self.client.close()
        if self.driver is not None:
            self.driver.quit()

    @pytest.mark.human
    def test_i_want_my_by_capability(self):
        capabilities = selenium.webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
        self.client.add_to_capabilities(capabilities)
        # sets self.driver for proper clean up
        self._create_webdriver(capabilites=capabilities)

        self._run_url_rewrite_test()

    @pytest.mark.human
    def test_i_want_my_by_proxy_object(self):
        self._create_webdriver(capabilites=selenium.webdriver.common.desired_capabilities.DesiredCapabilities.CHROME,
                               proxy=self.client)

        self._run_url_rewrite_test()

    def test_what_things_look_like(self):
        bmp_capabilities = copy.deepcopy(selenium.webdriver.common.desired_capabilities.DesiredCapabilities.FIREFOX)
        self.client.add_to_capabilities(bmp_capabilities)

        proxy_capabilities = copy.deepcopy(selenium.webdriver.common.desired_capabilities.DesiredCapabilities.FIREFOX)
        proxy_addr = 'localhost:%d' % self.client.port
        proxy = Proxy({'httpProxy': proxy_addr,'sslProxy': proxy_addr})
        proxy.add_to_capabilities(proxy_capabilities)

        assert bmp_capabilities == proxy_capabilities

    def _create_webdriver(self, capabilites, proxy=None):
        chrome_binary = environ.get("CHROME_BIN", None)
        if chrome_binary is not None:
            capabilites.update({
                "chromeOptions": {
                    "binary": chrome_binary,
                    "args": ['no-sandbox']
                }
            })
        if proxy is None:
            self.driver = webdriver.Remote(desired_capabilities=capabilites)
        else:
            self.driver = webdriver.Remote(desired_capabilities=capabilites, proxy=proxy)

    def _run_url_rewrite_test(self):
        targetURL = "https://www.saucelabs.com/versions.js"
        assert 200 == self.client.rewrite_url(
            "https://www.saucelabs.com/versions.+", "https://www.saucelabs.com/versions.json"
        )
        self.driver.get(targetURL)
        assert "Sauce Connect" in self.driver.page_source
        assert self.client.clear_all_rewrite_url_rules() == 200
        self.driver.get(targetURL)
        assert "Sauce Connect" not in self.driver.page_source

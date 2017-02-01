from os import environ

from selenium import webdriver
import selenium.webdriver.common.desired_capabilities
import os
import sys
import pytest


def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestRemote(object):
    def setup_method(self, method):
        from browsermobproxy.client import Client
        self.client = Client("localhost:9090")
        chrome_binary = environ.get("CHROME_BIN", None)
        self.desired_caps = selenium.webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
        if chrome_binary is not None:
            self.desired_caps.update({
                "chromeOptions": {
                    "binary": chrome_binary,
                    "args": ['no-sandbox']
                }
            })
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_caps,
            proxy=self.client)

    def teardown_method(self, method):
        self.client.close()
        self.driver.quit()

    @pytest.mark.human
    def test_set_clear_url_rewrite_rule(self):
        targetURL = "https://www.saucelabs.com/versions.js"
        assert 200 == self.client.rewrite_url(
            "https://www.saucelabs.com/versions.+", "https://www.saucelabs.com/versions.json"
        )
        self.driver.get(targetURL)
        assert "Sauce Connect" in self.driver.page_source
        assert self.client.clear_all_rewrite_url_rules() == 200
        self.driver.get(targetURL)
        assert "Sauce Connect" not in self.driver.page_source

    @pytest.mark.human
    def test_response_interceptor(self):
        content = "Response successfully intercepted"
        targetURL = "https://saucelabs.com/versions.json?hello"
        self.client.response_interceptor(
            """if(messageInfo.getOriginalUrl().contains('?hello')){contents.setTextContents("%s");}""" % content
        )
        self.driver.get(targetURL)
        assert content in self.driver.page_source

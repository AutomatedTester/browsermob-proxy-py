from selenium import webdriver
import os
import sys

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestWebDriver(object):
    def setup_method(self, method):
        from browsermobproxy.client import Client
        self.client = Client("localhost:9090")

    def teardown_method(self, method):
        self.client.close()

    def test_i_want_my(self):
        driver = webdriver.Firefox(proxy=self.client)

        self.client.new_har("mtv")
        targetURL = "http://www.mtv.com"
        self.client.rewrite_url(".*american_flag-384x450\\.jpg", "http://www.foodsubs.com/Photos/englishmuffin.jpg")

        driver.get(targetURL)

        import time
        time.sleep(10)

        driver.quit()

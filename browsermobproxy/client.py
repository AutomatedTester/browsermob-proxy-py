#from httplib2 import Http
import requests
from urllib import urlencode
import json

class Client(object):
    
    def __init__(self, url):
        """
        Initialises a new Client object
        :Args:
         - url: This is where the BrowserMob Proxy lives
        """
        self.host = url 
        resp = requests.post('%s/proxy' % self.host, urlencode(''))
        jcontent = json.loads(resp.content)
        self.port = jcontent['port']
        url_parts = self.host.split(":")
        self.proxy = url_parts[0] + ":" + url_parts[1] + ":" +  str(self.port)

    def headers(self, headers):
        """
        This sets the headers that will set by the proxy on all requests
        :Args:
         - headers: this is a dictionary of the headers to be set
         """
        if not isinstance(headers, dict):
            raise TypeError("headers needs to be dictionary")

        requests.post('%s/proxy/%s/har' % (self.host, self.port),
                                json.dumps(headers))

    def new_har(self, ref=None):
        """
        This sets a new HAR to be recorded
        :Args:
         - ref: A reference for the HAR. Defaults to None
        """
        requests.put('%s/proxy/%s/har' % (self.host, self.port), 
                                    ref or '')

    def new_page(self, ref):
        """
        This sets a new page to be recorded
        :Args:
         - ref: A reference for the new page. Defaults to None
        """
        resp = requests.put('%s/proxy/%s/har/pageRef' % (self.host, self.port), 
                                    ref or '')
        if resp.content:
            return json.loads(resp.content)

    @property
    def har(self):
        """
        Gets the HAR that has been recorded
        """
        resp = requests.get('%s/proxy/%s/har' % (self.host, self.port))
                                    
        return json.loads(resp.content)

    def selenium_proxy(self):
        """
        Returns a Selenium WebDriver Proxy class with details of the HTTP Proxy
        """
        from selenium import webdriver
        return webdriver.Proxy({"httpProxy":self.proxy})

    def whitelist(self, regexp, status_code):
        """
        Sets a list of URL patterns to whitelist
        :Args:
         - regex: a comma separated list of regular expressions
         - status_code: the HTTP status code to return for URLs that do not match the whitelist 

        """
        resp = requests.put('%s/proxy/%s/whitelist' % (self.host, self.port), 
                                    urlencode({ 'regex': regexp, 'status': status_code
                                    }))


    def blacklist(self, regexp, status_code):
        """
        Sets a list of URL patterns to blacklist 
        :Args:
         - regex: a comma separated list of regular expressions
         - status_code: the HTTP status code to return for URLs that do not match the blacklist 

        """
        resp = requests.put('%s/proxy/%s/blacklist' % (self.host, self.port), 
                                    urlencode({ 'regex': regexp, 'status': status_code
                                    }))

    LIMITS = {
        'upstream_kbps' : 'upstreamKbps',
        'downstream_kbps' : 'downstreamKbps',
        'latency' : 'latency'
      }
    

    def limits(self, options):
        """
        Limit the bandwidth through the proxy.
        :Args:
         - options: A dictionary with all the details you want to set.
                        downstreamKbps - Sets the downstream kbps
                        upstreamKbps - Sets the upstream kbps
                        latency - Add the given latency to each HTTP request
        """
        params = {}

        for (k, v) in options.items():
            if not self.LIMITS.has_key(k):
                raise Exception('invalid key: %s' % k)

            params[self.LIMITS[k]] = int(v)

        if len(params.items()) == 0:
            raise Exception("You need to specify one of the valid Keys")
        
        resp = requests.put('%s/proxy/%s/limit' % (self.host, self.port), 
                                    urlencode(params))

    def close(self):
        """
        shuts down the proxy and closes the port
        """
        resp = requests.delete('%s/proxy/%s' % (self.host, self.port))

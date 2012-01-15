from httplib2 import Http
from urllib import urlencode
import json

class Client(object):
    
    def __init__(self, url):
        self.host = url 
        h = Http()
        resp, content = h.request('%s/proxy' % self.host, 'POST', urlencode(''))
        jcontent = json.loads(content)
        self.port = jcontent['port']
        url_parts = self.host.split(":")
        self.proxy = url_parts[0] + ":" + url_parts[1] + ":" +  str(self.port)

    def new_har(self, ref=None):
        h = Http()
        resp, content = h.request('%s/proxy/%s/har' % (self.host, self.port), 
                                    'PUT', ref or '')

    def new_page(self, ref):
        h = Http()
        resp, content = h.request('%s/proxy/%s/har/pageRef' % (self.host, self.port), 
                                    'PUT', ref or '')
        if content:
            return json.loads(content)

    @property
    def har(self):
        h = Http()
        resp, content = h.request('%s/proxy/%s/har' % (self.host, self.port), 
                                    'GET')
        return json.loads(content)

    def selenium_proxy(self):
        from selenium import webdriver
        return webdriver.Proxy({"httpProxy":self.proxy})

    def whitelist(self, regexp, status_code):
        h = Http()
        resp, content = h.request('%s/proxy/%s/whitelist' % (self.host, self.port), 
                                    'PUT', urlencode({ 'regex': regexp, 'status': status_code
                                    }))


    def blacklist(self, regexp, status_code):
        h = Http()
        resp, content = h.request('%s/proxy/%s/blacklist' % (self.host, self.port), 
                                    'PUT', urlencode({ 'regex': regexp, 'status': status_code
                                    }))

    LIMITS = {
        'upstream_kbps' : 'upstreamKbps',
        'downstream_kbps' : 'downstreamKbps',
        'latency' : 'latency'
      }
    

    def limits(self, options):
        params = {}

        for (k, v) in options.items():
            if not self.LIMITS.has_key(k):
                raise Exception('invalid key: %s' % k)

            params[self.LIMITS[k]] = int(v)

        if len(params.items()) == 0:
            raise Exception("You need to specify one of the valid Keys")
        
        h = Http()
        resp, content = h.request('%s/proxy/%s/limit' % (self.host, self.port), 
                                    'PUT', urlencode(params))

    def close(self):
        h = Http()
        resp, content = h.request('%s/proxy/%s' % (self.host, self.port), 
                                    'DELETE' )

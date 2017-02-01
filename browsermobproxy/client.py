import requests

try:
    from urllib.parse import urlencode, unquote
except ImportError:
    from urllib import urlencode, unquote
import json


class Client(object):
    def __init__(self, url, params=None, options=None):
        """
        Initialises a new Client object


        :param url: This is where the BrowserMob Proxy lives
        :param params: URL query (for example httpProxy and httpsProxy vars)
        :param options: Dictionary that can contain the port of an existing
                        proxy to use (for example 'existing_proxy_port_to_use')
        """
        params = params if params is not None else {}
        options = options if options is not None else {}
        self.host = "http://" + url
        if params:
            urlparams = "?" + unquote(urlencode(params))
        else:
            urlparams = ""
        if 'existing_proxy_port_to_use' in options:
            self.port = options['existing_proxy_port_to_use']
        else:
            resp = requests.post('%s/proxy' % self.host + urlparams)
            content = resp.content.decode('utf-8')
            try:
                jcontent = json.loads(content)
            except Exception as e:
                raise Exception("Could not read Browsermob-Proxy json\n"
                                "Another server running on this port?\n%s..." % content[:512])
            self.port = jcontent['port']
        url_parts = self.host.split(":")
        self.proxy = url_parts[1][2:] + ":" + str(self.port)

    def close(self):
        """
        shuts down the proxy and closes the port
        """
        r = requests.delete('%s/proxy/%s' % (self.host, self.port))
        return r.status_code

    # webdriver integration
    # ...as a proxy object
    def selenium_proxy(self):
        """
        Returns a Selenium WebDriver Proxy class with details of the HTTP Proxy
        """
        from selenium import webdriver
        return webdriver.Proxy({
            "httpProxy": self.proxy,
            "sslProxy": self.proxy,
        })

    def webdriver_proxy(self):
        """
        Returns a Selenium WebDriver Proxy class with details of the HTTP Proxy
        """
        return self.selenium_proxy()

    # ...as a capability
    def add_to_capabilities(self, capabilities):
        """
        Adds an 'proxy' entry to a desired capabilities dictionary with the
        BrowserMob proxy information


        :param capabilities: The Desired capabilities object from Selenium WebDriver
        """
        capabilities['proxy'] = {
            'proxyType': "MANUAL",
            'httpProxy': self.proxy,
            'sslProxy': self.proxy
        }

    def add_to_webdriver_capabilities(self, capabilities):
        self.add_to_capabilities(capabilities)

    # browsermob proxy api
    @property
    def proxy_ports(self):
        """
        Return a list of proxy ports available
        """
        # r should look like {u'proxyList': [{u'port': 8081}]}
        r = requests.get('%s/proxy' % self.host).json()
        ports = [port['port'] for port in r['proxyList']]

        return ports

    @property
    def har(self):
        """
        Gets the HAR that has been recorded
        """
        r = requests.get('%s/proxy/%s/har' % (self.host, self.port))

        return r.json()

    def new_har(self, ref=None, options=None, title=None):
        """
        This sets a new HAR to be recorded

        :param str ref: A reference for the HAR. Defaults to None
        :param dict options: A dictionary that will be passed to BrowserMob
            Proxy with specific keywords. Keywords are:

                - captureHeaders: Boolean, capture headers
                - captureContent: Boolean, capture content bodies
                - captureBinaryContent: Boolean, capture binary content

        :param str title: the title of first har page. Defaults to ref.
        """
        options = options if options is not None else {}
        payload = {"initialPageRef": ref} if ref is not None else {}
        if title is not None:
            payload.update({'initialPageTitle': title})

        if options:
            payload.update(options)

        r = requests.put('%s/proxy/%s/har' % (self.host, self.port), payload)
        if r.status_code == 200:
            return (r.status_code, r.json())
        else:
            return (r.status_code, None)

    def new_page(self, ref=None, title=None):
        """
        This sets a new page to be recorded

        :param str ref: A reference for the new page. Defaults to None
        :param str title: the title of new har page. Defaults to ref.
        """
        payload = {"pageRef": ref} if ref is not None else {}
        if title is not None:
            payload.update({'pageTitle': title})
        r = requests.put('%s/proxy/%s/har/pageRef' % (self.host, self.port),
                         payload)
        return r.status_code

    def blacklist(self, regexp, status_code):
        """
        Sets a list of URL patterns to blacklist

        :param str regex: a comma separated list of regular expressions
        :param int status_code: the HTTP status code to return for URLs
            that do not match the blacklist
        """
        r = requests.put('%s/proxy/%s/blacklist' % (self.host, self.port),
                         {'regex': regexp, 'status': status_code})
        return r.status_code

    def whitelist(self, regexp, status_code):
        """
        Sets a list of URL patterns to whitelist

        :param str regex: a comma separated list of regular expressions
        :param int status_code: the HTTP status code to return for URLs
            that do not match the whitelist
        """
        r = requests.put('%s/proxy/%s/whitelist' % (self.host, self.port),
                         {'regex': regexp, 'status': status_code})
        return r.status_code

    def basic_authentication(self, domain, username, password):
        """
        This add automatic basic authentication

        :param str domain: domain to set authentication credentials for
        :param str username: valid username to use when authenticating
        :param  str password: valid password to use when authenticating
        """
        r = requests.post(url='%s/proxy/%s/auth/basic/%s' % (self.host, self.port, domain),
                          data=json.dumps({'username': username, 'password': password}),
                          headers={'content-type': 'application/json'})
        return r.status_code

    def headers(self, headers):
        """
        This sets the headers that will set by the proxy on all requests

        :param dict headers: this is a dictionary of the headers to be set
        """
        if not isinstance(headers, dict):
            raise TypeError("headers needs to be dictionary")

        r = requests.post(url='%s/proxy/%s/headers' % (self.host, self.port),
                          data=json.dumps(headers),
                          headers={'content-type': 'application/json'})
        return r.status_code

    def response_interceptor(self, js):
        """
        Executes the java/js code against each response
        `HttpRequest request <https://netty.io/4.1/api/io/netty/handler/codec/http/HttpRequest.html>`_,
        `HttpMessageContents contents <https://raw.githubusercontent.com/lightbody/browsermob-proxy/master/browsermob-core/src/main/java/net/lightbody/bmp/util/HttpMessageContents.java>`_,
        `HttpMessageInfo messageInfo <https://raw.githubusercontent.com/lightbody/browsermob-proxy/master/browsermob-core/src/main/java/net/lightbody/bmp/util/HttpMessageInfo.java>`_
        are available objects to interact with.
        :param str js: the js/java code to execute
        """
        r = requests.post(url='%s/proxy/%s/filter/response' % (self.host, self.port),
                          data=js,
                          headers={'content-type': 'text/plain'})
        return r.status_code

    def request_interceptor(self, js):
        """
        Executes the java/js code against each response
        `HttpRequest request <https://netty.io/4.1/api/io/netty/handler/codec/http/HttpRequest.html>`_,
        `HttpMessageContents contents <https://raw.githubusercontent.com/lightbody/browsermob-proxy/master/browsermob-core/src/main/java/net/lightbody/bmp/util/HttpMessageContents.java>`_,
        `HttpMessageInfo messageInfo <https://raw.githubusercontent.com/lightbody/browsermob-proxy/master/browsermob-core/src/main/java/net/lightbody/bmp/util/HttpMessageInfo.java>`_
        are available objects to interact with.
        :param str js: the js/java code to execute
        """
        r = requests.post(url='%s/proxy/%s/filter/request' % (self.host, self.port),
                          data=js,
                          headers={'content-type': 'text/plain'})
        return r.status_code

    LIMITS = {
        'upstream_kbps': 'upstreamKbps',
        'downstream_kbps': 'downstreamKbps',
        'latency': 'latency'
    }

    def limits(self, options):
        """
        Limit the bandwidth through the proxy.

        :param dict options: A dictionary with all the details you want to set.
            downstream_kbps - Sets the downstream kbps
            upstream_kbps - Sets the upstream kbps
            latency - Add the given latency to each HTTP request
        """
        params = {}

        for (k, v) in list(options.items()):
            if k not in self.LIMITS:
                raise KeyError('invalid key: %s' % k)

            params[self.LIMITS[k]] = int(v)

        if len(list(params.items())) == 0:
            raise KeyError("You need to specify one of the valid Keys")

        r = requests.put('%s/proxy/%s/limit' % (self.host, self.port),
                         params)
        return r.status_code

    TIMEOUTS = {
        'request': 'requestTimeout',
        'read': 'readTimeout',
        'connection': 'connectionTimeout',
        'dns': 'dnsCacheTimeout'
    }

    def timeouts(self, options):
        """
        Configure various timeouts in the proxy

        :param dict options: A dictionary with all the details you want to set.
            request - request timeout (in seconds)
            read - read timeout (in seconds)
            connection - connection timeout (in seconds)
            dns - dns lookup timeout (in seconds)
        """
        params = {}

        for (k, v) in list(options.items()):
            if k not in self.TIMEOUTS:
                raise KeyError('invalid key: %s' % k)

            params[self.TIMEOUTS[k]] = int(v)

        if len(list(params.items())) == 0:
            raise KeyError("You need to specify one of the valid Keys")

        r = requests.put('%s/proxy/%s/timeout' % (self.host, self.port),
                         params)
        return r.status_code

    def remap_hosts(self, address=None, ip_address=None, hostmap=None):
        """
        Remap the hosts for a specific URL

        :param str address: url that you wish to remap
        :param str ip_address: IP Address that will handle all traffic for
            the address passed in
        :param **hostmap: Other hosts to be added as keyword arguments
        """
        hostmap = hostmap if hostmap is not None else {}
        if (address is not None and ip_address is not None):
            hostmap[address] = ip_address

        r = requests.post('%s/proxy/%s/hosts' % (self.host, self.port),
                          json.dumps(hostmap),
                          headers={'content-type': 'application/json'})
        return r.status_code

    def wait_for_traffic_to_stop(self, quiet_period, timeout):
        """
        Waits for the network to be quiet

        :param int quiet_period: number of milliseconds the network needs
            to be quiet for
        :param int timeout: max number of milliseconds to wait
        """
        r = requests.put('%s/proxy/%s/wait' % (self.host, self.port),
                         {'quietPeriodInMs': quiet_period, 'timeoutInMs': timeout})
        return r.status_code

    def clear_dns_cache(self):
        """
        Clears the DNS cache associated with the proxy instance
        """
        r = requests.delete('%s/proxy/%s/dns/cache' % (self.host, self.port))
        return r.status_code

    def rewrite_url(self, match, replace):
        """
        Rewrites the requested url.

        :param match: a regex to match requests with
        :param replace: unicode \
                   a string to replace the matches with
        """
        params = {
            "matchRegex": match,
            "replace": replace
        }
        r = requests.put('%s/proxy/%s/rewrite' % (self.host, self.port),
                         params)
        return r.status_code

    def clear_all_rewrite_url_rules(self):
        """
        Clears all URL rewrite rules
        :return: status code
        """

        r = requests.delete('%s/proxy/%s/rewrite' % (self.host, self.port))
        return r.status_code

    def retry(self, retry_count):
        """
        Retries. No idea what its used for, but its in the API...

        :param int retry_count: the number of retries
        """
        r = requests.put('%s/proxy/%s/retry' % (self.host, self.port),
                         {'retrycount': retry_count})
        return r.status_code

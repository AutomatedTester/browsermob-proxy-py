
0.8.0 / 2017-02-07
==================

  * Adds rewrite rules clear api. Fixes content type for request/response intercept and adds doc links for writing intercept code. Adds comments clarifying intercept client test coverage. Augments human test for url rewrite and adds clear portion. Adds test for response intercept. Adds bootstrap script to download tools to test with. Refactors human tests so browser session are cleaned up when tests fail and tests run with chromium. Adds server start script for travis. Changes .travis.yml to use provided scripts and also run headless chrome.
  * If the JSON doesn't load, it's likely because the user has another server running on the same port. Improve the error message here so can figure out what's going on more easily.
  * Inherit from Exception as StandardError was removed in Python 3
  * Add ProxyServerError and raise it instead of Exception
  * Fix docstring for limits()
  * Fix path join issue: log_path_name would be /server.log
  * Make default option values more robust
  * Add retry sleep and count in options
  * Reenabling timeout tests as they have been fixed in B6 of the server
  * Removing duplicate method. Fixes #41
  * docstrings cleanup
  * configurable log file
  * added title options for new har and new har page
  * replaced mutable default values with None
  * Update Requests dependency version
  * Updating supported Python versions
  * Disabling a test due to BMP Server bug
  * Bumping version number of BMP server used in testing
  * Add bmp.log to .gitignore
  * Add details on how to contribute
  * Updating response URL endpoints to use filter
  * Ignoring .cache directory
  * Change remap_hosts to accept dictionary
  * Make sure the process is still running while waiting for the server to start.
  * Changed hostmap to be a named argument for compatibility
  * Merge remote-tracking branch 'upstream/master' into patch-1
  * Add the ability to empty the DNS cache
  * Correct function name
  * Add the ability to return all active proxy ports from Browsermob
  * switch to Travis container setup
  * Update to latest browsermob proxy release for testing
  * Correct exception typo
  * Update remap_hosts test
  * Fix whitespace
  * Let remap_hosts accept a dictionary
  * Upgrading Travis to it's container system
  * bumping to 0.7.1

0.7.1 / 2015-07-09
==================

  * Adding option of using existing proxy port.
  * Allow use of a remote proxy server.
  * improved directions on running tests
  * fix broken test (test_new_page_defaults)

0.7.0 / 2015-06-05 
==================

 * Updating travis ci to use browsermob proxy 2.0
 * Support to use httpsProxy and httpProxy at proxy creation time
 * Adding Python 3 support
 * add sslProxy to Client.add_to_capabilities with tests
 * Correct docstring for `wait_for_traffic_to_stop`
 * Removing unused :Args: items
 * Updating docstrings
 * Correcting args and params for documentation
 * updated docstrings for easier formatting on things like RTDs
 * updated new_har() docstrings
 * updated client documentation
 * Added client and server docs
 * updating version in docs

0.6.0 / 2014-01-21 
==================

  * Added support for parameters in har creation
  * Bug fixes for tests that are out of date
  * Setup server constructor to look on path for location of browsermob-proxy executable. As well as looking for a file. Also added example code for using browsermob-proxy with chrome
  * Fix project name
  * adding docs

0.5.0 / 2013-05-23 
==================
* Allow proxying of ssl requests with selenium.
* Updating case for proxy type


0.4.0 / 2013-03-06 
==================

  * Allow setting basic authentication
  * Adding the ability to remap hosts which is available from BrowserMob Proxy Beta 7
  * Merge pull request #6 from lukeis/patch-2
  * Update readme.md
  * initial commit of event listener to auto do record
  * server.create_proxy is a function, should be called :)
  * forgot to add the port

0.2.0 / 2012-06-18 
==================

  * pep8 --ignore=E501
  * DELETE /proxy/:port/
  * /proxy/:port/limits
  * /proxy/:port/blacklist
  * /proxy/:port/whitelist
  * fixing /proxy/:port/har/pageRef
  * fixing /proxy/:port/har/pageRef
  * fixing passing in a page ref as the name for the page in /proxy/:port/har
  * tests around /proxy/:port/har and some cleanup of the implementation
  * make /proxy/:port/headers work
  * wrapping selenium_proxy with webdriver_proxy since the project is more than just webdriver
  * extending the client to play nice with remote webdriver instances
  * create_proxy sounds and feels like a method to me, let's make it so
  * ensure the self.process exist, to reduce possibilities of AttributeError
  * check the path before attempting to start the server
  * wait longer than 3 seconds for the server to come up

0.1.0 / 2012-03-22 
==================

* Removed httplib2 in preference for requests
* Added support for setting headers

0.0.1 / 2012-01-16
==================

* Initial version

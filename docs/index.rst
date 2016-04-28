.. BrowserMob Proxy documentation master file, created by
   sphinx-quickstart on Fri May 24 12:37:12 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. highlightlang:: python


============================================
Welcome to BrowserMob Proxy's documentation!
============================================

Python client for the BrowserMob Proxy 2.0 REST API.

--------------
How to install
--------------

BrowserMob Proxy is available on PyPI_, so you can install it with ``pip``::

    $ pip install browsermob-proxy

Or with `easy_install`::

    $ easy_install browsermob-proxy

Or by cloning the repo from GitHub_::

    $ git clone git://github.com/AutomatedTester/browsermob-proxy-py.git

Then install it by running::

    $ python setup.py install

----------------------------------
How to use with selenium-webdriver
----------------------------------

Manually::

    from browsermobproxy import Server
    server = Server("path/to/browsermob-proxy")
    server.start()
    proxy = server.create_proxy()

    from selenium import webdriver
    profile  = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    driver = webdriver.Firefox(firefox_profile=profile)


    proxy.new_har("google")
    driver.get("http://www.google.co.uk")
    proxy.har # returns a HAR JSON blob

    server.stop()
    driver.quit()

For Legacy Implementation::

    from browsermobproxy import Server
    server = Server("path/to/browsermob-proxy",{'legacy_mode':True})
    server.start()
    proxy = server.create_proxy()

    from selenium import webdriver
    profile  = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    driver = webdriver.Firefox(firefox_profile=profile)


    proxy.new_har("google")
    driver.get("http://www.google.co.uk")
    proxy.har # returns a HAR JSON blob

    server.stop()
    driver.quit()

-----------------
How to Contribute
-----------------

Getting Started
---------------

* Fork the repository on GitHub - well... duh :P
* Create a virtualenv: `virtualenv venv`
* Activate the virtualenv: `. venv/bin/activate`
* Install the package in develop mode: `python setup.py develop`
* Install requirements: `pip install -r requirements.txt`
* Run the tests to check that everything was successful: `py.test tests

Making Changes
--------------

* Create a topic branch from where you want to base your work.
  * This is usually the master branch.
  * Only target release branches if you are certain your fix must be on that
    branch.
  * To quickly create a topic branch based on master; `git checkout -b
    /my_contribution master`. Please avoid working directly on the
    `master` branch.
* Make commits of logical units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure you have added the necessary tests for your changes.
* Run _all_ the tests to assure nothing else was accidentally broken.

Submitting Changes
------------------

* Push your changes to a topic branch in your fork of the repository.
* Submit a pull request to the main repository
* After feedback has been given we expect responses within two weeks. After two
  weeks will may close the pull request if it isn't showing any activity

Contents:

.. toctree::
   :maxdepth: 2

   client.rst
   server.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _GitHub: https://github.com/AutomatedTester/browsermob-proxy-py
.. _PyPI: http://pypi.python.org/pypi/browsermob-proxy

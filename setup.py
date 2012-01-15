from setuptools import setup, find_packages

setup(name='browsermob-proxy',
      version='0.0.1',
      description='A simple Assertion Framework',
      author='David Burns',
      author_email='david.burns at theautomatedtester dot co dot uk',
      url='http://oss.theautomatedtester.co.uk/browsermob-proxy-py',
      classifiers=['Development Status :: 3 - Alpha',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
                  'Operating System :: POSIX',
                  'Operating System :: Microsoft :: Windows',
                  'Operating System :: MacOS :: MacOS X',
                  'Topic :: Software Development :: Testing',
                  'Topic :: Software Development :: Libraries',
                  'Programming Language :: Python'],
        packages = find_packages() )

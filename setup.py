##############################################################################
#
# Copyright (c) 2012 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt. A copy of the license should accompany
# this distribution. THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

import os
from sys import version

from setuptools import setup, find_packages

VERSION = '0.1'

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

requires = [
    'pyramid',
    'amonpy'
    ]

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface',
    ]

testing_extras = [
    'nose',
    'coverage',
    'mock',
    ]

if version < '2.7':
    testing_extras.append('unittest2')

setup(name='pyramid_amon',
      version=VERSION,
      description=('Pyramid add-on for Amon application and system '
                   'monitoring toolkit.'),
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "License :: Repoze Public License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        ],
      keywords='wsgi pylons web pyramid',
      author="Blaise Laflamme",
      author_email="pylons-discuss@googlegroups.com",
      url="http://pylonsproject.org",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require={
          'testing': testing_extras,
          'docs': docs_extras,
          },
      tests_require=requires,
      test_suite='pyramid_amon',
      entry_points=''
      )

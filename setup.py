#!/usr/bin/env python
# This file is part of the product_pack module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from setuptools import setup
import re
import os
from configparser import ConfigParser

MODULE = 'product_pack'
PREFIX = 'trytonzz'
MODULE2PREFIX = {
}


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

config = ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = []
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        prefix = MODULE2PREFIX.get(dep, 'trytond')
        requires.append('%s_%s >= %s.%s, < %s.%s' %
                (prefix, dep, major_version, minor_version,
                major_version, minor_version + 1))
requires.append('trytond >= %s.%s, < %s.%s' %
        (major_version, minor_version, major_version, minor_version + 1))

tests_require = ['proteus >= %s.%s, < %s.%s' %
    (major_version, minor_version, major_version, minor_version + 1)]

setup(name='%s_%s' % (PREFIX, MODULE),
    version=info.get('version', '0.0.1'),
    description='Tryton module description',
    author='Zikzakmedia SL',
    author_email='zikzak@zikzakmedia.com',
    url='http://www.zikzakmedia.com',
    download_url='https://bitbucket.org/zikzakmedia/trytond-%s' % MODULE,
    package_dir={'trytond.modules.%s' % MODULE: '.'},
    packages=[
        'trytond.modules.%s' % MODULE,
        'trytond.modules.%s.tests' % MODULE,
        ],
    package_data={
        'trytond.modules.%s' % MODULE: (info.get('xml', [])
            + ['tryton.cfg', 'view/*.xml', 'locale/*.po', ]),
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Catalan',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        ],
    license='GPL-3',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    %s = trytond.modules.%s
    """ % (MODULE, MODULE),
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
)

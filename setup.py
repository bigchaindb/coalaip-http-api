#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

install_requires = [
    'coalaip>=0.0.1.dev2',
    'coalaip-bigchaindb>=0.0.1.dev2',
    'flask>=0.11.1',
    'flask-restful>=0.3.5',
    'gunicorn>=19.6.0'
]

tests_require = [
    'tox>=2.3.1',
    'flake8>=2.6.0',
    'pytest>=3.0.1',
    'pytest-mock',
    'pytest_flask',
]

dev_require = [
    'ipdb',
    'ipython',
]

docs_require = [
    'Sphinx>=1.4.4',
    'sphinx-autobuild',
    'sphinxcontrib-napoleon>=0.4.4',
    'sphinx_rtd_theme',
]

setup(
    name='coalaip-http-api',
    version='0.0.1.dev1',
    description="An HTTP wrapper for CoalaIP",
    author="BigchainDB",
    author_email='dev@bigchaindb.com',
    url='https://github.com/bigchaindb/coalaip-http-api',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'dev': dev_require + tests_require + docs_require,
        'docs': docs_require,
    },
    test_suite='tests',
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords=['coalaip', 'coalaip http api', 'bigchaindb'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

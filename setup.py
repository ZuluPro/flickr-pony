#!/usr/bin/env python
from setuptools import setup, find_packages
import flickr_pony


def get_file(addr):
    with open(addr, 'r') as fi:
        return fi.read()


setup(
    name='flickr-pony',
    version=flickr_pony.__version__,
    description=flickr_pony.__doc__,
    author=flickr_pony.__author__,
    author_email=flickr_pony.__email__,
    install_requires=get_file('./requirements.txt').splitlines(),
    tests_require=get_file('./requirements-tests.txt').splitlines(),
    long_description=get_file('README.rst'),
    license='BSD',
    url=flickr_pony.__url__,
    keywords=['django', 'flickr', 'storage', 'cloud'],
    packages=find_packages(exclude=['demo_project']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

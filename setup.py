import sys
from setuptools import setup

from attics import __version__

requires = ['jinja2', 'markdown', 'parsley']
if sys.version_info < (2,7):
    requires.append('argparse')
README = open('README.rst').read()

entry_points = {
    'console_scripts': [
        'attics = attics.tools:main',
    ]
}

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',

    # License goes here

    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='Attics',
    version=__version__,
    author='Colin Dunklau',
    author_email='colin.dunklau@gmail.com',
    long_description=README,
    packages=['attics', 'attics.tests'],
    include_package_data=True,
    entry_points=entry_points,
    install_requires=requires,
    classifiers=classifiers,
)

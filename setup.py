"""
Setup file
"""

# To use a consistent encoding
import codecs
import os

# Always prefer setuptools over distutils
from setuptools import setup, find_packages


def get_long_description():
    """
    Get the long description from the README file
    """
    here = os.path.abspath(os.path.dirname(__file__))

    with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as readme:
        return readme.read()


def find_package_data(package, data_dir):
    """
    Find all the package data
    """
    package_data = []
    oldcwd = os.getcwd()
    os.chdir(package)
    for dirpath, _, filenames in os.walk(data_dir):
        files = [os.path.join(dirpath, filename) for filename in filenames]
        package_data.extend(files)
    os.chdir(oldcwd)
    return package_data


setup(
    name='cli',
    version='0.0.1',
    description='packaging wrapper using ansible',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/theforeman/foreman-quadlet',
    author='The Foreman Project',
    author_email='foreman-dev@googlegroups.com',
    zip_safe=False,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],

    keywords='foreman',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['obsah >= 1.0.0'],

    extras_require={
        'argcomplete': ['argcomplete'],
    },

    package_data={
        'cli': find_package_data('cli'),
    },

    entry_points={
        'console_scripts': [
            'cli=cli:main',
        ],
    },
)

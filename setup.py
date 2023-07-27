# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py.
"""

from setuptools import setup

setup()
# from __future__ import absolute_import, print_function

# import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup
#
#
# def read(*names, **kwargs):
#     """Read description files."""
#     path = join(dirname(__file__), *names)
#     with open(path, encoding=kwargs.get('encoding', 'utf8')) as fh:
#         return fh.read()
#
# long_description = read('README.md')
#
# setup(
#     name='api_takehome',
#     version='0.11.3',
#     description='An API endpoint take-home exam.',
#     long_description=long_description,
#     long_description_content_type='text/x-rst',
#     license='MIT License',
#     author='Matthew Boyd',
#     author_email='machallboyd@gmail.com',
#     url='https://github.com/machallboyd/api_takehome',
#     packages=find_packages('src'),
#     package_dir={'': 'src'},
#     py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
#     include_package_data=True,
#     zip_safe=False,
#     classifiers=[
#         # complete classifier list:
#         # http://pypi.python.org/pypi?%3Aaction=list_classifiers
#         'Development Status :: 4 - Beta',
#         # 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
#         'License :: OSI Approved :: MIT License',
#         'Intended Audience :: Science/Research',
#         'Natural Language :: English',
#         'Operating System :: POSIX',
#         'Operating System :: MacOS',
#         'Operating System :: Microsoft',
#         'Programming Language :: Python :: 3.7',
#         'Programming Language :: Python :: 3.8',
#         'Programming Language :: Python :: 3.9',
#         'Programming Language :: Python :: 3.10',
#         'Topic :: Scientific/Engineering :: Bio-Informatics',
#         ],
#     project_urls={
#         'webpage': 'https://github.com/machallboyd/api_takehome',
#         # 'Documentation': 'https://api_takehome.readthedocs.io/en/latest/',
#         'Changelog': 'https://github.com/machallboyd/api_takehome/blob/main/CHANGELOG.rst',
#         'Issue Tracker': 'https://github.com/machallboyd/api_takehome/issues',
#         'Discussion Forum': 'https://github.com/machallboyd/api_takehome/discussions',
#         },
#     keywords=[
#         'ci', 'continuous-integration', 'project-template',
#         'project-skeleton', 'sample-project',
#         # eg: 'keyword1', 'keyword2', 'keyword3',
#         ],
#     python_requires='>=3.7, <4',
#     install_requires=[
#         # https://stackoverflow.com/questions/14399534
#         'fastapi',
#         ],
# extras_require={
#         "tests": ['pytest'],
#         # "dev": [],
#     },
#     setup_requires=[
#         #   'pytest-runner',
#         #   'setuptools_scm>=3.3.1',
#         ],
#     entry_points={
#         'console_scripts': [
#             'samplecli1= sampleproject.cli_int1:main',
#             ]
#         #
#         },
#
#     )
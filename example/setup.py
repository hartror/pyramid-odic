# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='example',
    version='0.0.0',
    description='',
    author='Rory Hart',
    author_email='hartror@gmail.com',
    url='https://github.com/hartror/pyramid-odic',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        "oic",
        "pyramid",
        "pyramid-debugtoolbar",
        "pyramid-oidc",
        "waitress"],
    entry_points="""\
      [paste.app_factory]
      main = example:main
      """
)

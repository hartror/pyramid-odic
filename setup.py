# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyramid_oidc',
    version='0.0.0',
    description='',
    long_description=readme,
    author='Rory Hart',
    author_email='hartror@gmail.com',
    url='https://github.com/hartror/pyramid-odic',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        "oic",
        "pyramid"]
)

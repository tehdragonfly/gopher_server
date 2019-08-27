import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

CHANGES = ""

setup(
    name="gopher_server",
    version="0.0",
    description="gopher_server",
    long_description=README,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "zope.interface",
    ],
)

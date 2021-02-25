"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='pushpad',
    version='0.9.0',
    description='Pushpad: real push notifications for websites',
    url='https://pushpad.xyz',
    author='Pushpad',
    author_email='support@pushpad.xyz',
    license='MIT',

    classifiers=[
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries",
        'License :: OSI Approved :: MIT License',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    keywords='pushpad web push notifications api',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests'],
    tests_require=['mock', 'nose'],
    test_suite='nose.collector',
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)

# coding=utf-8
from setuptools import setup

setup(
    name='nmp-web',

    version='4.0.0',

    description='A website on cloud for NWPC monitor platform.',
    long_description=__doc__,

    packages=['nmp_web'],

    include_package_data=True,

    zip_safe=False,

    install_requires=[
        'click',
        'Flask',
        'Flask-SQLAlchemy',
        'mysql-connector-python',
        'pymongo',
        'PyYAML',
        'redis',
        'requests',
        'SQLAlchemy',
        'backports-datetime-fromisoformat;python_version<"3.7"',
        'leancloud'
    ]
)
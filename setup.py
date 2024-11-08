"""
Bucket Dependency Manager by Astridot as part of Makoschin Free Software Distributions

This program is free software: you can redistribute it and/or modify
it under the terms of the Makoschin Free Software License (MFSL),
either version 1.0 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Makoschin Free Software License for more details.
"""

from setuptools import setup, find_packages

def read_long_description():
    with open('info.html', encoding='utf-8') as f:
        return f.read()

VERSION: str = "2.2.12"

setup(
    name='bkt',
    version=VERSION,
    author='astridot',
    author_email='pixilreal@gmail.com',
    description='Dependency manager for any language, for free, no subscriptions.',
    long_description=read_long_description(),
    long_description_content_type='text/plain',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bucket=bucket.cli:main'
        ]
    },
)

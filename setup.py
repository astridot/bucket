import os

from setuptools import setup, find_packages

def read_long_description():
    print(os.listdir())
    with open('info.html', encoding='utf-8') as f:
        return f.read()

VERSION: str = "v1"

setup(
    name='bkt',
    version=VERSION,
    author='astridot',
    author_email='pixilreal@gmail.com',
    description='Dependency manager for any language, for free, no subscriptions.',
    long_description=read_long_description(),
    long_description_content_type='text/html',
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
            'bucket=bucket.core:main'
        ]
    },
)
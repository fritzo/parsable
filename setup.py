from setuptools import setup, find_packages

VERSION = '0.1.0'

with open('README') as f:
    long_description = f.read()

config = {
    'name': 'parsable',
    'version': VERSION,
    'description': 'Lightweight command-line parsing via a decorator',
    'long_description': long_description,
    'author': 'Fritz Obermeyer',
    'author_email': 'fritz.obermeyer@gmail.com',
    'url': 'https://github.com/fritzo/parsable.py',
    'packages': find_packages(),
    'py_modules': ['parsable'],
    }

setup(**config)

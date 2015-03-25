from setuptools import setup, find_packages

__version__ = '0.1.2'

try:
    with open('README.rst') as f:
        long_description = f.read()
except IOError:
    long_description = 'Lightweight argument parsing using a decorator'

config = {
    'name': 'parsable',
    'version': __version__,
    'description': 'Lightweight argument parsing using a decorator',
    'long_description': long_description,
    'author': 'Fritz Obermeyer',
    'author_email': 'fritz.obermeyer@gmail.com',
    'url': 'https://github.com/fritzo/parsable',
    'packages': find_packages(),
    'py_modules': ['parsable'],
}

setup(**config)

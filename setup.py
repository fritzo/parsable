from setuptools import setup

__version__ = '0.3.1'

try:
    with open('README.rst') as f:
        long_description = f.read()
except IOError:
    long_description = 'Lightweight argument parsing using a decorator'

setup(
    name='parsable',
    version=__version__,
    description='Lightweight argument parsing using a decorator',
    long_description=long_description,
    author='Fritz Obermeyer',
    author_email='fritz.obermeyer@gmail.com',
    url='https://github.com/fritzo/parsable',
    py_modules=['parsable'],
)

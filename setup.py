from setuptools import setup

__version__ = '0.3.5'

try:
    with open('README.rst') as f:
        long_description = f.read()
except OSError:
    long_description = 'Lightweight argument parsing using a decorator'


setup(
    name='parsable',
    version=__version__,
    description='Lightweight argument parsing using a decorator',
    long_description=long_description,
    author='Fritz Obermeyer',
    author_email='fritz.obermeyer@gmail.com',
    url='https://github.com/fritzo/parsable',
    packages=['parsable'],
    package_data={'parsable': ['py.typed']},
    python_requires='>=3.10',
)

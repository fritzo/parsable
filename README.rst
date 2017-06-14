Parsable
========

.. image:: https://travis-ci.org/fritzo/parsable.png?branch=master
   :target: https://travis-ci.org/fritzo/parsable
   :alt: Build status

.. image:: https://badge.fury.io/py/parsable.png
   :target: https://pypi.python.org/pypi/parsable
   :alt: PyPI Version

Parsable is a lightweight decorator-based command line parser library.
Parsable was written to be simpler than argparse, optparse, and argh.

Installation
------------

Install from `PyPI`_ with ``pip``

.. _PyPI: http://pypi.python.org/pypi/parsable

.. code-block:: bash

    pip install parsable


Or just download `parsable.py`_ and add to your project.

.. _`parsable.py`: https://raw.github.com/fritzo/parsable/master/parsable.py

Usage
-----

Parsable uses just two pieces of syntax: a ``@parsable`` command decorator,
and a ``parsable()`` dispatch function.

1.  Import parsable.

    .. code-block:: python

        from parsable import parsable

2.  Decorate functions you want parsed.
    Parsable inspects the function to decide how to parse arguments.
    Arguments without default values are parsed as strings.
    Default arguments of any type ``T`` can be parsed as long
    as ``T(some_string)`` can do the parsing.

    .. code-block:: python  

        @parsable
        def my_function(required_arg, optional_bool=True, optional_int=1):
            '''Help messages are not just a good idea, they are required'''
            # parsable automatically converts types based on default arguments:
            assert isinstance(required_arg, str)
            assert isinstance(optional_string, bool)
            assert isinstance(optional_int, int)
            # ...

        @parsable
        def do_stuff_with_files(*filenames, inplace=True):
            '''This does something to each file'''
            # ...

3.  Dispatch at the end of the script.

    .. code-block:: python  

        if __name__ == '__main__':
            parsable()

4.  Use your new script

    .. code-block:: bash

        $ python my_script.py my_function demo optional_int=5
        ...

        # parsable replaces - with _ to make functions easier to read
        $ python my_script.py do-stuff-with-files *.py inplace=false
        ...

Advanced Usage
--------------

To show verbose information (commmand name and timing info),
set the environment variable ``PARSABLE_VERBOSE=true``.

If you use parsable for many modules in a package, you can collect them in your
``setup.py`` using ``parsable.find_entry_points()``.

.. code-block:: python

    from parsable import parsable
    from setuptools import setup
    
    setup(
        name='my_package',
        entry_points=parsable.find_entry_points('my_package'),
        ...
    )

LICENSE
-------

Parsable is dual-licensed under the MIT and GPL2 licenses.

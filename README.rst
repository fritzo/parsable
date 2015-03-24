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

Install with pip
~~~~~~~~~~~~~~~~

Parsable is already listed on `PyPI`_, you can install with ``pip`` if you have
the tool.

.. _PyPI: http://pypi.python.org/pypi/parsable

.. code-block:: bash

    pip install --upgrade parsable

Install with setup.py
~~~~~~~~~~~~~~~~~~~~~

You can also run the setup.py from the source if you don't have ``pip``.

.. code-block:: bash

    git clone https://github.com/fritzo/parsable.git
    cd parsable
    ./setup.py install

Download directly
~~~~~~~~~~~~~~~~~

Just save `parsable.py`_ and add to your project.

.. _`parsable.py`: https://raw.github.com/fritzo/parsable/master/parsable.py

Usage
-----

Parsable uses just tiny pieces of syntax: a ``@parsable.command`` decorator,
and a ``parsable.dispatch`` function.

1.  Import parsable

    .. code-block:: python

        import parsable

2.  Decorate functions you want parsed

    .. code-block:: python  

        @parsable.command
        def my_function(required_arg, optional_bool=True, optional_int=1):
            '''Help messages are not just a good idea, they are required'''
            # parsable automatically converts types based on default arguments:
            assert isinstance(required_arg, str)
            assert isinstance(optional_string, bool)
            assert isinstance(optional_int, int)
            # ...

        @parsable.command
        def do_stuff_with_files(*filenames, inplace=True):
            '''This does something to each file'''
            # ...

3.  Dispatch at the end of the script

    .. code-block:: python  

        if __name__ == '__main__':
            parsable.dispatch()

4.  Use your new script

    .. code-block:: bash

        $ python my_script.py my_function demo optional_int=5
        ...

        # parsable replaces - with _ to make functions easier to read
        $ python my_script.py do-stuff-with-files *.py in-place=false
        ...

That's it: only three little pieces of syntax!

LICENSE
-------

Parsable is dual-licensed under the MIT and GPL2 licenses.

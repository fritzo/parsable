#!/usr/bin/env python

from parsable import parsable
import sys

# This optional line creates a local parser
# that won't leak into modules that import this module.
parsable = parsable.Parsable()


@parsable
def example_command(required_arg, optional_int=1, optional_string='asdf'):
    'An example command that prints its arguments'
    assert isinstance(required_arg, str)
    assert isinstance(optional_int, int)
    assert isinstance(optional_string, str)
    print(required_arg, optional_int, optional_string)


@parsable
def another_command():
    'No arguments on this one'


@parsable
def print_all_strings(*args):
    'Example of variable number of arguments'
    print('len(args) = %i' % len(args))
    print('args:')
    for arg in args:
        assert isinstance(arg, str)
        print('  {0}'.format(arg))


global_value = True


@parsable
def __set_value_to_false():
    'Example of command-as-option'
    global global_value
    global_value = False


@parsable
def twice(*args):
    'Run a command twice'
    argv = [sys.argv[0]] + list(args)

    print('first time:')
    parsable(argv)

    print('second time:')
    parsable(argv)


if __name__ == '__main__':
    parsable()

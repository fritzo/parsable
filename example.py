#!/usr/bin/env python

import parsable

# This optional line creates a local parser
# that won't leak into modules that import this module.
parsable = parsable.Parsable()


@parsable.command
def example_command(required_arg, optional_int=1, optional_string='asdf'):
    'An example command that prints its arguments'
    assert isinstance(required_arg, str)
    assert isinstance(optional_int, int)
    assert isinstance(optional_string, str)
    print(required_arg, optional_int, optional_string)


@parsable.command
def another_command():
    'No arguments on this one'


@parsable.command
def print_all_strings(*args):
    'Example of variable number of arguments'
    print('len(args) = %i' % len(args))
    print('args:')
    for arg in args:
        assert isinstance(arg, str)
        print('  {0}'.format(arg))


global_value = True


@parsable.command
def __set_value_to_false():
    'Example of command-as-option'
    global global_value
    global_value = False


@parsable.command
def twice(*args):
    'Run a command twice'

    print('first time:')
    parsable.dispatch(args)

    print('second time:')
    parsable.dispatch(args)


if __name__ == '__main__':
    parsable.dispatch()

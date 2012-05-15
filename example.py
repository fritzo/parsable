#!/usr/bin/python

import parsable


@parsable.command
def example_command(required_arg, optional_int=1, optional_string='asdf'):
    'an example command that prints its arguments'
    print required_arg
    print optional_int
    print optional_string


@parsable.command
def another_command():
    'no arguments on this one'


@parsable.command
def print_all_strings(*args):
    'example of variable number of arguments'
    print 'len(args) = %i' % len(args)
    print 'args:'
    for arg in args:
        print '  %s' % arg


global_value = True


@parsable.command
def __set_value_to_false():
    'example of command-as-option'
    global global_value
    global_value = False


@parsable.command
def twice(*args):
    'run a command twice'

    print 'first time:'
    parsable.dispatch(args)

    print 'second time:'
    parsable.dispatch(args)


if __name__ == '__main__':
    parsable.dispatch()

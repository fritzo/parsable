'''
parsable - Lightweight argument parsing using a decorator.
http://github.com/fritzo/parsable

Copyright (c) 2011-2015, Fritz Obermeyer
Dual licensed under the MIT or GPL Version 2 licenses.
http://www.opensource.org/licenses/MIT
http://www.opensource.org/licenses/GPL-2.0
'''

import inspect
import os
import re
import resource
import sys
import time

VERBOSE = bool(os.environ.get('PARSABLE_VERBOSE'))

_commands = []

_bool_names = {'0': False, 'false': False, '1': True, 'true': True}

_parsers = {
    bool: (lambda b: _bool_names[b.lower()]),
    None.__class__: str,
}


def _parser(d):
    class_ = d.__class__
    return _parsers.get(class_, class_)


def command(fun):
    '''Decorator for parsable _commands.

    Example:
    >>> from parsable import parsable
    >>> @parsable
    ... def cat(*filenames):
    ...     'Concatenate and print files'
    ...     for f in filenames:
    ...        print(open(f).read())
    '''

    args, vargs, kwargs, defaults = inspect.getargspec(fun)
    if defaults is None:
        defaults = ()
    arg_types = (
        [str] * (len(args) - len(defaults)) +
        list(map(_parser, defaults)))
    kwd_types = dict(zip(args, arg_types))

    name = fun.__name__.replace('_', '-')
    assert fun.__doc__, 'missing docstring for %s' % name

    def parser(*args, **kwargs):
        varg_types = arg_types + [str] * (len(args) - len(arg_types))
        typed_args = tuple(t(a) for a, t in zip(args, varg_types))
        typed_kwargs = dict([
            (k, kwd_types.get(k, str)(v))
            for k, v in kwargs.items()
        ])
        start = time.time()
        fun(*typed_args, **typed_kwargs)
        elapsed = time.time() - start
        space = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if VERBOSE:
            sys.stderr.write(
                '%s took %g sec, maxrss = %d\n' % (name, elapsed, space))

    _commands.append((name, (fun, parser)))

    return fun


def at_top(extra_depth=0):
    '''Returns whether calling location is top-level parsable command.

    Example:
    >>> from parsable import parsable
    >>> @parsable
    ... def subroutine(arg=0):
    ...     'a subroutine'
    ...     result = arg + arg
    ...     if parsable.at_top():
    ...         print(result)
    ...     else:
    ...         return result
    '''

    depth = len(inspect.stack())
    assert depth >= 5
    return depth == 5 + extra_depth


def dispatch(argv=None):
    '''Parses arguments to call a parsable command.
    Example:
    >>> from parsable import parsable
    >>> if __name__ == '__main__':
    ...     parsable.dispatch()
    '''

    if argv is None:
        argv = sys.argv
    args = argv[1:]
    if VERBOSE:
        sys.stderr.write('# python {0}\n'.format(' '.join(argv)))

    if not args:
        script = os.path.split(argv[0])[-1]
        print('Usage: {0} COMMAND [ARG ARG ... KEY=VAL KEY=VAL ...]'.format(
            script))
        for name, (fun, _) in _commands:
            print('\n{0} {1}\n    {2}'.format(
                name,
                inspect.formatargspec(*inspect.getargspec(fun)),
                fun.__doc__.strip(),
            ))
        sys.exit(1)

    cmd, args, kwargs = args[0], args[1:], {}
    try:
        parser = dict(_commands)[cmd.replace('_', '-')][1]
    except KeyError:
        raise ValueError("unknown command '{0}', try one of:\n  {1}".format(
            cmd, ', '.join(name for name, _ in _commands)))
    while args and '=' in args[-1]:
        key, val = args.pop().split('=', 1)
        kwargs[key] = val
    parser(*args, **kwargs)


def find_entry_points(package_name, package_dir=None, pattern=r'\bparsable\b'):
    '''Finds parsable entry points during package setup.

    Example in setup.py:
        from setuptools import setup, find_packages
        from parsable import find_entry_points
        setup(
            name='example_package',
            packages=find_packages(),
            entry_points=find_entry_points('example_package'))
    '''

    if package_dir is None:
        package_dir = package_name
    package_dir = os.path.normpath(os.path.abspath(package_dir))
    points = []
    for root, dirnames, filenames in os.walk(package_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                path = os.path.join(root, filename)
                path = os.path.relpath(path, os.path.dirname(package_dir))
                with open(path) as lines:
                    if any(re.search(pattern, l) for l in lines):
                        module = path[:-3].replace(os.sep, '.')
                        name = module.replace('.__main__', '')
                        points.append('{0} = {1}'.format(name, module))
    assert points, 'no entry points found at {0}'.format(package_dir)
    console_scripts = list(map('{0}:parsable.dispatch'.format, points))
    return {'console_scripts': console_scripts}


class Parsable:
    '''Collects parsable commands locally for optional dispatch.

    Example:
    >>> from parsable import parsable
    >>> parsable = parsable.Parsable()
    '''

    def __init__(self):
        self._commands = []

    def command(self, fun):
        self._commands.append(fun)
        return fun

    def dispatch(self, argv=None):
        for fun in self._commands:
            command(fun)
        dispatch(argv)

    def __call__(self, fun_or_argv=None):
        '''Abbreviation of both .command() and .dispatch().'''
        if callable(fun_or_argv):
            return self.command(fun_or_argv)
        else:
            self.dispatch(fun_or_argv)

    at_top = staticmethod(at_top)
    find_entry_points = staticmethod(find_entry_points)


Parsable.Parsable = Parsable

# To support callable module, use 'from parsable import parsable'
parsable = Parsable()

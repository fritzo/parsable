'''
parsable - Lightweight argument parsing using a decorator.
http://github.com/fritzo/parsable

Copyright (c) 2011-2015, Fritz Obermeyer
Dual licensed under the MIT or GPL Version 2 licenses.
http://www.opensource.org/licenses/MIT
http://www.opensource.org/licenses/GPL-2.0
'''

import os
import sys
import time
import inspect

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
    'Decorator for parsable _commands'

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
        stop = time.time()
        sys.stderr.write('%s took %g sec\n' % (name, stop - start))

    _commands.append((name, (fun, parser)))

    return fun


def at_top(extra_depth=0):
    'Returns whether calling location is top-level parsable command'

    depth = len(inspect.stack())
    assert depth >= 5
    return depth == 5 + extra_depth


def dispatch(args=None):
    'Parses arguments to call a parsable command'

    if args is None:
        args = sys.argv[1:]
        sys.stderr.write('# python %s\n' % ' '.join(sys.argv))
    else:
        sys.stderr.write('# (in %s) %s\n' % (sys.argv[0], ' '.join(args)))

    if not args:
        script = os.path.split(sys.argv[0])[-1]
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


class Parsable:
    'Collects parsable commands locally for optional dispatch'

    def __init__(self):
        self._commands = []

    def command(self, fun):
        self._commands.append(fun)
        return fun

    def dispatch(self, args=None):
        for fun in self._commands:
            command(fun)
        dispatch(args)

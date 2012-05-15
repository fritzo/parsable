
'''
parsable.py - A lightweight decorator-based command line parser
http://github.com/fritzo/parsable.py

Copyright (c) 2011, Fritz Obermeyer
Dual licensed under the MIT or GPL Version 2 licenses.
http://www.opensource.org/licenses/MIT
http://www.opensource.org/licenses/GPL-2.0
'''

import os
import sys
import inspect

__commands = []


def command(fun):
    'decorator for parsable commands'

    args, vargs, kwds, defaults = inspect.getargspec(fun)
    if defaults is None:
        defaults = ()
    types = ([str] * (len(args) - len(defaults)) +
             [d.__class__ for d in defaults])

    def parser(*args, **kwds):
        assert not kwds, 'TODO parse keyword arguments'
        types_etc = types + [str] * (len(args) - len(types))  # for vargs
        fun(*tuple(t(a) for a, t in zip(args, types_etc)))

    name = fun.__name__.replace('_', '-')
    assert fun.__doc__, 'missing docstring for %s' % name
    __commands.append((name, (fun, parser)))

    return fun


def at_top(extra_depth=0):
    'returns whether calling location is top-level parsable command'

    depth = len(inspect.stack())
    assert depth >= 5
    return depth == 5 + extra_depth


def dispatch(args=None):
    'parses arguments to call a parsable command'

    if args is None:
        args = sys.argv[1:]

    if not args:
        print 'Usage: %s COMMAND [ARGS] [KWDS]' % os.path.split(sys.argv[0])[-1]
        for name, (fun, _) in  __commands:
            print '\n%s %s\n    %s' % (
                    name,
                    inspect.formatargspec(*inspect.getargspec(fun)),
                    fun.__doc__.strip(),
                    )
        sys.exit(1)

    cmd, args, kwds = args[0], args[1:], {}
    while args and '=' in args[-1]:
        key, val = args.pop().split('=', 1)
        kwds[key] = val
    dict(__commands)[cmd.replace('_', '-')][1](*args, **kwds)

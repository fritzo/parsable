
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
import time
import inspect

__commands = []


def command(fun):
    'Decorator for parsable commands'

    args, vargs, kwargs, defaults = inspect.getargspec(fun)
    if defaults is None:
        defaults = ()
    arg_types = ([str] * (len(args) - len(defaults)) +
                 [d.__class__ for d in defaults])
    kwd_types = dict(zip(args, arg_types))

    name = fun.__name__.replace('_', '-')
    assert fun.__doc__, 'missing docstring for %s' % name

    def parser(*args, **kwargs):
        varg_types = arg_types + [str] * (len(args) - len(arg_types))
        typed_args = tuple(t(a) for a, t in zip(args, varg_types))
        typed_kwargs = dict([(k, kwd_types.get(k, str)(v))
                           for k, v in kwargs.iteritems()])
        start = time.time()
        fun(*typed_args, **typed_kwargs)
        stop = time.time()
        sys.stderr.write('%s took %g sec\n' % (name, stop - start))

    __commands.append((name, (fun, parser)))

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
        print 'Usage: %s COMMAND [ARGS] [KWDS]' % script
        for name, (fun, _) in  __commands:
            print '\n%s %s\n    %s' % (
                    name,
                    inspect.formatargspec(*inspect.getargspec(fun)),
                    fun.__doc__.strip(),
                    )
        sys.exit(1)

    cmd, args, kwargs = args[0], args[1:], {}
    while args and '=' in args[-1]:
        key, val = args.pop().split('=', 1)
        kwargs[key] = val
    dict(__commands)[cmd.replace('_', '-')][1](*args, **kwargs)

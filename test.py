import subprocess


def run(*args, **kwargs):
    command = ['python', 'example.py']
    for arg in args:
        command.append(str(arg))
    for key, val in kwargs.items():
        val = str(val)
        if len(val.split()) > 1:
            val = "'{0}'".format(val)
        command.append("{0}={1}".format(key, val))
    print(' '.join(command))
    subprocess.check_call(command)


def test():
    run('example_command', 'test1')
    run('example-command', 'test2')
    run('example-command', 'test3', 3)
    run('example-command', 'test4', 4, 'blah')
    run('example-command', 'test5', optional_string='ghjk')
    run('example-command', 'test6', optional_int=0)
    run('another-command')
    run('print-all-strings', *map(str, range(10)))

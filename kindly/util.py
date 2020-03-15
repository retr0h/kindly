# Copyright (c) 2020 John Dewey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import contextlib
import os
import sys

import click
import colorama
import plumbum
import yaml

colorama.init(autoreset=True)


def color_text(color, msg):
    return '{}{}{}{}'.format(
        color, msg, colorama.Style.RESET_ALL, colorama.Fore.RESET
    )


def red_text(msg):
    return color_text(colorama.Fore.RED, msg)


def cyan_text(msg):
    return color_text(colorama.Fore.CYAN, msg)


def yellow_text(msg):
    return color_text(colorama.Fore.YELLOW, msg)


def sysexit(code=1):
    sys.exit(code)


def sysexit_with_message(msg, code=1):
    click.echo(red_text('ERROR: {}'.format(msg)))
    sysexit(code)


def safe_load(string):
    '''Parse the provided string returns a dict.

    :param string: A string to be parsed.
    :return: dict
    '''
    try:
        return yaml.safe_load(string) or {}
    except yaml.scanner.ScannerError as e:
        sysexit_with_message(str(e))


def safe_load_file(filename):
    '''Parse the provided YAML file and returns a dict.

    :param filename: A string containing an absolute path to the file to parse.
    :return: dict
    '''
    with open_file(filename) as stream:
        return safe_load(stream)


@contextlib.contextmanager
def open_file(filename, mode='r'):
    '''Open the provide file safely and returns a file type.

    :param filename: A string containing an absolute path to the file to open.
    :param mode: A string describing the way in which the file will be used.
    :return: file type
    '''
    with open(filename, mode) as stream:
        yield stream


def run(commands, stream=False, debug=False, env={}):
    cmd = get_run_command(commands, env=env)
    return run_command(cmd, stream=stream, debug=debug)


def get_run_command(commands, env=os.environ):
    __cmd = plumbum.local
    __cmd.env = env
    try:
        for partial in commands:
            __cmd = __cmd[partial]

        return __cmd
    except plumbum.CommandNotFound as e:
        msg = "Command not found '{}'".format(e.program)
        sysexit_with_message(msg)


def run_command(cmd, stream=False, debug=False):
    try:
        if stream:
            return _run_streaming_command(cmd)
        return 0, cmd()
    except plumbum.commands.processes.ProcessExecutionError as e:
        msg = 'Command failed to execute\n\n{}'.format(e.stderr)
        sysexit_with_message(msg)


def _run_streaming_command(cmd):
    try:
        for stdout, stderr in cmd.popen().iter_lines():
            if stdout:
                click.echo(stdout)
            if stderr:
                click.echo(stderr)
        return 0, ''
    except plumbum.commands.processes.ProcessExecutionError:
        return 1, ''


def safe_dump(data):
    return yaml.dump(data, default_flow_style=False, explicit_start=True)


def abort_with_message(msg):
    click.echo(red_text('ERROR: {}'.format(msg)))
    abort()


def abort():
    raise click.Abort()

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

import plumbum
import pytest

from kindly import util


@pytest.fixture
def _patched_red_text(mocker):
    return mocker.patch('kindly.util.red_text')


def test_red_text():
    x = '\x1b[31mfoo\x1b[0m\x1b[39m'

    assert x == util.red_text('foo')


def test_cyan_text():
    x = '\x1b[36mfoo\x1b[0m\x1b[39m'

    assert x == util.cyan_text('foo')


def test_sysexit():
    with pytest.raises(SystemExit) as e:
        util.sysexit()

    assert 1 == e.value.code


def test_sysexit_with_custom_code():
    with pytest.raises(SystemExit) as e:
        util.sysexit(2)

    assert 2 == e.value.code


def test_sysexit_with_message(_patched_red_text):
    with pytest.raises(SystemExit) as e:
        util.sysexit_with_message('foo')

    assert 1 == e.value.code

    msg = 'ERROR: foo'
    _patched_red_text.assert_called_once_with(msg)


def test_sysexit_with_message_and_custom_code(_patched_red_text):
    with pytest.raises(SystemExit) as e:
        util.sysexit_with_message('foo', 2)

    assert 2 == e.value.code

    msg = 'ERROR: foo'
    _patched_red_text.assert_called_once_with(msg)


def test_safe_load():
    assert {'foo': 'bar'} == util.safe_load('foo: bar')


def test_safe_load_returns_empty_dict_on_empty_string():
    assert {} == util.safe_load('')


def test_safe_load_exits_when_cannot_parse():
    data = """
---
%foo:
""".strip()

    with pytest.raises(SystemExit) as e:
        util.safe_load(data)

    assert 1 == e.value.code


def test_safe_load_file(fs):
    f = 'foo.txt'
    fs.create_file(f, contents='{"foo": "bar"}')
    x = {'foo': 'bar'}

    assert x == util.safe_load_file(f)


def test_open_file(fs):
    f = 'foo.txt'
    fs.create_file(f, contents='foo')

    with util.open_file(f) as stream:
        assert 'foo' == stream.read()


def test_get_run_command():
    commands = [
        'ls',
        '-l',
    ]
    x = '{} -l'.format(plumbum.local.which('ls'))

    assert x == str(util.get_run_command(commands))


def test_get_run_command_raises_when_command_not_found(_patched_red_text):
    commands = ['invalid']
    with pytest.raises(SystemExit) as e:
        util.get_run_command(commands)

    assert 1 == e.value.code
    msg = "ERROR: Command not found 'invalid'"
    _patched_red_text.assert_called_once_with(msg)


def test_run_command():
    cmd = util.get_run_command(['echo', 'foo'])
    x = (0, 'foo\n')

    assert x == util.run_command(cmd)


def test_run_command_raises_and_prints_stderr_on_failure(_patched_red_text):
    commands = [
        'python',
        '-c',
        'import sys; sys.exit("stderr")',
    ]
    with pytest.raises(SystemExit) as e:
        cmd = util.get_run_command(commands)
        util.run_command(cmd)

    assert 1 == e.value.code
    msg = 'ERROR: Command failed to execute\n\nstderr\n'
    _patched_red_text.assert_called_once_with(msg)


def test_run_command_streams_stdout(capsys):
    cmd = util.get_run_command(['echo', 'stdout'])
    util.run_command(cmd, stream=True)

    captured = capsys.readouterr()
    assert 'stdout\n' == captured.out


def test_run_command_streams_stderr(capsys):
    commands = [
        'python',
        '-c',
        'import sys; sys.stderr.write("stderr")',
    ]
    cmd = util.get_run_command(commands)
    util.run_command(cmd, stream=True)

    captured = capsys.readouterr()
    assert 'stderr\n' == captured.out


def test_run_command_streams_stderr_on_failure(capsys):
    commands = [
        'python',
        '-c',
        'import sys; sys.exit("stderr")',
    ]
    cmd = util.get_run_command(commands)
    util.run_command(cmd, stream=True)

    captured = capsys.readouterr()
    assert 'stderr\n' == captured.out


def test_safe_dump():
    x = """
---
foo: bar
""".lstrip()

    assert x == util.safe_dump({'foo': 'bar'})

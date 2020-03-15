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

import pytest

from kindly import config
from kindly import spec


@pytest.fixture
def config_instance():
    args = {
        'debug': False,
        'kindly_file': 'test/resources/kindly.yml',
    }
    command_args = {}

    return config.Config(args, command_args)


@pytest.fixture
def spec_instance(config_instance):
    return spec.DeploymentSpec(config_instance.kindly_file)


@pytest.fixture
def patched_run(mocker):
    return mocker.patch('kindly.util.run')


@pytest.fixture
def patched_get_run_command(mocker):
    return mocker.patch('kindly.util.get_run_command')


@pytest.fixture
def patched_run_command(mocker):
    m = mocker.patch('kindly.util.run_command')
    m.return_value = mocker.Mock(spec=open)

    return m

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

from kindly import driver


@pytest.fixture
def _patched_kind_drivr_get(mocker):
    return mocker.patch('kindly.driver.Kind.get')


@pytest.fixture
def _instance(config_instance, spec_instance):
    return driver.Kind(config_instance, spec_instance)


def test_create(_instance, patched_run):
    _instance.create()

    commands = [
        'kind',
        'create',
        'cluster',
        '--name',
        'kindly-foo',
    ]
    patched_run.assert_called_once_with(
        commands, stream=False, debug=False, env=_instance._config.env
    )


def test_delete(_instance, patched_run):
    _instance.delete()

    commands = [
        'kind',
        'delete',
        'cluster',
        '--name',
        'kindly-foo',
    ]
    patched_run.assert_called_once_with(
        commands, stream=False, debug=False, env=_instance._config.env
    )


def test_get(_instance, patched_run):
    patched_run.return_value = 0, 'stdout'

    x = ['stdout']
    assert x == _instance.get()

    commands = [
        'kind',
        'get',
        'clusters',
    ]
    patched_run.assert_called_once_with(
        commands, stream=False, debug=False, env=_instance._config.env
    )


def test_exists(_instance, _patched_kind_drivr_get):
    _patched_kind_drivr_get.return_value = [
        'foo',
        'bar',
        'kindly-foo',
    ]

    assert _instance.exists()


def test_exists_cluster_does_not_exist(_instance, _patched_kind_drivr_get):
    _patched_kind_drivr_get.return_value = [
        'foo',
        'bar',
    ]

    assert not _instance.exists()


def test_load_image(_instance, patched_run):
    _instance.load_image()

    commands = [
        'kind',
        'load',
        'docker-image',
        '--name',
        'kindly-foo',
        'test/kindly:latest',
    ]
    patched_run.assert_called_once_with(
        commands, stream=False, debug=False, env=_instance._config.env
    )

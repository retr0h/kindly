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

from kindly import orchestrator


@pytest.fixture
def _instance(config_instance, spec_instance):
    return orchestrator.Kubectl(config_instance, spec_instance)


def test_set_context(_instance, patched_run):
    _instance.set_context()

    commands = [
        'kubectl',
        'cluster-info',
        '--context',
        'kind-kindly-foo',
    ]
    patched_run.assert_called_once_with(
        commands, stream=False, debug=False, env=_instance._config.env
    )


def test_set_context_with_debug(_instance, patched_run):
    pass


def test_create_namespace(_instance, patched_run):
    _instance.create_namespace()

    commands = [
        'kubectl',
        'create',
        'namespace',
        'foo',
    ]
    patched_run.assert_called_once_with(
        commands, stream=False, debug=False, env=_instance._config.env
    )


def test_create_namespace_with_debug(_instance, patched_run):
    pass


def test_create_objects(_instance, patched_run):
    _instance.create_objects()

    commands = [
        'kubectl',
        'create',
        '--save-config',
        '-f',
        'test/resources/configs/',
    ]
    patched_run.assert_called_once_with(
        commands, stream=False, debug=False, env=_instance._config.env
    )


def test_update_objects(_instance, patched_run):
    _instance.update_objects()

    commands = [
        'kubectl',
        'apply',
        '-f',
        'test/resources/configs/',
    ]
    patched_run.assert_called_once_with(
        commands, stream=False, debug=False, env=_instance._config.env
    )

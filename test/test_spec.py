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

from kindly import spec


@pytest.fixture
def _instance(config_instance):
    return spec.DeploymentSpec(config_instance.kindly_file)


def test_cluster_name(_instance):
    x = 'kindly-foo'

    assert x == _instance.cluster_name


def test_image(_instance):
    x = 'test/kindly:latest'

    assert x == _instance.image


def test_image_repository(_instance):
    x = 'test/kindly'

    assert x == _instance.image_repository


def test_image_tag(_instance):
    x = 'latest'

    assert x == _instance.image_tag


def test_packager_name(_instance):
    x = 'foo'

    assert x == _instance.packager_name


def test_packager_chart(_instance):
    x = 'test/resources/charts/foo'

    assert x == _instance.packager_chart


def test_packager_namespace(_instance):
    x = 'foo'

    assert x == _instance.packager_namespace


def test_configs_path(_instance):
    x = 'test/resources/configs/'

    assert x == _instance.configs_path

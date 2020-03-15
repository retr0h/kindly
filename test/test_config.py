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

import os


def test_kindly_file_property(config_instance):
    x = os.path.abspath('test/resources/kindly.yml')

    assert x == config_instance.kindly_file


def test_debug_property(config_instance):
    assert not config_instance.debug


def test_debug_setter(config_instance):
    config_instance.debug = True

    assert config_instance.debug


def test_env_property(config_instance):
    env = os.environ.copy()

    assert env == config_instance.env


def test_stream_property(config_instance):
    assert not config_instance.stream


def test_stream_property_true_when_debug_enabled(config_instance):
    config_instance.debug = True

    assert config_instance.stream


def test_spinner_property(config_instance):
    assert config_instance.spinner


def test_spinner_property_false_when_debug_enabled(config_instance):
    config_instance.debug = True

    assert not config_instance.spinner

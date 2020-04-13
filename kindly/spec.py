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

from kindly import util

DEFAULT_KINDLY_FILE = 'kindly.yml'
DEFAULT_CLUSTER_PREFIX = 'kindly'


class DeploymentSpec(object):
    '''A class representing `kindly_file`. '''

    def __init__(self, kindly_file):
        self._data = self._get_config(kindly_file)
        self._template_spec = self._data['spec']['template']['spec']
        self._validate = self._validate(kindly_file)

    @property
    def cluster_name(self):
        name = self._data['metadata']['name']

        return f'{DEFAULT_CLUSTER_PREFIX}-{name}'

    @property
    def configs_path(self):
        return self._template_spec['configs']['configPath']

    @property
    def image(self):
        image_repository = self.image_repository
        image_tag = self.image_tag

        return f'{image_repository}:{image_tag}'

    @property
    def image_repository(self):
        return self._template_spec['image']['repository']

    @property
    def image_tag(self):
        return self._template_spec['image']['tag']

    @property
    def packager_name(self):
        return self._template_spec['packager']['name']

    @property
    def packager_chart(self):
        return self._template_spec['packager']['chart']

    @property
    def packager_namespace(self):
        return self._template_spec['packager']['namespace']

    def template_spec_contains(self, attrib):
        return attrib in self._template_spec

    def _get_config(self, kindly_file):
        return util.safe_load_file(kindly_file)

    def _validate(self, kindly_file):
        # TODO(jodewey): Move validation into a better library.
        assert 'core/v1alpha1' == self._data['apiVersion']
        assert 'KindlyDeployment' == self._data['kind']

        # Template spec validation
        __req_attributes = {
            'packager': {'name', 'chart', 'namespace'},
            'image': {'repository', 'pullPolicy', 'tag'},
            'configs': {'configPath'},
        }
        for attrib in self._template_spec:
            if (
                not set(self._template_spec[attrib])
                == __req_attributes[attrib]
            ):
                msg = (
                    f"kindly_file validation failed for template:spec:{attrib}"
                    f" required attribs missing {__req_attributes[attrib]}"
                )
                util.abort_with_message(msg)

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


class Kubectl(object):
    '''A class responsible for managing the interactions with `Helm`. '''

    def __init__(self, config, spec):
        self._config = config
        self._deployment_spec = spec

    def set_context(self):
        '''Sets `kubectl` context to current Kind cluster. '''

        cluster_name = self._deployment_spec.cluster_name
        kube_context = f'kind-{cluster_name}'

        commands = [
            'kubectl',
            'cluster-info',
            '--context',
            kube_context,
        ]

        util.run(
            commands,
            stream=False,
            debug=self._config.debug,
            env=self._config.env,
        )

    def create_namespace(self):
        '''Create a namespace in the current Kind cluster. '''

        commands = [
            'kubectl',
            'create',
            'namespace',
            self._deployment_spec.packager_namespace,
        ]

        util.run(
            commands,
            stream=False,
            debug=self._config.debug,
            env=self._config.env,
        )

    def create_objects(self):
        '''Create objects defined in the path on Kind cluster. '''

        commands = [
            'kubectl',
            'create',
            '--save-config',
            '-f',
            self._deployment_spec.configs_path,
        ]

        util.run(
            commands,
            stream=False,
            debug=self._config.debug,
            env=self._config.env,
        )

    def update_objects(self):
        '''Apply changes to objects defined in the path on Kind cluster. '''

        commands = [
            'kubectl',
            'apply',
            '-f',
            self._deployment_spec.configs_path,
        ]

        util.run(
            commands,
            stream=False,
            debug=self._config.debug,
            env=self._config.env,
        )

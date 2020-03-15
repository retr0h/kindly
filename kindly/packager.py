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


class Helm(object):
    '''A class responsible for managing the interactions with `Helm`. '''

    def __init__(self, config, spec):
        self._config = config
        self._deployment_spec = spec

    def install(self):
        '''Run Helm install. '''

        commands = [
            'helm',
            'install',
            '-n',
            self._deployment_spec.packager_namespace,
            self._deployment_spec.packager_name,
            self._deployment_spec.packager_chart,
        ]

        util.run(
            commands,
            stream=False,
            debug=self._config.debug,
            env=self._config.env,
        )

    def upgrade(self):
        '''Run Helm upgrade. '''

        commands = [
            'helm',
            'upgrade',
            '-n',
            self._deployment_spec.packager_namespace,
            self._deployment_spec.packager_name,
            self._deployment_spec.packager_chart,
        ]

        util.run(
            commands,
            stream=False,
            debug=self._config.debug,
            env=self._config.env,
        )

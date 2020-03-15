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


class Kind(object):
    '''A class responsible for managing the interactions with `Kind`. '''

    def __init__(self, config, spec):
        self._config = config
        self._deployment_spec = spec

    def create(self):
        '''Create a new Kind cluster. '''

        commands = [
            'kind',
            'create',
            'cluster',
            '--name',
            self._deployment_spec.cluster_name,
        ]

        util.run(
            commands,
            stream=self._config.stream,
            debug=self._config.debug,
            env=self._config.env,
        )

    def delete(self):
        '''Delete a Kind cluster. '''

        commands = [
            'kind',
            'delete',
            'cluster',
            '--name',
            self._deployment_spec.cluster_name,
        ]

        util.run(
            commands,
            stream=self._config.stream,
            debug=self._config.debug,
            env=self._config.env,
        )

    def get(self):
        '''Returns list of all Kind clusters. '''

        commands = [
            'kind',
            'get',
            'clusters',
        ]

        exit_code, output = util.run(
            commands,
            stream=False,
            debug=self._config.debug,
            env=self._config.env,
        )

        return [l for l in output.split('\n') if l]

    def exists(self):
        '''Returns True if cluster already exists. '''

        return self._deployment_spec.cluster_name in self.get()

    def load_image(self):
        '''Load image into cluster. '''

        image = self._deployment_spec.image

        commands = [
            'kind',
            'load',
            'docker-image',
            '--name',
            self._deployment_spec.cluster_name,
            image,
        ]

        util.run(
            commands,
            stream=self._config.stream,
            debug=self._config.debug,
            env=self._config.env,
        )

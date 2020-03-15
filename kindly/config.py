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


class Config(object):
    """A class representing Kindly's. higher level config. """

    def __init__(self, args, command_args):
        self._args = args
        self._command_args = command_args
        self._debug = self._args.get('debug')

    @property
    def kindly_file(self):
        '''Returns string with path to Kindly file.

        The CLI uses @click's file type.  This allows some level
        of error handling.  We re-open/marshal the file path returned
        by this method, so our unit tests follow the same code path
        as our CLI.

        :return: str
        '''
        return os.path.abspath(self._args['kindly_file'])

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    @property
    def env(self):
        return os.environ.copy()

    @property
    def stream(self):
        return self._debug

    @property
    def spinner(self):
        return not self._debug

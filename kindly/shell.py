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

import click
import click_completion

import kindly
from kindly import cmd
from kindly import spec

click_completion.init()


@click.group()
@click.option(
    '--debug/--no-debug',
    default=False,
    help='Enable or disable debug mode. Default is disabled.',
)
@click.option(
    '--kindly-file',
    default=spec.DEFAULT_KINDLY_FILE,
    help='Path to kindly file.  [{}]'.format(spec.DEFAULT_KINDLY_FILE),
    type=click.File('r'),
)
@click.version_option(version=kindly.__version__)
@click.pass_context
def main(ctx, debug, kindly_file):  # pragma: no cover
    '''
    \b
    kindly - Kind lifecycle manager.

    '''  # noqa: H404,H405
    ctx.obj = {}
    ctx.obj['args'] = {}
    ctx.obj['args']['debug'] = debug
    ctx.obj['args']['kindly_file'] = kindly_file.name


main.add_command(cmd.apply.apply)
main.add_command(cmd.create.create)
main.add_command(cmd.delete.delete)
main.add_command(cmd.get.get)

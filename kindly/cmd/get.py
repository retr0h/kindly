import click

from kindly import config
from kindly import driver
from kindly import spec
from kindly import util


@click.command()
@click.pass_context
def get(ctx):
    '''Get all Kind clusters. '''

    args = ctx.obj.get('args')
    command_args = {}

    c = config.Config(args, command_args)
    s = spec.DeploymentSpec(c.kindly_file)
    d = driver.Kind(c, s)

    data = {'clusters': d.get()}
    click.echo(util.safe_dump(data))

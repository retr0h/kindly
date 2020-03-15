import click
import halo

from kindly import config
from kindly import driver
from kindly import spec


@click.command()
@click.pass_context
def delete(ctx):
    '''Delete an existing cluster. '''

    args = ctx.obj.get('args')
    command_args = {}

    c = config.Config(args, command_args)
    s = spec.DeploymentSpec(c.kindly_file)
    d = driver.Kind(c, s)

    with halo.Halo(
        text='Deleting cluster', spinner='dots', enabled=c.spinner
    ) as spinner:
        d.delete()
        spinner.succeed()

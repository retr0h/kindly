import click
import halo

from kindly import config
from kindly import driver
from kindly import orchestrator
from kindly import packager
from kindly import spec
from kindly import util


@click.command()
@click.pass_context
def create(ctx):
    '''Create a new cluster. '''

    args = ctx.obj.get('args')
    command_args = {}

    c = config.Config(args, command_args)
    s = spec.DeploymentSpec(c.kindly_file)
    d = driver.Kind(c, s)
    p = packager.Helm(c, s)
    o = orchestrator.Kubectl(c, s)

    cluster_name = s.cluster_name
    if d.exists():
        msg = f"Cluster '{cluster_name}' already exists"
        util.abort_with_message(msg)

    with halo.Halo(
        text=f"Creating cluster '{cluster_name}'",
        spinner='dots',
        enabled=c.spinner,
    ) as spinner:
        d.create()
        spinner.succeed()

    if s.template_spec_contains('image'):
        with halo.Halo(
            text=f"Loading image '{s.image}'",
            spinner='dots',
            enabled=c.spinner,
        ) as spinner:
            d.load_image()
            spinner.succeed()

    if s.template_spec_contains('packager'):
        with halo.Halo(
            text=f"Create package namespace '{s.packager_namespace}'",
            spinner='dots',
            enabled=c.spinner,
        ) as spinner:
            o.create_namespace()
            spinner.succeed()

        with halo.Halo(
            text=f"Install package '{s.packager_chart}'",
            spinner='dots',
            enabled=c.spinner,
        ) as spinner:
            p.install()
            spinner.succeed()

    if s.template_spec_contains('configs'):
        with halo.Halo(
            text=f"Create objects from yaml definitions in '{s.configs_path}'",
            spinner='dots',
            enabled=c.spinner,
        ) as spinner:
            o.create_objects()
            spinner.succeed()

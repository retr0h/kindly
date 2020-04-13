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
def apply(ctx):
    '''Apply configs to an existing cluster. '''

    args = ctx.obj.get('args')
    command_args = {}

    c = config.Config(args, command_args)
    s = spec.DeploymentSpec(c.kindly_file)
    d = driver.Kind(c, s)
    p = packager.Helm(c, s)
    o = orchestrator.Kubectl(c, s)

    if not d.exists():
        msg = (
            f"Cluster '{s.cluster_name}' does not exist.  "
            "Please execute create subcommand."
        )
        util.abort_with_message(msg)

    with halo.Halo(
        text="Setting orchestrator's context",
        spinner='dots',
        enabled=c.spinner,
    ) as spinner:
        o.set_context()
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
            text=f"Upgrade package '{s.packager_chart}'",
            spinner='dots',
            enabled=c.spinner,
        ) as spinner:
            p.upgrade()
            spinner.succeed()

    if s.template_spec_contains('configs'):
        with halo.Halo(
            text=f"Apply updated configs in '{s.configs_path}'",
            spinner='dots',
            enabled=c.spinner,
        ) as spinner:
            o.update_objects()
            spinner.succeed()

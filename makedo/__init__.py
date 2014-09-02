import pprint

import click

from core import Core

core = None

@click.group()
@click.option('--verbose', is_flag=True)
def cli(verbose):
    """Command line interface for DigitalOcean"""
    global core
    core = Core()


@cli.command()
@click.argument('droplet_name')
@click.argument('snapshot_name')
@click.option('--region', default='sfo1', help="The region to create the droplet in")
@click.option('--size', default='1gb', help="The size of the droplet")
@click.option('--ssh-key', help="The name of the ssh-key to bind the droplet with")
def create(droplet_name, snapshot_name, region, size, ssh_key):
    """Create a droplet from a snapshot."""
    # TODO: Accept a list of the names of ssh-keys
    click.echo("Creating the droplet...")
    core.create_droplet_from_snapshot(droplet_name, region,
                                      snapshot_name, ssh_key=[ssh_key], size=size)
    click.echo("Droplet created.")


@click.group()
def list():
    """List resources/configurations available on the DigitalOcean account"""
    pass


@list.command()
def keys():
    click.echo(pprint.pformat(core.list_ssh_keys()))


@list.command()
def sizes():
    click.echo(pprint.pformat(core.list_sizes()))


@list.command()
def snapshots():
    click.echo(pprint.pformat(core.list_snapshots()))

cli.add_command(list)

import pprint

import click

from core import Core

core = None

@click.group()
@click.option('--verbose', is_flag=True)
def cli(verbose):
    """
    Command line interface for DigitalOcean. \n
    Important: Provide the API key in environment variable DIGITALOCEAN_API_KEY
    """
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
    droplet = core.create_droplet_from_snapshot(droplet_name, region,
                                      snapshot_name, ssh_keys=[ssh_key], size=size)
    click.echo("Droplet created.")
    click.echo("Droplet IP: " + droplet.ip_address) 

    
@cli.command()
@click.argument('droplet_name')
@click.option('--snapshot', help="The name of the snapshot " \
              "if you want to make a snapshot before destroying the droplet")
def destroy(droplet_name, snapshot):
    """(Optionally) create a snapshot and destroy a droplet"""
    if snapshot:
        core.snapshot_and_destroy(droplet_name, snapshot)
    else:
        core.destroy(droplet_name)


@click.group()
def remove():
    """Remove snapshots or ssh keys"""
    pass


@remove.command()
@click.argument('snapshot_name')
def snapshot(snapshot_name):
    """Remove a snapshot from the account"""
    response = core.remove_snapshot(snapshot_name)
    if response is not None:
        click.echo("Snapshot removed!")
    else:
        click.echo("Failed to remove the snapshot!")

                
@click.group()
def list():
    """List resources/configurations available on the DigitalOcean account"""
    pass


@list.command()
def keys():
    """List ssh keys"""
    click.echo(pprint.pformat(core.list_ssh_keys()))


@list.command()
def sizes():
    """List usable sizes of droplets"""
    click.echo(pprint.pformat(core.list_sizes()))


@list.command()
def snapshots():
    """List snapshots/private images"""
    click.echo(pprint.pformat(core.list_snapshots()))

    
cli.add_command(list)
cli.add_command(remove)

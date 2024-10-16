
import os
import click

from command.command_init import command_init
from hook.hook import Hooks
from command.command_set_config import command_set_config

@click.group()
def cli():
    """A command line tool for managing file backups."""
    pass

@click.command()
def init():
    """initialize the local repository."""
    mode = click.prompt('Please enter the mode: ORIGINAL/ENCRYPTED', default='ORIGINAL')
    password = click.prompt('Please enter the password', default='default_password')
    local_path = click.prompt('Please enter the local_path', default=os.getcwd())
    remote_path = click.prompt('Please enter the remote_path', default='')
    app_id = click.prompt('Please enter the app_id', default=os.getenv("BDWP_APP_ID", ""))
    secret_key = click.prompt('Please enter the secret_key', default=os.getenv("BDWP_SECRET_KEY", ""))
    app_key = click.prompt('Please enter the app_key', default=os.getenv("BDWP_APP_KEY", ""))
    sign_code = click.prompt('Please enter the sign_code', default=os.getenv("BDWP_SIGN_CODE", ""))
    expires_in = click.prompt('Please enter the expires_in', default=os.getenv("BDWP_EXPIRES_IN", ""))
    refresh_token = click.prompt('Please enter the refresh_token', default=os.getenv("BDWP_REFRESH_TOKEN", ""))
    access_token = click.prompt('Please enter the access_token', default=os.getenv("BDWP_ACCESS_TOKEN", ""))

    Hooks.init_constant()
    command_init(mode, password, local_path, remote_path, app_id, secret_key, app_key, sign_code, expires_in, refresh_token, access_token)

@click.command()
@click.argument('key')
@click.argument('value')
def set_config(key, value):
    """change file-git config_instance, key-value pairs."""
    Hooks.execute()
    command_set_config(key, value)
    

@click.command()
def clone():
    """clone remote repository."""
    Hooks.execute()
    click.echo(f"command-clone.")

@click.command()
def refresh_token():
    """refresh Baidu Wangpan access token."""
    Hooks.execute()
    click.echo(f"command-refresh_token.")

@click.command()
def pull():
    """pull files from the remote repository."""
    Hooks.execute()
    click.echo(f"command-pull.")

@click.command()
def push():
    """push files to the remote repository."""
    Hooks.execute()
    click.echo(f"command-push.")

@click.command()
def queue():
    """contiune queue action."""
    Hooks.execute()
    click.echo(f"command-queue.")


cli.add_command(init)
cli.add_command(clone)
cli.add_command(set_config)
cli.add_command(refresh_token)

cli.add_command(pull)
cli.add_command(push)
cli.add_command(queue)

if __name__ == "__main__":
    cli()

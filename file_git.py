
import os
import click

from command.command_init import command_init
from hook.hook import Hooks
from command.command_set_config import command_set_config
from command.command_clone import command_clone
from command.command_pull import command_pull
from command.command_push import command_push
from command.command_queue import command_queue
from command.command_refresh_token import command_refresh_token
from command.command_verify import command_verify
from command.command_diff import command_diff
from command.command_encrypted import command_encrypted

from support import file_support

@click.group()
def cli():
    """A command line tool for managing file backups."""
    pass

@click.command()
def init():
    """initialize the local repository."""
    mode = click.prompt('Please enter the mode: ORIGINAL/ENCRYPTED', default='ORIGINAL')
    password = click.prompt('Please enter the password', default='default_password')
    virtual_local_path = click.prompt('Please enter the virtual_local_path', default=file_support.virtual_get_current_path())
    virtual_remote_path = click.prompt('Please enter the virtual_remote_path', default='')
    app_id = click.prompt('Please enter the app_id', default=os.getenv("BDWP_APP_ID", ""))
    secret_key = click.prompt('Please enter the secret_key', default=os.getenv("BDWP_SECRET_KEY", ""))
    app_key = click.prompt('Please enter the app_key', default=os.getenv("BDWP_APP_KEY", ""))
    sign_code = click.prompt('Please enter the sign_code', default=os.getenv("BDWP_SIGN_CODE", ""))
    expires_in = click.prompt('Please enter the expires_in', default=os.getenv("BDWP_EXPIRES_IN", ""))
    refresh_token = click.prompt('Please enter the refresh_token', default=os.getenv("BDWP_REFRESH_TOKEN", ""))
    access_token = click.prompt('Please enter the access_token', default=os.getenv("BDWP_ACCESS_TOKEN", ""))

    command_init(mode, password, virtual_local_path, virtual_remote_path, app_id, secret_key, app_key, sign_code, expires_in, refresh_token, access_token)

@click.command()
@click.argument('key')
@click.argument('value')
def set_config(key, value):
    """change file-git config_instance, key-value pairs."""
    Hooks.base_hook()
    command_set_config(key, value)

@click.command()
def clone():
    """clone remote repository."""
    # Hooks.base_hook()
    mode = click.prompt('Please enter the mode: ORIGINAL/ENCRYPTED', default='ORIGINAL')
    password = click.prompt('Please enter the password', default='default_password')
    virtual_local_path = click.prompt('Please enter the virtual_local_path', default=file_support.virtual_get_current_path())
    virtual_remote_path = click.prompt('Please enter the virtual_remote_path', default='')
    app_id = click.prompt('Please enter the app_id', default=os.getenv("BDWP_APP_ID", ""))
    secret_key = click.prompt('Please enter the secret_key', default=os.getenv("BDWP_SECRET_KEY", ""))
    app_key = click.prompt('Please enter the app_key', default=os.getenv("BDWP_APP_KEY", ""))
    sign_code = click.prompt('Please enter the sign_code', default=os.getenv("BDWP_SIGN_CODE", ""))
    expires_in = click.prompt('Please enter the expires_in', default=os.getenv("BDWP_EXPIRES_IN", ""))
    refresh_token = click.prompt('Please enter the refresh_token', default=os.getenv("BDWP_REFRESH_TOKEN", ""))
    access_token = click.prompt('Please enter the access_token', default=os.getenv("BDWP_ACCESS_TOKEN", ""))

    Hooks.init_constant()
    command_clone(mode, password, virtual_local_path, virtual_remote_path, app_id, secret_key, app_key, sign_code, expires_in, refresh_token, access_token)

@click.command()
def refresh_token():
    """refresh Baidu Wangpan access token."""
    Hooks.base_hook()
    command_refresh_token()

@click.command()
def pull():
    """pull files from the remote repository."""
    Hooks.base_hook()
    Hooks.clean_trash()
    command_pull()

@click.command()
def push():
    """push files to the remote repository."""
    Hooks.base_hook()
    Hooks.clean_trash()
    command_push()

@click.command()
def queue():
    """contiune queue action."""
    Hooks.base_hook()
    Hooks.clean_trash()
    command_queue()

@click.command()
def verify():
    """verify local and remote dictory."""
    Hooks.base_hook()
    Hooks.clean_trash()
    command_verify()

@click.command()
@click.argument('strategy')
@click.argument('source_path')
@click.argument('target_path')
def command_diff(strategy, virtual_source_path, virtual_target_path):
    """change file-git config_instance, key-value pairs."""
    Hooks.base_hook()
    command_diff(strategy, virtual_source_path, virtual_target_path)

@click.command()
@click.option('--all-flag', '-a', help='encrypted all files.')
def command_encrypted(all_flag):
    """encrypted files but not upload, if -a is false, will only encrtptes only in local files."""
    Hooks.base_hook()
    command_encrypted(all_flag)

cli.add_command(init)
cli.add_command(clone)
cli.add_command(set_config)
cli.add_command(refresh_token)

cli.add_command(pull)
cli.add_command(push)
cli.add_command(queue)
cli.add_command(verify)

cli.add_command(command_diff)
cli.add_command(command_encrypted)

if __name__ == "__main__":
    cli()

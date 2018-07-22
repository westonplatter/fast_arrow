# from __future__ import absolute_import, division, print_function

import click
import functools

from fast_arrow.auth import Session
from fast_arrow.resources.user import User

def get_username_password(config_file):
    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)

    username = config['account']['username']
    password = config['account']['password']

    account = {
            'username': username,
            'password': password}
    return account


def common_options(func):
    @click.option('--debug/--no-debug', default=False)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@click.group()
def cli():
    pass

@cli.command()
@common_options
def check(debug):
    click.echo("fa.check -- you're good to go")

@cli.command()
@common_options
def get_token(debug):
    account = get_username_password('config.debug.ini')
    u = account['username']
    p = account['password']
    token = Session.login(u, p)
    click.echo(token)

@cli.command()
@common_options
def get_user(debug):
    account = get_username_password('config.debug.ini')
    u = account['username']
    p = account['password']
    token = Session.login(u, p)
    data = User.fetch(token)
    print(data)



if __name__ == '__main__':
    cli()

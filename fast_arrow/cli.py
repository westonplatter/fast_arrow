import click
import functools
import configparser
import pdb
from fast_arrow.resources.auth import Auth
from fast_arrow.resources.user import User
from fast_arrow.resources.position import Position
from fast_arrow.resources.option_position import OptionPosition
from fast_arrow.resources.option import Option
from fast_arrow.resources.stock import Stock


def get_username_password(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return [config['account']['username'], config['account']['password']]


def get_token(config_file):
    username, password = get_username_password(config_file)
    token = Auth.login(username, password)
    return token


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
def get_user(debug):
    token = get_token('config.debug.ini')
    data = User.fetch(token)
    print(data)


@cli.command()
@common_options
def get_positions(debug):
    token = get_token('config.debug.ini')
    data = Position.all(token)
    if debug:
        pdb.set_trace()


@cli.command()
@common_options
def get_option_positions(debug):
    token = get_token('config.debug.ini')
    data = OptionPosition.all(token)
    if debug:
        pdb.set_trace()


@cli.command()
@common_options
@click.option('--id', default=None)
def get_option_instrument(debug, id):
    token = get_token('config.debug.ini')
    bearer = Auth.get_oauth_token(token)
    data = Option.fetch(bearer, id)
    if debug:
        pdb.set_trace()


@cli.command()
@common_options
@click.option('--id', default=None)
def get_option_marketdata(debug, id):
    token = get_token('config.debug.ini')
    bearer = Auth.get_oauth_token(token)
    data = Option.marketdata(bearer, id)
    if debug:
        pdb.set_trace()


if __name__ == '__main__':
    cli()

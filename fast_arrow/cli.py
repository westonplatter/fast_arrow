import click
import functools


# def get_username_password(config_file):
#     import configparser
#     config = configparser.ConfigParser()
#     config.read(config_file)
#
#     username = config['account']['username']
#     password = config['account']['password']
#
#     account = {
#             'username': username,
#             'password': password}
#     return account


def common_options(func):
    @click.option('--debug/--no-debug', default=False)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@click.group()
def cli():
    pass


# @cli.command()
# @click.option('--config-file', default="config.ini", required=False)
# @click.option('--trades', default="stock",
#     type=click.Choice(['stock', 'option']), required=False)
# @click.option('--duration', default="1m")
# @click.option('--export-file', default="default.csv", required=False)
# @common_options
# def export_history(debug, duration, config_file, trades, export_file):
#     if debug and config_file == "config.ini":
#         config_file = "config.debug.ini"
#     account = get_username_password(config_file)
#
#     if trades == 'stock':
#         stock_orders = fetch.stock_orders(account, {})
#         click.echo("-- sm: Fetched {} stock orders".format(len(stock_orders)))
#
#         click.echo("-- sm: Exporting to stock_orders.cvs")
#         export.stock_orders(stock_orders, {})
#
#     elif trades == 'option':
#         option_orders = fetch.option_orders(account, {})
#         click.echo("-- sm: Fetched {} option orders".format(len(option_orders)))
#
#         click.echo("-- sm: Exporting to option_orders.csv")
#         export.option_orders(option_orders, {})
#
#     click.echo("-- sm: Finished")

@cli.command()
@common_options
def check(debug):
    click.echo("fa.check -- you're good to go")


if __name__ == '__main__':
    cli()

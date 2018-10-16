import click

from pysense import api


class SenseCLI(object):
    """sense context and hanger of things cli-ish"""

    def __init__(self):
        """set override for username and pass if provided"""
        self.api = api.SenseMonitor()



pass_sensecli = click.make_pass_decorator(SenseCLI, ensure=True)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS, chain=True)
@click.pass_context
def cli(ctx):
    ctx.obj = SenseCLI()


@cli.command('devices')
@click.option('--active/--inactive', default=True, is_flag=True,
              help='Use the active option for only returning devices which '
                   'are currently active.')
@click.pass_obj
def devices(sensecli, active):
    api = sensecli.api
    if active:
        devices = api.active_devices
    else:
        devices = api.devices

    click.echo(devices)


@cli.command('trend')
@click.option('--period', type=click.Choice(['daily',
                                             'weekly',
                                             'monthly',
                                             'yearly']))
def trend(period):
    click.echo('trend period %s' % trend)


if __name__ == "__main__":
    """run the command line interface"""
    cli()


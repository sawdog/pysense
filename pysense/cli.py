import click

from pysense import api
import versioneer


class SenseCLI(object):
    """sense context and hanger of things cli-ish"""

    usage = False
    production = False

    def __init__(self):
        """set override for username and pass if provided"""
        self.api = api.SenseMonitor()



pass_sensecli = click.make_pass_decorator(SenseCLI, ensure=True)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(versioneer.get_version())
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS,
             chain=True,
             invoke_without_command=True)
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
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


@cli.command('active_power')
@click.pass_obj
def active_power(sensecli):
    """return the realtime current active power consumption
    """
    api = sensecli.api
    click.echo(api.active_power)


@cli.command('active_solar_power')
@click.pass_obj
def active_solar_power(sensecli):
    """return the realtime current active solar power creation
    """
    api = sensecli.api
    click.echo(api.active_solar_power)


@cli.command('active_voltage')
@click.pass_obj
def active_voltage(sensecli):
    """return the realtime current active solar voltage
    """
    api = sensecli.api
    click.echo(api.active_voltage)


@cli.command('active_frequency')
@click.pass_obj
def active_frequency(sensecli):
    """return the realtime current active frequency
    """
    api = sensecli.api
    click.echo(api.active_frequency)



@cli.command('production')
@click.option('--daily', 'period', flag_value='daily', default=True,
              help='Pass --daily to display the daily utilization')
@click.option('--weekly', 'period', flag_value='weekly',
              help='Pass --weekly to display the weekly utilization')
@click.option('--monthly', 'period', flag_value='monthly',
              help='Pass --monthly to display the monthly utilization')
@click.option('--yearly', 'period', flag_value='yearly',
              help='Pass --yearly to display the yearly utilization')
@click.pass_obj
def production(sensecli, period):
    if sensecli.usage:
        raise 'Foo'
    sensecli.production = True


    attr = 'production'
    api = sensecli.api
    value = getattr(api, period + '_' + attr)
    click.echo(value)


@cli.command('usage')
@click.option('--daily', 'period', flag_value='daily', default=True,
              help='Pass --daily to display the daily consumption')
@click.option('--weekly', 'period', flag_value='weekly',
              help='Pass --weekly to display the weekly oconsumption')
@click.option('--monthly', 'period', flag_value='monthly',
              help='Pass --monthly to display the monthly')
@click.option('--yearly', 'period', flag_value='yearly',
              help='Pass --yearly to display the yearly consumption')
@click.pass_obj
def trend(sensecli, period):
    """return the usage trend for the supplied period"""
    if sensecli.usage:
        raise 'Foo'
    sensecli.production = True

    attr = 'usage'
    api = sensecli.api
    value = getattr(api, period + '_' + attr)
    click.echo(value)


if __name__ == "__main__":
    """run the command line interface"""
    cli()


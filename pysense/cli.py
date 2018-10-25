import click

from pysense import __version__
from pysense import api
from pysense import utils


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
    click.echo(__version__)
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS,
             chain=True,
             invoke_without_command=True)
@click.option('--version', '-v',
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True)
@click.pass_context
def cli(ctx):
    ctx.obj = SenseCLI()


@cli.command('config')
@click.option('-e', '--edit',
              is_flag=True,
              help='edit the user configuration file')
@click.pass_obj
def cfg(sensecli, edit=False):
    """Edit the users' configuratoin file"""
    if edit:
        utils.edit_config()


@cli.command('devices')
@click.option('--active/--inactive', default=True, is_flag=True,
              help='Use the active option for only returning devices which '
                   'are currently active.')
@click.pass_obj
def devices(sensecli, active):
    """return the list of active device names or all devices' names"""
    api = sensecli.api
    if active:
        devices = api.active_devices
    else:
        devices = api.devices

    click.echo(devices)


@cli.command('realtime')
@click.option('--power', 'power', flag_value='w', default=True,
              help='energy consumed in watts')
@click.option('--solar', 'solar', flag_value='solar_w',
              help='solar power produced in watts')
@click.option('--frequency', 'frequency', flag_value='hz',
              help='frequency in hz')
@click.option('--voltage', 'voltage', flag_value='voltage',
              help='energy consumed in volts')
@click.pass_obj
def active(sensecli, **kw):
    """obtain the realtime values all active devices energy profile:

       power, frequency, voltage, or production via solar
    """
    api = sensecli.api
    for k,v in kw.items():
        if v is None:
            continue

        ldr = k + ': %s'
        data = api.active(v)
        msg = ldr % data
        if data is not None:
            msg = msg + ' ' + v

        click.echo(msg)


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


@cli.command('devices_map')
@click.pass_obj
def devices_map(sensecli):
    """return device mapping for all for discovered devices

       todo: merge with devices above and it can add an optional argument:
        --mappining

       to return the device mapping of active and all devices.

       XXX a good candidate for cacheing

       todo: Add nice formatter if to display the mapping data

    """
    api = sensecli.api
    click.echo(api.devices_map())


@cli.command('usage_data')
@click.pass_obj
def usage_data(sensecli):
    """return all the usage data
    """
    api = sensecli.api
    click.echo(api.get_all_usage_data())

@cli.command('production')
@click.option('--daily', 'period', flag_value='daily', default=True,
              help='to display the daily utilization')
@click.option('--weekly', 'period', flag_value='weekly',
              help='to display the weekly utilization')
@click.option('--monthly', 'period', flag_value='monthly',
              help='to display the monthly utilization')
@click.option('--yearly', 'period', flag_value='yearly',
              help='to display the yearly utilization')
@click.pass_obj
def production(sensecli, period):
    if sensecli.usage:
        raise click.UsageError('You cannot use the production and usage '
                               'commands at the same time.')
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
def usage(sensecli, period):
    """return the usage trend for the supplied period"""
    if sensecli.production:
        raise click.UsageError('You cannot use the production and usage '
                               'commands at the same time.')
    sensecli.usage = True
    attr = 'usage'
    api = sensecli.api
    value = getattr(api, period + '_' + attr)
    click.echo(value)


if __name__ == "__main__":
    """run the command line interface"""
    cli()


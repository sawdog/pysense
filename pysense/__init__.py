# a package
from pysense.config import yamlcfg
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

if yamlcfg.sentry.enable:
    import sentry_sdk
    sentry_sdk.init(yamlcfg.sentry.dsn,
                    release=yamlcfg.package + '-' + __version__,
                    environment=yamlcfg.environment)



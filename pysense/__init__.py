# a package
__version__ = "0.7.0"
from pysense.config import yamlcfg

if yamlcfg.sentry.enable:
    import sentry_sdk
    sentry_sdk.init(yamlcfg.sentry.dsn)


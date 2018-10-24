import os
import logging

from pysense.config import (yamlcfg,
                            USER_CONFIG_PATH,
                            )


log = logging.getLogger(yamlcfg.logging.name)
if not log.handlers:
    log.setLevel(yamlcfg.logging.level)
    log.addHandler(logging.StreamHandler())
    log.propagate = yamlcfg.logging.propigate



# grab the environment var for the users editor
def get_editor():
    """return the editor command or raise Exception:

       look in the environment for either EDITOR, GIT_EDITOR or SVN_EDITOR

       if not found, raise error EDITOR needs to be set in the env

    """
    found = os.environ.get('EDITOR',
                            os.environ.get('GIT_EDITOR',
                                           os.environ.get('SVN_EDITOR')))
    if not found:
        msg = 'You must set your editor in your environment. Either ' \
              '"EDITOR", "GIT_EDITOR" or "SVN_EDITOR" ' 'must be set.'
        raise Exception(msg)

    return found


def edit_config():
    """open the configuration file for editing"""
    command = get_editor()
    try:
        if not os.path.isfile(USER_CONFIG_PATH):
            open(USER_CONFIG_PATH, 'w+').close()

        edit(USER_CONFIG_PATH, command)
    except OSError as e:
        msg = u"Could not edit configuration: {0}".format(e)
        raise Exception(msg)


def edit(config_dir, command):
    """edit the configuration file"""
    args = str.split(command)
    args.insert(0, args[0])  # for argv[0]
    args += [config_dir]

    return os.execlp(*args)





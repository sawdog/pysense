# pySense 
Sense Energy Monitor API in python


API access to the Sense monitor data. 
Used for pulling data from the Sense energy monitor, and used within other
tools: e.g.

- InfluxDB: for managing your own timeseries monitoring and graphing
- Smartthings: ingtegrate with existing SmartThings IoT devices
- ActiveTiles
- HomeAutomation
 and so on.

This project is written and tested in Python 3.7.0. 

## History

This project is thanks to the work on this [Powershell project on github]:
(https://gist.github.com/mbrownnycnyc/db3209a1045746f5e287ea6b6631e19c)

This is was then ran with by I think the kbickar and then a following fork
by sscottbonline. Since appears to lost it's mainter, I've forked it here.

### Initial Project Contributors
(https://github.com/kbickar)
(https://github.com/sscottbonline/sense)

### Todo

- Continue the development of a fully functional CLI for accessing the APIs:
  - ensure entry_point is functional
- Make configuration more flexible: Adding Confuse as the yaml configuration
  package.
- Add POST/PUT where/if applicable
- Improved error handling
- Adding Sentry configuration


### Install

```
pip install git+https://github.com/sawdog/pysense.git
```


### Setup YAML Config

The configuration uses the standard system config path for the user customized
configuration.

The default search paths for each platform:

#### OS X

> ~/.config/app and ~/Library/Application Support/app

#### Other Unix

> Other Unix: $XDG_CONFIG_HOME/app and ~/.config/app

#### Windows

> %APPDATA%\app where the APPDATA environment variable falls back to 
> %HOME%\AppData\Roaming if undefined

#### Environment Override

You can also add an override configuration directory by setting an environment
variable PYSENSEDIR: export PYSENSEDIR=/opt/app/pysense

#### Example user configuration

You can override any configuration setting you wish, but there are 2 that you
must set. Create a config such as:
vim ~/.config/pysense/config.yaml
sense:
  username: YOUR_SENSE_USERNAME
  password: YOUR_SENSE_PASSWORD

Anything else you wish to override can be added to your user configuraiton
file.

### Example Usage

Once you have your configuration setup, you can begin using the package:

```
sensecli devices --active
```

**or**

```
sensecli devices --inactive
```

See the following command for more help:

```
sensecli --help
```

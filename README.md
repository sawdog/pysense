# pySense 
Sense Energy Monitor API


API access to the Sense monitor data. 
Exploratory work on pulling data from Sense
to be used in other tools - Smartthings, ActiveTiles, etc. 

This is a Python 3.7 implementation based on the work done here in Powershell:
https://gist.github.com/mbrownnycnyc/db3209a1045746f5e287ea6b6631e19c

### Contributors
This is now a fork of (https://github.com/kbickar) a fork (https://github.com/sscottbonline/sense)

### Todo

- Continue the development of a fully functional CLI for accessing the APIs:
  - ensure entry_point is functional
- Make YML path more configurable: check ENV first, then
  path we'll be using in doker, then lastly, the package
- Add POST/PUT where/if applicable
- Improved error handling


### Install

```
pip install git+https://github.com/sawdog/pysense.git
```


### Setup YML Config

### Example Usage:
```
python cli.py devices --active
```

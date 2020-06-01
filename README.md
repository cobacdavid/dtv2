# Under development: DO NOT USE

## Drevo Tyrfing helper functions

Python module to manage key color assignments on the Drevo Tyrfing
v2 keyboard.

## key identifiers and command prefix found at

[https://github.com/dennisblokland/DrevoTyrfing](https://github.com/dennisblokland/DrevoTyrfing)

Nevertheless I noticed RGB preceeds spacer on the DTV2, so that the
script send 31 bytes instead of 32.

## example script

The script `exemples/tyrfingcfg.py` shows how to use the module.

Some config to try:

`python3 tyrfingcfg.py -kbd white -cat letters green mod gold function red edition yellow digits gray arrows cyan -key space blue esc blue enter lightblue`


`python3 tyrfingcfg.py -kbd black -cat letters gray`

`python3 tyrfingcfg.py -kbd black -cat letters gray -key space gray enter gray tab gray`

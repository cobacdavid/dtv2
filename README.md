## Installation

1. Put the ` 99-drevo-tyrfing.rules` in the `/etc/udev/rules.d`
   directory to grant user permissions for to send/write
   informations to the keyboard.

2. `pip3 install dtv2`

3. (optional) Use `tyrfingcfg.py` script (in `exemples` directory)
   to change keys colors (whole keyboard, categories and/or just
   some keys) using svg color names. See examples at the end.

## Drevo Tyrfing helper functions

Python module to manage key color assignments on the Drevo Tyrfing
v2 keyboard.

``` python3
import dtv2
my_kbd = dtv2.dtv2()
my_kbd.change_kbd_color((0, 0, 0))
my_kbd.change_cat_color("arrows", (0, 0x80, 0))
my_kbd.change_key_color('esc', (0xff, 0, 0))
```

## key identifiers and command prefix found at

[https://github.com/dennisblokland/DrevoTyrfing](https://github.com/dennisblokland/DrevoTyrfing)

Nevertheless I noticed RGB preceeds spacer on the DTV2, so that the
script send 31 bytes instead of 32.

[USB hid tables](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf) (for missing french key codes) 

## example script

The script `exemples/tyrfingcfg.py` shows how to use the module.

Some config to try:

`python3 tyrfingcfg.py -kbd white -cat letters green mod gold function red edition yellow digits gray arrows cyan -key space blue esc blue enter lightblue`


`python3 tyrfingcfg.py -kbd black -cat letters gray`

`python3 tyrfingcfg.py -kbd black -cat letters gray -key space gray enter gray tab gray`


## Thanks

[Flozz](https://github.com/flozz)


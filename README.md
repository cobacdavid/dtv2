# Some important notes

This python module handles key coloring of the Drevo Tyrfing v2
keyboard, especially for linux users ; nevertheless it should work
under other platforms.

# Requirements

`dtv2` needs `hidapi` library: `pip3 install hidapi` and `colour`
library: `pip3 install colour`. These dependances are notified in
the **Pypi** `setup` file, so that if you install via `pip`
command, you have nothing to do.

You may need to install `libhidapi-hidraw` dynamic library on your
system. For debian users: `$ sudo apt install libhidapi-hidraw0`

_Note_ python `hidapi` library may confict with python `hid`
library, you may need to uninstall `hid` library.

# Installation

1. Copy the ` 99-drevo-tyrfing.rules` in the `/etc/udev/rules.d/`
   directory to grant user with permissions for to send/write
   informations to the keyboard. Restart or `# udevadm trigger`.

2. `pip3 install dtv2`

# Usage


## With friendly scripts

### dtv2change

Live change and eventually store.


``` bash

$ ./bin/dtv2change -h
usage: dtv2change [-h] [-V] [-r] [-n] [-a] [-kbd KEYBOARD] [-cat CATEGORY [CATEGORY ...]] [-key KEY [KEY ...]]

Change Drevo tyrfing keys colors

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         display version (last modif. date)
  -r, --read            read and apply saved config
  -n, --new             replace or create config file
  -a, --append          change config with args and store changes
  -kbd KEYBOARD, --keyboard KEYBOARD
                        svg_color_name or hex coloror [rgb|hsl]=(.25,1,.5)
  -cat CATEGORY [CATEGORY ...], --category CATEGORY [CATEGORY ...]
                        category_name svg_color_name or hex coloror [rgb|hsl]=(.25,1,.5)
  -key KEY [KEY ...], --key KEY [KEY ...]
                        key_name svg_color_name or hex coloror [rgb|hsl]=(.25,1,.5)



```

### dtv2rdr

Read config JSON files and apply changes.

``` bash

$ dtv2reader -h
usage: dtv2reader [-h] [-V] filename

Change Drevo tyrfing keys colors

positional arguments:
  filename       config_file_name (json)

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  display version (last modif. date)
  
```

## As a module

``` python3
import dtv2

my_kbd = dtv2.dtv2()

# mem_effect: the more you type the more color change
my_kbd.mem_effect((0, 0, 255), color2=(255, 0, 0), brightness=100)

# radar: rays turn around central key (direction: 0 or 1)
my_kbd.radar((0, 0, 255), color2=(255, 0, 0), brightness=100, speed=100, direction=0)

# static: simple static color or if rainbow=True alternate rainbow colors
my_kbd.static((0, 0, 255), brightness=100, speed=100, rainbow=False)

# breath: breath effect
my_kbd.breath((0, 0, 255), brightness=100, speed=100)

# stream: stream effect (direction = 'n' or 's' or 'e' or 'w')
my_kbd.stream((0, 0, 255), color2=(255, 0, 0), brightness=100, speed=100, direction='e', rainbow=False)

# category: change color of a whole category ('letters', 'digits', 'arrows', 'function', 'mod', 'edition')
my_kbd.category('arrows', (255, 0, 0))

# key_set: list of keys and list of colors
my_kbd.key_set( ['esc', 'space'], [(255, 0, 0), (0, 255, 0)] )
my_kbd.key_set( {'esc': (255, 0, 0), 'space': (0, 255, 0)} )
my_kbd.key_set( [('esc', (255, 0, 0)), ('space',(0, 255, 0)] )
my_kbd.key_set( (('esc', (255, 0, 0)), ('space',(0, 255, 0)) )


# key: simple key color change
my_kbd.key('esc', (255, 0, 0))
```

For the moment `rainbow` in `static` mode can be tricky and affect
other effects.

Using simple `key` or `category` modes enter personal mode so exit
all others. It can be boring to affect each key of the keyboard to
the same color so there's this special method in personal mode to
change all the keyboard color (and then you can change categories
colors and finally some individual keys): `kbd`

``` python3
my_kbd.kbd((255, 0, 0))
my_kbd.category('letters', (0, 0, 255))
my_kbd.key('space', (0, 0, 255))
```

## Recap

If you need a monocolor keyboard: `static` or `kbd`.

If you want some effects: `mem_effect`, `radar`, `static` (with
rainbow) `breath` or `stream`.

If you want to personalize categories or some keys: `kbd`,
`category` `key_set` and `key`.

## 
An example usage is provided in the `examples` directory. It uses
[`colour` package](https://github.com/vaab/colour) to allow human
color names instead of hex triplets!


## Examples

In the [examples
section](https://github.com/cobacdavid/dtv2/tree/master/examples),
you'll find a `README` file to use `dtv2change` and `dtv2reader`
scripts.

# First steps and thanks

I did my first steps in this project with a prefix from:

[https://github.com/dennisblokland/DrevoTyrfing](https://github.com/dennisblokland/DrevoTyrfing)

I followed [Flozz](https://github.com/flozz)'s [tutorial (on a mouse)](https://blog.flozz.fr/2016/03/27/steelseries-rival-100-reverse-engineering-dun-peripherique-usb/)

So: I used wireshark to find other command prefixes.

[USB hid tables](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf) (for missing french key codes) 

[Zer0xFF](https://github.com/Zer0xFF) proposed some changes making
individual key color assignments really usable.

[onekk](https://github.com/onekk) added 104-keys keyboard
compatibility, support of `it`alian version and other useful things
on key categories.

# And now?

1. Fix bugs

2. Add functionalities

3. ...

# License

CC-BY-NC-SA

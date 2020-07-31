# Some important notes

This python module handles key coloring of the Drevo Tyrfing v2
keyboard, especially for linux users ; nevertheless it should work
under other platforms.

BUT development is still in progress, the code needs testing (unit,
assertions etc.)

# Installation

1. Copy the ` 99-drevo-tyrfing.rules` in the `/etc/udev/rules.d/`
   directory to grant user with permissions for to send/write
   informations to the keyboard. Restart or `# udevadm trigger`.

2. `pip3 install dtv2`

# Requirements

`dtv2` needs `hidapi` library: `pip3 install hidapi`

# Usage

## Object methods

``` python3
import dtv2

my_kbd = dtv2.dtv2()

# mem_effect: the more you type the more color change
my_kbd.mem_effect((0, 0, 0xff), color2=(0xff, 0, 0), brightness=100)

# radar: rays turn around central key (direction: 0 or 1)
my_kbd.radar((0, 0, 0xff), color2=(0xff, 0, 0), brightness=100, speed=100, direction=0)

# static: simple static color or if rainbow=True alternate rainbow colors
my_kbd.static((0, 0, 0xff), brightness=100, speed=100, rainbow=False)

# breath: breath effect
my_kbd.breath((0, 0, 0xff), brightness=100, speed=100)

# stream: stream effect (direction = 'n' or 's' or 'e' or 'w')
my_kbd.stream((0, 0, 0xff), color2=(0xff, 0, 0), brightness=100, speed=100, direction='e', rainbow=False)

# category: change color of a whole category ('letters', 'digits', 'arrows', 'function', 'mod', 'edition')
my_kbd.category('arrows', (0xff, 0, 0))

# key_set: list of keys and list of colors
my_kbd.key_set(['esc', 'space'], [(0xff, 0, 0), (0, 0xff, 0)])

# key: simple key color change
my_kbd.key('esc', (0xff, 0, 0))
```

Note: colors triplets can be passed usind decimal values.

For the moment `rainbow` in `static` mode can be tricky and affect
other effects.

Using simple `key` or `category` modes enter personal mode so exit
all others. It can be boring to affect each key of the keyboard to
the same color so there's this special method in personal mode to
change all the keyboard color (and then you can change categories
colors and finally some individual keys): `kbd`

``` python3
my_kbd.kbd((0xff, 0, 0))
my_kbd.category('letters', (0, 0, 0xff))
my_kbd.key('space', (0, 0, 0xff))
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
you'll find user scripts that came frontend of this module. Each of
these scripts come with a `README` file.

### dtv2change

Live change and eventually store.

### dtv2rdr

Read config JSON files and apply changes.


# First steps and thanks

I did my first steps in this project with a prefix from:

[https://github.com/dennisblokland/DrevoTyrfing](https://github.com/dennisblokland/DrevoTyrfing)

I followed [Flozz](https://github.com/flozz)'s [tutorial (on a mouse)](https://blog.flozz.fr/2016/03/27/steelseries-rival-100-reverse-engineering-dun-peripherique-usb/)

So: I used wireshark to find other command prefixes.

[USB hid tables](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf) (for missing french key codes) 

Recently [Zer0xFF](https://github.com/Zer0xFF) proposed some
changes making individual key color assignments really usable.

# And now?

1. Fix bugs

2. Add functionalities

3. ...

# License

CC-BY-NC-SA

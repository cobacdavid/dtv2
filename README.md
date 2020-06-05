# complete rework since 0.3

## Installation

1. Copy the ` 99-drevo-tyrfing.rules` in the `/etc/udev/rules.d/`
   directory to grant user with permissions for to send/write
   informations to the keyboard. Restart or `# udevadm trigger`.

2. `pip3 install dtv2`

## Requirements

`dtv2` needs `hidapi` library: `pip3 install hidapi`


## Change colors

Python module to manage key color assignments on the Drevo Tyrfing
v2 keyboard.


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
my_kbd.stream((0, 0, 0xff), color2=(0xff, 0, 0), brightness=100, speed=100, direction='e')
# category: change color of a whole category ('letters', 'digits', 'arrows', 'function', 'mod', 'edition')
my_kbd.category('arrows', (0xff, 0, 0))
# key: simple key color change
my_kbd.key('esc', (0xff, 0, 0))
```


For the moment `rainbow` in `static` mode can be tricky and affect
other effects.

Using simple `key` or `category` modes enter personal mode so exit
all others. It can be boring to affect each key of the keyboard to
the same color so there's this special method in personal mode to
change all the keyboard color (and then you can change categories colors and finally some individual keys): `kbd`

``` python3
my_kbd.kbd((0xff, 0, 0))
my_kbd.category('letters', (0, 0, 0xff))
my_kbd.key('space', (0, 0, 0xff))
```

## Recap

If you need a monocolor keyboard : `static`

If you want some effects : `radar`, `static` (with rainbow)
`breath` or `stream`

If you want to personalize categories or some keys : `kbd`, `category` or `key`.


## key identifiers and command prefix

First steps with a prefix from:

[https://github.com/dennisblokland/DrevoTyrfing](https://github.com/dennisblokland/DrevoTyrfing)

Then: I used wireshark to find other prefixes.

[USB hid tables](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf) (for missing french key codes) 

## colors

Color tuples can be given in decimals, of course.


## And now?

1. Fix bugs

2. Add functionalities

3. Add a utility script handling color names (with `colour` package maybe)

4. ...

## License

CC-BY-NC-SA

## Thanks

[Flozz](https://github.com/flozz)


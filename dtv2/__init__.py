from .dtv2 import *


if __name__ == "__main__":
    drevo = Kbd()
    drevo.change_kbd_color((0, 0, 0))
    drevo.change_cat_color("arrows", (0, 0x80, 0x0))
    drevo.change_cat_color("edition", (0x80, 0, 0x80))
    drevo.change_cat_color("letters", (0xff, 0xff, 0xff))
    drevo.change_cat_color("digits", (0x80, 0, 0))
    drevo.change_cat_color("function", (0x80, 0x80, 0x80))
    drevo.change_cat_color("mod", (0x80, 0x80, 0))

__author__ = "david cobac"
__email__ = "david.cobac @ gmail.com"
__twitter__ = "https://twitter.com/david_cobac"
__github__ = "https://github.com/cobacdavid"
__copyright__ = "Copyright 2020, CC-BY-NC-SA"

import hid
import string
import locale


# keyboard identification
vendor_id = 0x416
product_id = 0xa0f8

# keycodes
keys = {'esc': 0x29, 'f1': 0x3a, 'f2': 0x3b, 'f3': 0x3c, 'f4': 0x3d,
        'f5': 0x3e, 'f6': 0x3f, 'f7': 0x40, 'f8': 0x41, 'f9': 0x42,
        'f10': 0x43, 'f11': 0x44, 'f12': 0x45, 'PS': 0x46, 'SL': 0x47,
        'PB': 0x48,
        #
        '~': 0x35, '1': 0x1e, '2': 0x1f, '3': 0x20, '4': 0x21,
        '5': 0x22, '6': 0x23, '7': 0x24, '8': 0x25, '9': 0x26,
        '0': 0x27, '-': 0x2d, '=': 0x2e, 'BACKS': 0x2a,
        'ins': 0x49, 'home': 0x4a, 'p-up': 0x4b,
        #
        'tab': 0x2b, 'q': 0x14, 'w': 0x1a, 'e': 0x08, 'r': 0x15,
        't': 0x17, 'y': 0x1c, 'u': 0x18, 'i': 0x0c, 'o': 0x12,
        'p': 0x13, '[': 0x2f, ']': 0x30, '\\': 0x31, 'del': 0x4c,
        'end': 0x4d, 'p-down': 0x4e,
        #
        'caps': 0x39, 'a': 0x04, 's': 0x16, 'd': 0x07, 'f': 0x09,
        'g': 0x0a, 'h': 0x0b, 'j': 0x0d, 'k': 0x0e, 'l': 0x0f,
        ';': 0x33, '\'': 0x34, 'enter': 0x28,
        #
        'lshift': 0xe1, 'z': 0x1d, 'x': 0x1b, 'c': 0x06, 'v': 0x19,
        'b': 0x05, 'n': 0x11, 'm': 0x10, ',': 0x36, '.': 0x37,
        '/': 0x38, 'rshift': 0xe5, 'up': 0x52,
        #
        'lctrl': 0xe0, 'win': 0xe3, 'lalt': 0xe2, 'space': 0x2c,
        'ralt': 0xe6, 'FN': 0xed, 'compo': 0x65, 'rctrl': 0xe4,
        'left': 0x50, 'down': 0x51, 'right': 0x4f}

# keys groups
category_keys = {'letters': string.ascii_lowercase,
                 'digits': string.digits,
                 'mod': ['esc', 'lshift', 'rshift', 'lctrl',
                         'win', 'lalt', 'ralt', 'rctrl'],
                 'arrows': ['left', 'right', 'down', 'up'],
                 'function': [f'f{i}' for i in range(1, 1 + 12)],
                 'edition': ['ins', 'home', 'p-up',
                             'del', 'end', 'p-down']}
# fr locale 
if 'fr' in locale.setlocale(locale.LC_ALL, ''):
    frkeys = {'²': 0x35,
              ')': 0x2d,
              '^': 0x2f,
              '$': 0x30,
              'm': 0x33,
              'ù': 0x34,
              '*': 0x32,
              '<': 0x64,
              ',': 0x10,
              ';': 0x36,
              ':': 0x37,
              '!': 0x38}
    keys.update(frkeys)

# commands prefixes
coms = {"mem_effect":
        {"prefix": [0x6, 0xbe, 0x15, 0x0, 0x1, 0x1, 0xd]},
        "radar":
        {"prefix": [0x6, 0xbe, 0x15, 0x0, 0x1, 0x1, 0x10]},
        "static":
        {"prefix": [0x6, 0xbe, 0x15, 0x0, 0x1, 0x1, 0x1]},
        "breath":
        {"prefix": [0x6, 0xbe, 0x15, 0x0, 0x1, 0x1, 0x2]},
        "stream":
        {"prefix": [0x6, 0xbe, 0x15, 0x0, 0x1, 0x1, 0x3]},
        "indiv":
        {"avantp": [0x6, 0xbe, 0x15, 0x0, 0x1, 0x1, 0xf],
         "prefix": [0x6, 0xbe, 0x19, 0x0, 0x1, 0x1, 0xe],
         "apresp": [0x6, 0xbe, 0x15, 0x0, 0x2, 0x1, 0x1]}}


def split_list(L):
    """Split a list in groups of (max) 5 elements

    For individual assignments, a packet sent to the device can
    contain max 5 keys config

    """
    return [L[i:i + 5] for i in range(0, len(L), 5)]


class dtv2:
    #
    def __init__(self):
        self.__init_trame()
        self.iface = None
        self.path = None
        self.dev = None

    def __init_trame(self):
        self.trame = [0] * 32

    def __device_accessible(self):
        """" explicit naming

        :rtype: boolean

        """

        interfaces = hid.enumerate(vendor_id, product_id)
        # si présent mais pas accessible (cf. /etc/udev/rules.d)
        # cette chaîne est vide
        for interface in interfaces:
            if interface['interface_number'] == 1 and interface['usage'] == 0:
                self.iface = interface
                return True
        return False

    def __ouverture_device(self):
        """explicit naming

        """

        if self.__device_accessible():
            self.dev = hid.device()
            try:
                self.dev.open_path(self.iface['path'])
            except:
                raise Exception("problème d'accès")

    def __ecriture_device(self):
        """write packet to the device

        """

        a = self.dev.write(self.trame)
        self.__init_trame()
        return a

    def __trame_couleur_touche(self, id_key, couleur_RGB):
        """assign a key color to a single key

        id_key: key id as in 'keys' dictionary
        couleur_RGB: color tuple (or list) (3 integers required)

        """

        self.trame[:7] = coms["indiv"]["prefix"]
        self.trame[7] = keys[id_key]
        self.trame[12:15] = [*couleur_RGB]

    def __trame_couleur_plusieurs_touches(self, id_keys, couleurs_RGB):
        """assign color to several keys

        id_keys: list of key ids as in 'keys' dictionary

        couleurs_RGB: list of color tuples (or lists) (3 integers required)

        IMPORTANT: lists length <=5 so you eventually have to use
        'split_liste' BEFORE

        """

        if len(id_keys) != len(couleurs_RGB):
            return
        else:
            hexa_keys = [keys[i] for i in id_keys]
            colors = []
            for c in couleurs_RGB:
                colors += [*c, 0]
            self.trame[:7] = coms["indiv"]["prefix"]
            self.trame[7:7 + len(id_keys)] = hexa_keys
            self.trame[12:12 + 4 * len(id_keys)] = colors

    def __construction_trames(self, liste_touches, couleur_RGB):
        """build a list of packets to send to the device with 1 color

        """

        trames = []
        for liste_cinq_touches in split_list(liste_touches):
            # met à jour self.trame
            self.__trame_couleur_plusieurs_touches(
                liste_cinq_touches,
                [couleur_RGB] * len(liste_cinq_touches)
            )
            trames.append(self.trame[:])
        return trames

    def __applique_trames(self, liste_trames, indiv=False):
        """heart of the program. Apply previously built packets to the
device.

        """

        self.__ouverture_device()
        for i in range(len(liste_trames)):
            trame = liste_trames[i]
            self.trame = trame
            if indiv and i == 0:
                self.trame[15] = 0x53
                self.trame[31] = 0x65
            a = self.__ecriture_device()
            if a == -1:
                pass
                #  raise Exception('erreur...')
        self.dev.close()

    def mem_effect(self, color1,
                   color2=(0xff, 0, 0),
                   brightness=100):
        """Mem animation: the more you type the more second color appears

        """

        # keys est un dict
        # keys.keys() est un dict_keys
        # list(keys.keys()) est une liste
        # trames = self.__construction_trames(list(keys.keys()),
        #                                     couleur_RGB)
        self.trame[:7] = coms["mem_effect"]["prefix"]
        self.trame[8] = int(round(brightness / 100 * 6))
        self.trame[12:15] = [*color1]
        self.trame[16:19] = [*color2]
        #
        self.__applique_trames([self.trame])

    def radar(self, color1,
              color2=(0xff, 0, 0),
              brightness=100,
              speed=100,
              direction=0):
        """Radar like animation

        """

        self.__execute__command("radar", color1,
                                color2=color2,
                                brightness=brightness,
                                speed=speed,
                                direction=direction)

    def static(self, color1,
               brightness=100,
               speed=100,
               rainbow=False):
        """Monocolor keyboard

        """

        self.__execute__command("static", color1,
                                brightness=brightness,
                                speed=speed,
                                rainbow=rainbow)

    def breath(self, color1,
               color2=(0xff, 0, 0),
               brightness=100,
               speed=100):
        """Breathe like animation

        """

        self.__execute__command("breath", color1,
                                color2=color2,
                                brightness=brightness,
                                speed=speed)

    def stream(self, color1,
               color2=(0xff, 0, 0),
               brightness=100,
               speed=100,
               direction="e",
               rainbow=False):
        """Stream like animation

        """

        directions = {'e': 0, 'w': 1, 's': 2, 'n': 3}
        self.__execute__command("stream", color1,
                                color2=color2,
                                brightness=brightness,
                                speed=speed,
                                direction=directions[direction],
                                rainbow=rainbow)

    def __execute__command(self, commande, color1,
                           color2=(0xff, 0, 0),
                           brightness=100,
                           speed=100,
                           rainbow=False,
                           direction=0):
        """Build packet for animations and ask for applying

        """

        self.trame[:7] = coms[commande]["prefix"]
        self.trame[7] = int(round(speed / 100 * 9))
        self.trame[8] = int(round(brightness / 100 * 6))
        self.trame[9] = direction
        self.trame[12:15] = [*color1]
        self.trame[15] = 1 if rainbow else 0
        self.trame[16:19] = [*color2]
        #
        self.__applique_trames([self.trame])

    def key(self, id_key, couleur_RGB):
        """Individual key color assignment

        """

        self.__ouverture_device()
        self.__trame_couleur_touche(id_key, couleur_RGB)
        if self.__ecriture_device() == -1:
            self.dev.close()
            raise Exception('erreur...')
        self.dev.close()

    def key_set(self, id_keys, RGB_colors):
        """Multi-keys assignments

        """

        trames = []
        for keys, colors in zip(split_list(id_keys), split_list(RGB_colors)):
            self.__trame_couleur_plusieurs_touches(keys, colors)
            trames.append(self.trame[:])

        self.__applique_trames(trames)

    def category(self, categorie, couleur_RGB):
        """Category keys color assignment

        :categorie: is a key of the 'category_keys' dictionary

        """

        cat = category_keys[categorie]
        trames = self.__construction_trames(cat, couleur_RGB)
        self.__applique_trames(trames)

    def kbd(self, couleur_RGB):
        """Whole keyboard in a single color

        Notes: using wireshark, I saw a packet sent before and
        another sent after... so I produce the same packets.
        Some verifications need to be done in this section.

        Difference with 'static' is that it's not a
        prestored-effect in the device. This method assigns the
        same color to keys. It's a user config.

        """

        trames = self.__construction_trames(list(keys.keys()),
                                            couleur_RGB)
        #
        trame_avant = [0x0] * 32
        trame_avant[:7] = coms["indiv"]["avantp"]
        trame_avant[8] = 0x6  # luminosité
        trame_avant[12] = 0xff
        self.__applique_trames(trame_avant)
        #
        self.__applique_trames(trames, indiv=True)
        #
        trame_apres = [0] * 32
        trame_apres[:7] = coms["indiv"]["apresp"]
        trame_apres[7] = 0x5
        trame_apres[8] = 0x9
        trame_apres[12] = 0xff
        trame_apres[16] = 0xff
        self.__applique_trames(trame_apres)

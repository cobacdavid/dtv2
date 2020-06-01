import hid
import string
import locale


class Kbd:
    #
    vendor_id = 0x416
    product_id = 0xa0f8
    #
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
               'lctrl': 0xe0, 'win': 0xe3, 'alt': 0xe2, 'space': 0x2c,
               'altgr': 0xe6, 'FN': 0xed, 'compo': 0x65, 'rctrl': 0xe4,
               'left': 0x50, 'down': 0x51, 'right': 0x4f}
    #
    category_keys = {'letters': string.ascii_lowercase,
                     'digits': string.digits,
                     'mod': ['esc', 'lshift', 'rshift', 'lctrl',
                             'win', 'alt', 'altgr', 'rctrl'],
                     'arrows': ['left', 'right', 'down', 'up'],
                     'function': [f'f{i}' for i in range(1, 1 + 12)],
                     'edition': ['ins', 'home', 'p-up',
                                 'del', 'end', 'p-down']}
    #
    if 'fr' in locale.setlocale(locale.LC_ALL, ''):
        frkeys = {'²': 0x35,
                  ')': 0x2d,
                  '^': 0x2f,
                  '$': 0x30,
                  'm': 0x33,
                  'ù': 0x34,
                  # '*': 0x35,
                  # '<': ????,
                  ',': 0x10,
                  ';': 0x36,
                  ':': 0x37,
                  '!': 0x38}
        keys.update(frkeys)

    def __init__(self):
        # https://github.com/dennisblokland/DrevoTyrfing
        self.com_prefixe = [0x6, 0xbe, 0x19, 0x0, 0x1, 0x1, 0xe]
        #
        self.trame = []
        self.iface = None
        self.path = None
        self.dev = None

    def __device_accessible(self):
        """" nom explicite
        retourne un booléen
        """

        interfaces = hid.enumerate(Kbd.vendor_id, Kbd.product_id)
        # si présent mais pas accessible (cf. /etc/udev/rules.d)
        # cette chaîne est vide
        if interfaces[1]['product_string'] == '':
            return False
        else:
            self.iface = interfaces[1]
            return True

    def __ouverture_device(self):
        """ nom explicite
        """

        if self.__device_accessible():
            self.dev = hid.device()
            try:
                self.dev.open_path(self.iface['path'])
            except:
                raise Exception("problème d'accès")

    def __trame_couleur_touche(self, id_key, couleur_RGB):
        """ attribue une couleur à UNE touche particulière
        id_touche: identifiant de la touche tel que sur le dictionnaire (clé)
        couleur_hexa_RGB: couleur sous forme d'un tuple/liste (RGB) d'entiers
        """

        key = [Kbd.keys[id_key]] + [0] * 4
        couleurs = [*couleur_RGB] + [0xf]
        couleurs += [0, 0, 0, 0xff] * 4
        trame = self.com_prefixe + key + couleurs
        if len(trame) == 32:
            self.trame = trame
        else:
            self.trame = None

    def __ecriture_device(self):
        """ envoie la trame construite au device (clavier)
        """

        if not self.trame:
            return -1
        else:
            retour = self.dev.write(self.trame)
            self.dev.close()
            return retour

    def change_key_color(self, id_key, couleur_RGB):
        """ demande l'application d'un changement sur une touche
        """

        self.__ouverture_device()
        self.__trame_couleur_touche(id_key, couleur_RGB)
        if self.__ecriture_device() == -1:
            raise Exception('erreur...')

    def change_cat_color(self, categorie, couleur_RGB):
        """demande l'application d'un changement sur une catégorie de
        touches
        Les catégories possibles :
        letters
        digits
        mod
        arrows
        function
        edition
        """

        cat = self.category_keys[categorie]
        for id_key in cat:
            self.__ouverture_device()
            self.__trame_couleur_touche(id_key, couleur_RGB)
            if self.__ecriture_device() == -1:
                raise Exception('erreur...')

    def change_kbd_color(self, couleur_RGB):
        """demande l'application d'un changement sur l'ensemble des touches
        """

        for id_key in Kbd.keys:
            self.__ouverture_device()
            self.__trame_couleur_touche(id_key, couleur_RGB)
            if self.__ecriture_device() == -1:
                raise Exception('erreur...')

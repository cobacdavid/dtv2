import hid
import string
import locale

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
        'lctrl': 0xe0, 'win': 0xe3, 'lalt': 0xe2, 'space': 0x2c,
        'ralt': 0xe6, 'FN': 0xed, 'compo': 0x65, 'rctrl': 0xe4,
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
              '*': 0x32,
              '<': 0x64,
              ',': 0x10,
              ';': 0x36,
              ':': 0x37,
              '!': 0x38}
    keys.update(frkeys)

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
        "indiv":  # https://github.com/dennisblokland/DrevoTyrfing
        {"prefix": [0x6, 0xbe, 0x19, 0x0, 0x1, 0x1, 0xe]}}


def split_list(L):
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
        """" nom explicite
        retourne un booléen
        """

        interfaces = hid.enumerate(vendor_id, product_id)
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

    def __ecriture_device(self):
        """ envoie la trame construite au device (clavier)
        """

        a = self.dev.write(self.trame)
        self.__init_trame()
        return a

    def __trame_couleur_touche(self, id_key, couleur_RGB):
        """ attribue une couleur à UNE touche particulière
        id_key: identifiant de la touche tel que sur le dictionnaire (clé)
        couleur_RGB: couleur sous forme d'un tuple/liste (RGB) d'entiers
        """

        self.trame[:7] = coms["indiv"]["prefix"]
        self.trame[7] = keys[id_key]
        self.trame[12:15] = [*couleur_RGB]

    def __trame_couleur_plusieurs_touches(self, id_keys, couleurs_RGB):
        """attribue les couleurs à plusieurs touches

        id_keys: liste d'identifiants des touches tels que sur le
        dictionnaire (clé)

        couleurs_RGB: liste de couleurs sous forme de tuples/listes
        (RGB) d'entiers

        IMPORTANT : la longeur des lises doit être inférieur ou égal à 5
        donc utilisation de split_liste AVANT
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
            self.trame[12:12 + 4*len(id_keys)] = colors

    def __construction_trames(self, liste_touches, couleur_RGB):
        """ construit toutes les trames nécessaire par groupe de 5
        1 seule couleur !
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

    def __applique_trames(self, liste_trames):
        """
        """

        for trame in liste_trames:
            self.__ouverture_device()
            self.trame = trame
            a = self.__ecriture_device()
            self.dev.close()
            if a == -1:
                raise Exception('erreur...')

    def mem_effect(self, color1,
                   color2=(0xff, 0, 0),
                   brightness=100):
        """demande l'application d'un changement sur l'ensemble des touches
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
        self.__execute__command("radar", color1,
                                color2=color2,
                                brightness=brightness,
                                speed=speed,
                                direction=direction)

    def static(self, color1,
               brightness=100,
               speed=100,
               rainbow=False):
        self.__execute__command("static", color1,
                                brightness=brightness,
                                speed=speed,
                                rainbow=rainbow)

    def breath(self, color1,
               color2=(0xff, 0, 0),
               brightness=100,
               speed=100):
        self.__execute__command("breath", color1,
                                color2=color2,
                                brightness=brightness,
                                speed=speed)

    def stream(self, color1,
               color2=(0xff, 0, 0),
               brightness=100,
               speed=100,
               direction="e"):
        directions = {'e': 0, 'w': 1, 's': 2, 'n': 3}
        self.__execute__command("stream", color1,
                                color2=color2,
                                brightness=brightness,
                                speed=speed,
                                direction=directions[direction])

    def __execute__command(self, commande, color1,
                           color2=(0xff, 0, 0),
                           brightness=100,
                           speed=100,
                           rainbow=False,
                           direction=0):

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
        """ demande l'application d'un changement sur une touche
        """

        self.__ouverture_device()
        self.__trame_couleur_touche(id_key, couleur_RGB)
        if self.__ecriture_device() == -1:
            self.dev.close()
            raise Exception('erreur...')
        self.dev.close()

    def category(self, categorie, couleur_RGB):
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

        cat = category_keys[categorie]
        trames = self.__construction_trames(cat, couleur_RGB)
        self.__applique_trames(trames)

    def kbd(self, couleur_RGB):
        """
        """

        trames = self.__construction_trames(list(keys.keys()),
                                            couleur_RGB)
        self.__applique_trames(trames)

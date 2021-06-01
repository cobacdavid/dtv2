__author__ = "david cobac"
__contributors_page__ = "https://github.com/cobacdavid/dtv2/graphs/contributors"
__email__ = "david.cobac @ gmail.com"
__twitter__ = "https://twitter.com/david_cobac"
__github__ = "https://github.com/cobacdavid"
__copyright__ = "Copyright 2020-2021, CC-BY-NC-SA"

import hid
import string
import locale
import json
import importlib.resources


# keyboard identification
vendor_id = 0x416
product_id = 0xa0f8


def split_list(L):
    """Split a list in groups of (max) 5 elements

    For individual assignments, a packet sent to the device can
    contain max 5 keys config

    """

    return [L[i:i + 5] for i in range(0, len(L), 5)]


def get_key_locale_name(hid_id, keys_dict):
    """ returns dictionary key from its value

    hid_id: integer representing hid id of a key
    keys_dict: a flat dictionary of locale identified keys
    """

    for name, id_code in keys_dict.items():
        if id_code == hid_id:
            return name


class dtv2:
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
            {"beforep": [0x6, 0xbe, 0x15, 0x0, 0x1, 0x1, 0xf],
             "prefix": [0x6, 0xbe, 0x19, 0x0, 0x1, 0x1, 0xe],
             "afterp": [0x6, 0xbe, 0x15, 0x0, 0x2, 0x1, 0x1]}
            }
    #
    def __init__(self, lcl=None):
        self.__init_packet()
        self.iface = None
        self.path = None
        self.dev = None
        self._keys = {}
        self._category_keys = {}
        if lcl is None:
            lcl = locale.setlocale(locale.LC_ALL, '')[:2]
        self._local = lcl
        self.__assign_keys()

    def __assign_keys(self):
        lang_file = f"{self._local}.json"
        try:
            lang_text = importlib.resources.read_text(__package__, lang_file)
        except FileNotFoundError:
            print(f"{self._local}.json not found.\nLoading en.json")
            lang_file = "en.json"
            lang_text = importlib.resources.read_text(__package__, lang_file)
        #
        json_keys = json.loads(lang_text)
            # parse lang_file row (of keyboard) by row 
            # and convert values: str -> int
        self._category_keys = {}
        self._keys = {}
        for row in json_keys:
            self._category_keys[row] = []
            for key in json_keys[row]:
                self._keys[key] = int(json_keys[row][key], 16)
                self._category_keys[row].append(key)

        # keys groups
        self._category_keys.update({
            # common letters
            'letters': string.ascii_lowercase,
            # digits
            'digits': string.digits,
            # mod keys
            'mod': ['esc', 'lshift', 'rshift', 'lctrl', 'win', 'lalt', 'ralt', 'rctrl'],
            # arrow pad
            'arrow': ['left', 'right', 'down', 'up'],
            # function aka row K
            'function': ['esc'] + [f'f{i}' for i in range(1, 1 + 12)],
            'other': ['PS', 'SL', 'PB'],
            # edition keys aka control
            'edition': ['ins', 'home', 'p-up', 'del', 'end', 'p-down'],
            # alphanumeric: main part of the keyboard
            'alphanumeric': list(string.ascii_lowercase) + list(string.digits) +\
            ['lshift', 'rshift', 'lctrl', 'win', 'lalt', 'ralt', 'rctrl'] +\
            # and now row by row:
            [get_key_locale_name(0x35, self._keys), get_key_locale_name(0x2d, self._keys),
             get_key_locale_name(0x2e, self._keys), 'BACKS',
             'tab', get_key_locale_name(0x2f, self._keys), get_key_locale_name(0x30, self._keys),
             'caps', get_key_locale_name(0x34, self._keys), get_key_locale_name(0x32, self._keys),
             'enter',
             get_key_locale_name(0x64, self._keys), get_key_locale_name(0x10, self._keys),
             get_key_locale_name(0x36, self._keys), get_key_locale_name(0x37, self._keys),
             get_key_locale_name(0x38, self._keys),
             'space', 'FN', 'compo'],
            # keypad digits
            'kpdigits': [f'kp{i}' for i in range(10)],
            'kpsymbols': ['kpnlk', 'kpdiv', 'kpmul', 'kpsub', 'kpadd', 'kpdot', 'kpent']
        })
        # create extended numeric keypad category
        self._category_keys['kpnum'] = self._category_keys['kpdigits'] + ['kpdot']
        self._category_keys['keypad'] =  self._category_keys['kpnum'] +\
            self._category_keys['kpsymbols']
        # not a deepcopy: control and edition point to the same list
        self._category_keys['numpad'] = self._category_keys['keypad']
        # not a deepcopy: control and edition point to the same list
        self._category_keys['control'] = self._category_keys['edition']
        # backward compatibility
        self._category_keys['arrows'] = self._category_keys['arrow']

    @property
    def local(self):
        """ getter for localisation string

        """
        
        return self._local

    @local.setter
    def local(self, lcl=None):
        """ setter for localisation string

        """
        
        if lcl is None:
            self._local = locale.setlocale(locale.LC_ALL, '')[:2]
        else:
            self._local = lcl
        self.__assign_keys()

    def __init_packet(self):
        self.packet = [0] * 32

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

    def __open_device(self):
        """explicit naming

        """

        if self.__device_accessible():
            self.dev = hid.device()
            try:
                self.dev.open_path(self.iface['path'])
            except:
                raise Exception("Impossible to reach device... unplug and plug your keyboard.")

    def __write_device(self):
        """write packet to the device
        reset packet container

        """

        a = self.dev.write(self.packet)
        self.__init_packet()
        return a

    def __packet_key_color(self, id_key, rgb_color):
        """assign a key color to a single key

        id_key: key id as in 'keys' dictionary
        rgb_color: color tuple (or list) (3 integers required)

        """

        self.packet[:7] = dtv2.coms["indiv"]["prefix"]
        self.packet[7] = self._keys[id_key]
        self.packet[12:15] = [*rgb_color]

    def __packet_keys_and_colors(self, id_keys, rgb_colors):
        """assign color to several keys

        id_keys: list of key ids as in 'keys' dictionary

        rgb_colors: list of color tuples (or lists) (3 integers required)

        IMPORTANT: lists length <=5 so you eventually have to use
        'split_list' BEFORE

        """

        if len(id_keys) != len(rgb_colors):
            return
        else:
            hexa_keys = [self._keys[i] for i in id_keys]
            colors = []
            self.__init_packet()
            #
            for c in rgb_colors:
                colors += [*c, 0]
                self.packet[:7] = dtv2.coms["indiv"]["prefix"]
                self.packet[7:7 + len(id_keys)] = hexa_keys
                self.packet[12:12 + 4 * len(id_keys)] = colors

    def __build_packets(self, keys_list, rgb_color):
        """build a list of packets to send to the device with 1 color

        """

        packets = []
        for five_keys_list in split_list(keys_list):
            # met à jour self.packet
            self.__packet_keys_and_colors(
                five_keys_list,
                [rgb_color] * len(five_keys_list)
            )
            packets.append(self.packet[:])
        return packets

    def __apply_packets(self, liste_packets, indiv=False):
        """heart of the program. Apply previously built packets to the
        device.

        """

        for i in range(len(liste_packets)):
            packet = liste_packets[i]
            self.packet = packet
            if indiv and i == 0:
                self.packet[15] = 0x53
                self.packet[31] = 0x65
            a = self.__write_device()
            if a == -1:
                pass
                # raise Exception('erreur...')

    def mem_effect(self, color1,
                   color2=(0xff, 0, 0),
                   brightness=100):
        """Mem animation: the more you type the more second color appears

        """

        # keys est un dict
        # keys.keys() est un dict_keys
        # list(keys.keys()) est une liste
        # packets = self.__build_packets(list(keys.keys()),
        #                                     rgb_color)
        self.packet[:7] = dtv2.coms["mem_effect"]["prefix"]
        self.packet[8] = int(round(brightness / 100 * 6))
        self.packet[12:15] = [*color1]
        self.packet[16:19] = [*color2]
        #
        self.__open_device()
        self.__apply_packets([self.packet])
        self.dev.close()

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

    def __execute__command(self, command, color1,
                           color2=(0xff, 0, 0),
                           brightness=100,
                           speed=100,
                           rainbow=False,
                           direction=0):
        """Build packet for animations and ask for applying

        """

        self.packet[:7] = dtv2.coms[command]["prefix"]
        self.packet[7] = int(round(speed / 100 * 9))
        self.packet[8] = int(round(brightness / 100 * 6))
        self.packet[9] = direction
        self.packet[12:15] = [*color1]
        self.packet[15] = 1 if rainbow else 0
        self.packet[16:19] = [*color2]
        #
        self.__open_device()
        self.__apply_packets([self.packet])
        self.dev.close()

    def key(self, id_key, rgb_color):
        """Individual key color assignment

        """

        self.__open_device()
        self.__packet_key_color(id_key, rgb_color)
        if self.__write_device() == -1:
            self.dev.close()
            raise Exception('Oups error...')
        self.dev.close()

    def __key_set(self, id_keys, rgb_colors):
        """Multi-keys assignments

        """

        packets = []
        for keys, colors in zip(split_list(id_keys), split_list(rgb_colors)):
            self.__packet_keys_and_colors(keys, colors)
            packets.append(self.packet[:])
        #
        self.__open_device()
        self.__apply_packets(packets)
        self.dev.close()

    def key_set(self, *args):
        """Multi-keys assignments with differents entry types

        Usage examples:
        key_set( ['esc', 'space'], [(0xff, 0, 0), (0, 0xff, 0)] )
        key_set( {'esc': (0xff, 0, 0), 'space': (0, 0xff, 0)} )
        key_set( [('esc', (0xff, 0, 0)), ('space', (0, 0xff, 0)] )
        key_set( (('esc', (0xff, 0, 0)), ('space', (0, 0xff, 0)) )

        """

        if len(args) == 2:
            id_keys, rgb_colors = args
        elif len(args) == 1:
            args = args[0]
            if type(args) == dict:
                id_keys = list(args.keys())
                rgb_colors = list(args.values())
            if (type(args) == list
                # or type(args) == set
                or type(args) == tuple):
                id_keys, rgb_colors = [], []
                for key, color in args:
                    id_keys.append(key)
                    rgb_colors.append(color)
        else:
            return
        #
        self.__key_set(id_keys, rgb_colors)

    def category(self, category, rgb_color):
        """Category keys color assignment

        :category: is a key of the 'category_keys' dictionary

        """

        cat = self._category_keys[category]
        packets = self.__build_packets(cat, rgb_color)
        #
        self.__open_device()
        self.__apply_packets(packets)
        self.dev.close()

    def kbd(self, rgb_color):
        """Whole keyboard in a single color

        Notes: using wireshark, I saw a packet sent before and
        another sent after... so I produce the same packets.
        Some verifications need to be done in this section.

        Difference with 'static' is that it's not a
        prestored-effect in the device. This method assigns the
        same color to keys. It's a user config.

        """

        packets = self.__build_packets(list(self._keys.keys()),
                                       rgb_color)
        #
        self.__open_device()
        #
        self.__init_packet()
        self.packet[:7] = dtv2.coms["indiv"]["beforep"]
        self.packet[8] = 0x6  # luminosité
        self.packet[12] = 0xff
        self.__write_device()
        #
        self.__apply_packets(packets, indiv=True)
        #
        self.__init_packet()
        self.packet[:7] = dtv2.coms["indiv"]["afterp"]
        self.packet[7] = 0x5
        self.packet[8] = 0x9
        self.packet[12] = 0xff
        self.packet[16] = 0xff
        self.__write_device()
        #
        self.dev.close()

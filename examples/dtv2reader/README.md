# Installation

`dtv2reader` is automatically installed with `dtv2` installation.

# What it does

As its name suggests, it reads config file to change colours of
`Drevo Tyrfing v2` keys.

# Config file format

Config files are `json` formatted.

Here is an example (`config_awesome.json` file):

``` javascript
{"kbd": "gray",
 "cat": {"letters": "aquamarine"},
 "key": {"PS": "black",
         "SL": "black",
         "PB": "black",
         "²": "black",
         "ins": "black",
         "win": "red",
         "right": "red",
         "left": "red"}
}
```

Key' dictionary may be `kbd` (whole keyboeard), `cat` (category) or
`key` (individual key).

`cat` is a dictionary, possible keys are:

```
'row K', 'row E', 'row D', 'row C', 'row B', 'row A',
'letters', 'digits', 'mod', 'arrow', 'function', 'other',
'edition', 'alphanumeric', 'kpdigits', 'kpsymbols', 'kpnum',
'keypad', 'numpad', 'control', 'arrows'

```

`key` is a dicitonary, possible keys are key names.

# Usage

``` bash
$ dtv2reader /path/to/your/config/file.json
```

# Colors

Color are given with their SVG names (e.g. `blue`) or hex3 version if possible (e.g. `#f00`) or hex6 version (e.g. `#ff0000`) or with floats in [0;1[ either in rgb (e.g. `rgb=(1,0,0)`) or with hsl(e.g. `hsl=(.94,1,.5)`) . Made available thanks to [`colour` package](https://github.com/vaab/colour)

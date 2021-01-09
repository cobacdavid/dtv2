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

`cat` is a dictionary, possible keys are `letters`, `digits`,
`mod`, `arrows`, `function` and `edition`.

`key` is a dicitonary, possible keys are key names.

# Usage

``` bash
$ dtv2reader /path/to/your/config/file.json
```

# Colors

Color names are SVG ones. Made available thanks to [`colour` package](https://github.com/vaab/colour)


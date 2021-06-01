# Installation

`dtv2change` is automatically installed with `dtv2` installation.


# What it does

As its name suggests, it allows live change of key colors of `Drevo
Tyrfing v2` keyboard.

# Config file

It writes `$HOME/.dtv2change` file to read and save your current
config. This is a JSON formatted file (possibly usable with
`dvt2reader`).

# Usage

To create or empty the config file: `$ dtv2change -n`

To read the saved config file: `$ dtv2change -r`

To change -without saving- whole keyboard: `$ dtv2change -kbd red`

To change -without saving- a category: `$ dtv2change -cat letters yellow`

Possible categories are:

```
'row K', 'row E', 'row D', 'row C', 'row B', 'row A',
'letters', 'digits', 'mod', 'arrow', 'function', 'other',
'edition', 'alphanumeric', 'kpdigits', 'kpsymbols', 'kpnum',
'keypad', 'numpad', 'control', 'arrows'

```

To change -without saving- a key: `$ dtv2change -key space blue`

To change AND append changes to saved config use `-chg` option with previous options, e.g.:

`$ dtv2change -chg -kbd tomato -cat digits cyan -key esc white`

Then `$HOME/.dtv2change` contains:

``` javascript
{"kbd": "tomato", "cat": {"digits": "cyan"}, "key": {"esc": "white"}}
```

To append a new color key to this, just type:

`$ dtv2change -chg -key space white`

and now `$HOME/.dtv2change` contains:

``` javascript
{"kbd": "tomato", "cat": {"digits": "cyan"}, "key": {"esc": "white", "space": "white"}}
```

# Issues?

## After appending to existing config, my keyboard doesn't show correct colors.

Try:  `$ dtv2change -r`

## Where are animations?

Though partially implemented in the package, for the moment no CLI
script has been developed to take advantage of these functionnalities.

# Colors

Color are given with their SVG names (e.g. `blue`) or hex3 version if possible (e.g. `#f00`) or hex6 version (e.g. `#ff0000`) or with floats in [0;1[ either in rgb (e.g. `rgb=(1,0,0)`) or with hsl(e.g. `hsl=(.94,1,.5)`) . Made available thanks to [`colour` package](https://github.com/vaab/colour)


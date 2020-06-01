import argparse
import dtv2
import colour

parseur_args = argparse.ArgumentParser(
    description="""Change Drevo tyrfing keys colors""")
parseur_args.add_argument('-kbd', '--keyboard', help='svg color name')
parseur_args.add_argument('-cat', '--category',
                          nargs='+',
                          help='category_name svg_color_name')
parseur_args.add_argument('-key', '--key',
                          nargs='+',
                          help='key_name svg_color_name')

args = parseur_args.parse_args()

clavier = dtv2.dtv2()

if args.keyboard and args.keyboard not in colour.COLOR_NAME_TO_RGB:
    print("""This color does not exist!
Please see https://www.w3.org/TR/css-color-3/#svg-color""")
elif args.keyboard:
    couleur = colour.COLOR_NAME_TO_RGB[args.keyboard]
    clavier.change_kbd_color(couleur)
#
if args.category and len(args.category) < 2:
    print("""Need a category name AND a color name""")
elif args.category and len(args.category) % 2 == 0:
    for k, v in {args.category[i]: args.category[i+1]
                 for i in range(0, len(args.category), 2)}.items():
        if k not in clavier.category_keys:
            print("""This category does not exist!
Available categories are f{liste_categories}""")
            continue
        if v not in colour.COLOR_NAME_TO_RGB:
            print("""This color does not exist!
Please see https://www.w3.org/TR/css-color-3/#svg-color""")
            continue
        clavier.change_cat_color(k, colour.COLOR_NAME_TO_RGB[v])
#
if args.key and len(args.key) < 2:
    print("""Need a key name AND a color name""")
elif args.key and len(args.key) % 2 == 0:
    for k, v in {args.key[i]: args.key[i+1]
                 for i in range(0, len(args.key), 2)}.items():
        if k not in clavier.keys:
            print("""This key does not exist!
Look at your keyboard!""")
            continue
        if v not in colour.COLOR_NAME_TO_RGB:
            print("""This color does not exist!
Please see https://www.w3.org/TR/css-color-3/#svg-color""")
            continue
        clavier.change_key_color(k, colour.COLOR_NAME_TO_RGB[v])

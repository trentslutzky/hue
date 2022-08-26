from pretty import print_colors
from generate import make_colors, generate_files
from pathlib import Path
from os import environ
from curses import setupterm, tigetnum

def main():

    setupterm()
    if(tigetnum("colors") < 256):
        print("Your teminal does not support 256 colors!")
        return

    print("\nTHEME GENERATOR\n\nGenerating colorscheme")

    colors_path = Path(environ['HOME']+"/.config/theme_generator/colors")
    overrides_path = Path(environ['HOME']+"/.config/theme_generator/overrides")

    if colors_path.is_file() == False:
        print('\nno colors file found. creating one at',colors_path,'\n')
        colors_path.touch()

    file = open(colors_path, 'r')
    lines = file.readlines()

    if(len(lines) == 0):
        print("Colors file is empty. Quitting")
        return

    colors,longest = make_colors(lines)

    overrides_colors = {}
    if overrides_path.is_file():
        file = open(overrides_path, 'r')
        lines = file.readlines()
        if(len(lines) > 0):
            print("Found overrides. Patching theme.")
            overrides_colors, _ = make_colors(lines)

    for color in overrides_colors:
        colors[color] = overrides_colors[color]

    if(len(colors) == 0):
        return

    print()
    print_colors(colors,longest)
    generate_files(colors)

    print("Done!")

if __name__ == "__main__":
    main()


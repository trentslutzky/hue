#!/usr/bin/env python
from curses import setupterm, tigetnum
from os import environ
from pathlib import Path
import sys

import args
import prints
import generate

# this is a comment
def main():
    parser = args.make_parser()
    arguments = parser.parse_args()

    if len(sys.argv) <= 1 or (not arguments.theme and not arguments.theme):
        parser.print_help()
        sys.exit(1)

    setupterm()
    if(tigetnum("colors") < 256):
        print("Your teminal does not support 256 colors!")
        return
    
    default_theme = arguments.theme
    variant_light = arguments.light

    paths = {}
    paths['config_dir'] = Path(environ['HOME']+"/.config/hue/")
    paths['themes_dir'] = paths['config_dir'].joinpath("themes")
    paths['templates_dir'] = paths['config_dir'].joinpath("templates")

    if arguments.themes:
        prints.print_themes(paths['themes_dir'])
        sys.exit(1)

    paths['current_theme_dir'] = paths['themes_dir'].joinpath(default_theme)
    paths['theme_colors'] = paths['current_theme_dir'].joinpath("colors.light" if variant_light else "colors.dark")

    try:
        if arguments.preview:
            colors_lines = open(paths['theme_colors'],'r').readlines()
            colors,longest = generate.make_colors(colors_lines)
            prints.print_colors(colors,longest,default_theme)
            sys.exit(1)

        colors_lines = open(paths['theme_colors'],'r').readlines()
        colors,longest = generate.make_colors(colors_lines)
        if not arguments.q:
            prints.print_colors(colors,longest,default_theme)
        generate.generate_files(colors,arguments)
    except FileNotFoundError:
        print("Could not find theme",default_theme,('light' if variant_light else ''))
    

if __name__ == "__main__":
    main()


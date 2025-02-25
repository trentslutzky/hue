#!/usr/bin/env python
import subprocess
from curses import setupterm, tigetnum
from os import environ, system
from pathlib import Path
import sys

import args
import prints
import generate

paths = {}


def build_paths():
    paths['config_dir'] = Path(environ['HOME']+"/.config/hue/")
    paths['cache_dir'] = Path(environ['HOME']+"/.cache/hue/")
    paths['themes_dir'] = paths['config_dir'].joinpath("themes")
    paths['templates_dir'] = paths['config_dir'].joinpath("templates")
    # Ensure all directories exist
    for key, path in paths.items():
        if key.endswith("_dir"):  # Only create directories
            path.mkdir(parents=True, exist_ok=True)


def cache_theme(theme, variant):
    cache_path = paths["cache_dir"]
    with open(cache_path.joinpath("current"), "w+") as file:
        file.write(f"{theme} {variant}")


def main():
    parser = args.make_parser()
    arguments = parser.parse_args()

    if len(sys.argv) <= 1 or (
        not arguments.theme
        and not arguments.themes
        and not arguments.switch
        and not arguments.reload
    ):
        parser.print_help()
        sys.exit(1)

    setupterm()
    if (tigetnum("colors") < 256):
        print("Your teminal does not support 256 colors!")
        return

    build_paths()

    try:
        cached_theme_from_file = open(paths['cache_dir'].joinpath("current"), "r").readlines()
        cache_content = cached_theme_from_file[0]
        cached_theme, cached_variant = cache_content.split(" ")
        cached_theme = cached_theme.strip()
        cached_variant = cached_variant.strip()
    except FileNotFoundError:
        print("No cached theme present! Must run once with theme selected. See hue --help")
        return

    current_theme = arguments.theme
    variant = "light" if arguments.light else "dark"

    if arguments.themes:
        prints.print_themes(paths['themes_dir'])
        sys.exit(1)

    if not arguments.theme:
        current_theme = cached_theme
        variant = cached_variant

    if arguments.switch:
        variant = "dark" if cached_variant == "light" else "light"

    paths['current_theme_dir'] = paths['themes_dir'].joinpath(current_theme)
    paths['theme_colors'] = paths['current_theme_dir'].joinpath("colors."+variant)

    try:
        colors_lines = open(paths['theme_colors'], 'r').readlines()
    except FileNotFoundError:
        if arguments.switch or current_theme == "":
            print("theme cache file is invalid. Please select a theme")
        else:
            print("Could not find theme", current_theme, ('light' if variant == "light" else ''))
        return

    if arguments.preview:
        colors, longest = generate.make_colors(colors_lines)
        prints.print_colors(colors, longest, current_theme)
        sys.exit(1)

    colors, longest = generate.make_colors(colors_lines)
    if not arguments.q:
        prints.print_colors(colors, longest, current_theme)
    generate.generate_files(colors, arguments)

    with open(paths['config_dir'].joinpath("commands"), "r") as commands_file:
        for line in commands_file.readlines():
            if not arguments.q:
                print("RUNNING:", line)
            system(line)

    with open(paths['config_dir'].joinpath("commands."+variant), "r") as commands_file:
        for line in commands_file.readlines():
            if not arguments.q:
                print("RUNNING:", line)
            system(line)

    if variant == "light":
        if not arguments.q:
            print('RUNNING:', 'osascript -e "tell app \\"System Events\\" to tell appearance preferences to set dark mode to false"')
        line = ('osascript -e "tell app \\"System Events\\" to tell appearance preferences to set dark mode to false"')
        system(line)
    else:
        if not arguments.q:
            print('RUNNING:', 'osascript -e "tell app \\"System Events\\" to tell appearance preferences to set dark mode to true"')
        line = ('osascript -e "tell app \\"System Events\\" to tell appearance preferences to set dark mode to true"')
        system(line)

    cache_theme(current_theme, variant)


if __name__ == "__main__":
    main()

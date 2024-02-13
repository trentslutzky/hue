import argparse


def make_parser():
    parser = argparse.ArgumentParser(
            prog="hue",
            usage="hue <arguments>",
            description="HUE the dotfiles color injector"
            )

    parser.add_argument(
            '--preview', '-p', 
            action='store_true',
            help="show generated colors without changing anything")

    parser.add_argument(
            '--themes', '-l',
            action='store_true',
            help="list themes available")

    parser.add_argument(
            '--theme',
            metavar="theme name",
            help="select a theme",
            nargs="?")

    parser.add_argument(
            '--set-default', '-d',
            action='store_true',
            help="set the selected theme as the new default")

    parser.add_argument(
            '--dark',
            action='store_true',
            help="select theme variant dark")

    parser.add_argument(
            '--light',
            action='store_true',
            help="select theme variant light")

    parser.add_argument(
            '--switch', '-s',
            action='store_true',
            help="switch from dark to light or vice versa")

    parser.add_argument(
            '--reload', '-r',
            action='store_true',
            help="reload templates with the current theme")

    parser.add_argument(
            '-q',
            action='store_true',
            help="don't print anything")

    return(parser)

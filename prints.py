from pathlib import Path

RESET = '\033[0m'
PURPLE = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'


def print_warning(text):
    print(YELLOW+str(text)+RESET)


def print_error(text):
    print(RED+str(text)+RESET)


def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


def print_colors(colors, longest, themename="", variant="dark"):
    if themename:
        print(f"\ntheme: {themename}")
        print(f"variant: {variant}\n")
    else:
        print()
    print(f" COLOR  {'NAME'.ljust(longest)}   HEX       RGB")
    print(f" -----  {'----'.ljust(longest,'-')}   ---       ---")

    for name in colors:
        color = colors[name]
        print(
            get_color_escape(
                color['color_rgb'][0],
                color['color_rgb'][1],
                color['color_rgb'][2],
            ),
            "█████",
            RESET,
            name.ljust(longest, ' '),
            ' ',
            color['color_hex'],
            ' ',
            color['color_rgb'],
        )
    print(RESET)


def print_themes(themes_dir: Path):
    print("\nCustom Themes:\n")

    for theme_dir in themes_dir.iterdir():
        if theme_dir.is_dir():  # Ensure it's a directory
            theme_name = theme_dir.name
            variants = []

            if (theme_dir / "colors.light").is_file():
                variants.append("light")
            if (theme_dir / "colors.dark").is_file():
                variants.append("dark")

            variants_str = ", ".join(variants) if variants else "none"
            print(f"{theme_name} - variants: {variants_str}")

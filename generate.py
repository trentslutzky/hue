from pathlib import Path
from os import environ
import re

from prints import print_warning, RESET, get_color_escape


def make_colors(lines):
    longest = 0
    colors = {}

    for line in lines:
        line = line.replace("\n", "")
        line = re.sub(' +', ' ', line)
        line_split = line.split(" ")
        if len(line_split) < 2:
            continue
        name = line_split[0]
        color_hex = line_split[1]
        color_rgb = tuple(int((color_hex.lstrip("#"))[i:i+2], 16) for i in (0, 2, 4))

        if (len(name) > longest):
            longest = len(name)

        colors[name] = {
            "color_hex": color_hex,
            "color_rgb": color_rgb,
        }

    return colors, longest


def generate_files(colors, args):
    if not args.q:
        print("Generating files from templates\n")

    templates_path = Path(environ['HOME']+"/.config/hue/templates/")
    if (templates_path.is_dir() is False):
        print_warning("No templates found in "+str(templates_path))
        templates_path.mkdir()
        return

    files = templates_path.glob("**/*")
    templates = []
    for t in files:
        templates.append(t)
        if not args.q:
            print("Found template: "+t.name)

    if (len(templates) == 0):
        print_warning("No templates found in "+str(templates_path))
        return

    for template in templates:
        generate_template_output(template, colors, args)


def generate_template_output(template, colors, args):
    file = open(template, 'r')
    lines = file.readlines()

    target = ""
    colors_set = 0
    use_hash = True

    new_lines = []

    for line in lines:
        line_split = line.split(" ")

        if ("#[no_hash]" in line):
            use_hash = False
            continue

        if ("#[target]" in line):
            target = line_split[1].strip()
            continue

        if ("#[run]" in line):
            continue

        keywords = re.findall(r'\{\{.*?\}\}', line)

        if (len(keywords) == 0):
            new_lines.append(line)
            continue

        for keyword in keywords:
            keyword_name = re.sub('[{{}}]', "", keyword)
            color_hex = ""

            if (keyword_name in colors):
                color_hex = colors[keyword_name]["color_hex"]
                colors_set += 1

            if (not use_hash):
                color_hex = color_hex.replace("#", "")
            line = line.replace(keyword, color_hex)
            new_lines.append(line)

    output_file = open(target, "w")
    output_file.writelines(new_lines)
    output_file.close()

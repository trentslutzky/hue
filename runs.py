from pathlib import Path
from os import environ, system

from prints import print_warning


def run_from_files(args):
    if not args.q:
        print("\nRunnig commands from templates\n")

    templates_path = Path(environ['HOME']+"/.config/hue/templates/")
    if (templates_path.is_dir() is False):
        print_warning("No templates found in "+str(templates_path))
        templates_path.mkdir()
        return

    files = templates_path.glob("**/*")
    templates = []
    for t in files:
        templates.append(t)

    if (len(templates) == 0):
        return

    runs = []

    for template in templates:
        for run in runs_from_template(template, args):
            runs.append(run)

    print("\nRunning commands from templates:")
    for run in runs:
        print(run)
        system(run)


def runs_from_template(template, args):
    if not args.q:
        print(f"{template.name}")
    file = open(template, 'r')
    lines = file.readlines()

    runs = []

    if not args.q:
        print("  -> Looking for keywords")

    for line in lines:
        if ("#[run]" in line):
            run = line.replace("#[run] ", "").strip()
            if not args.q:
                print(f"  RUN: {run}")
            runs.append(run)
            continue

    return runs

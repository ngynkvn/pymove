from glob import glob
from colors import *
import re
import os
import toml
from shutil import move
from prettytable import PrettyTable
from pyfiglet import Figlet

f = Figlet(font="slant")


# Regex -> Target Directory
CONFIG = {
    r".*\.exe": "Executables/",
    r".*\.msi": "Executables/",
    r".*\.pdf": "../Books/",
    r".*\.zip": "Archives/",
    r".*\.ps1": None,
    r".pymove.toml": None,
    r"pymove.py": None,
}


def read_toml(path):
    print(blue(f"{path} found"))
    tom = toml.load(path)
    config = {rule.get("regex"): rule.get("target") for rule in tom.get("rule")}
    return config


def validate_config(c):
    all_good = True
    missing = []
    for k, v in CONFIG.items():
        if v == None:
            continue
        if os.path.exists(v):
            if not os.path.isdir(v):
                all_good = False
                print(red(f"The path {v} for associated regex {k} is invalid."))
        else:
            if v not in missing:
                print(yellow(f"The path {v} does not exist"))
                missing.append([v, k])
    if not all_good:
        raise ValueError("Configuration was found to be invalid.")
    if missing:
        table = PrettyTable()
        table.field_names = ["Target", "Regex"]
        table.align = "l"
        table.add_rows(missing)
        response = ask(
            yellow(
                f"The following paths do not exist currently:\n-{table}\nAre you okay with PyMover creating these directories?"
            ),
            "Y/n",
        )
        if response not in YES_DEFAULT:
            raise RuntimeError("Exited by user.")


toml_path = os.path.join(os.getcwd(), ".pymove.toml")
if os.path.exists(toml_path):
    CONFIG = read_toml(toml_path)


regexes = {re.compile(k): v for k, v in CONFIG.items()}

YES_DEFAULT = ["Y", "y", "Y/n"]


def main():
    # Banner
    print(green(f.renderText("PyMover")))
    print(green("Globbing the current directory.."))
    unhandled = []
    for file in glob("*"):
        if not os.path.isfile(file):
            continue
        print(yellow(file))
        matched = False
        for regex, target in regexes.items():
            if os.path.isfile(file) and regex.match(file):
                matched = True
                if target is None:
                    print(yellow("--Ignored--"))
                    continue
                if not os.path.exists(target):
                    response = ask(
                        green(f"Path to {target} does not exist, create?"), "Y/n"
                    )
                    if response in YES_DEFAULT:
                        new_dir = os.path.join(os.getcwd(), target)
                        print(yellow(f"Creating path {new_dir}"))
                        os.mkdir(new_dir)
                dest = os.path.join(target, file)
                print(yellow(f"Moving {file} to {dest}"))
                move(file, dest)
        if not matched:
            unhandled.append(file)
    table = PrettyTable()
    table.align = "l"
    table.add_column("File", unhandled)
    print(
        green(
            f"The follow files were not matched.\n-{table}\nFor PyMover to handle these files please add rules to the configuration file ({toml_path})."
        )
    )


def ask(field, default):
    """
    Prompt
    """
    value = input(f"> {field} [{default}]: ")
    value = value or default
    if not value:
        raise ValueError(red("f{field} was not given."))
    return value


def cli():
    try:
        # Validate the config file.
        validate_config(CONFIG)
        main()
    except:
        print(red("An error occured during runtime."))
        raise


if __name__ == "__main__":
    cli()
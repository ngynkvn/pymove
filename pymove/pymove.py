from glob import glob
from colors import *
import re
import os
from shutil import move
from prettytable import PrettyTable
from pyfiglet import Figlet

from config.config import CONFIG, toml_path, validate_config
from interface.interface import ask, YES_DEFAULT

f = Figlet(font="slant")
REGEXES = {re.compile(k): v for k, v in CONFIG.items()}


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
        for regex, target in REGEXES.items():
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


def cli():
    try:
        # Validate the config file.
        validate_config()
        main()
    except:
        print(red("An error occured during runtime."))
        raise


if __name__ == "__main__":
    cli()
import os
import toml
from colors import *
from prettytable import PrettyTable
from interface.interface import ask, YES_DEFAULT


def read_toml(path):
    print(blue(f"{path} found"))
    tom = toml.load(path)
    config = {rule.get("regex"): rule.get("target") for rule in tom.get("rule")}
    return config


# Regex -> Target Directory
DEFAULT_CONFIG = {
    r".*\.exe": "Executables/",
    r".*\.msi": "Executables/",
    r".*\.pdf": "../Books/",
    r".*\.zip": "Archives/",
    r".*\.ps1": None,
    r".pymove.toml": None,
    r"pymove.py": None,
}
CONFIG = None


toml_path = os.path.join(os.getcwd(), ".pymove.toml")

if os.path.exists(toml_path):
    CONFIG = read_toml(toml_path)
else:
    CONFIG = DEFAULT_CONFIG
CONFIG[r".pymove.toml"] = None
CONFIG[r"pymove.py"] = None


def validate_config():
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
                f"The following paths do not exist currently:\n{table}\nAre you okay with PyMover creating these directories?"
            ),
            "Y/n",
        )
        if response not in YES_DEFAULT:
            raise RuntimeError("Exited by user.")

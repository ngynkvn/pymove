from colors import *

YES_DEFAULT = ["Y", "y", "Y/n"]


def ask(field, default):
    """
    Prompt
    """
    value = input(f"> {field} [{default}]: ")
    value = value or default
    if not value:
        raise ValueError(red("f{field} was not given."))
    return value

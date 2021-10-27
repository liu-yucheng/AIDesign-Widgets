"""The "widgets" command executable."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import copy
import pkg_resources
import sys

# Private attributes ...

# Init _version
_version = "<unknown version>"
_packages = pkg_resources.require("aidesign-widgets")
if len(_packages) > 0:
    _version = _packages[0].version

_brief_usage = "widgets <command> ..."
_usage = fr"""Usage: {_brief_usage}
Help: widgets help"""

# ... Private attributes
# Nominal info strings ...

info = fr"""AIDesign-Widgets (aidesign-widgets) {_version}
{_usage}
"""
"""The primary info to display."""

# ... Nominal info strings
# Error info strings ...

unknown_command_info = f"\"{_brief_usage}\""r""" gets an unknown command: {}"""fr"""
{_usage}
"""
"""The info to display when the executable gets an unknown command."""

unknown_arg_info = f"\"{_brief_usage}\""r""" gets an unknown argument: {}"""fr"""
{_usage}
"""
"""The info to display when the executable gets an unknown argument."""

# ... Error info strings
# Other public attributes ...

argv_copy = None
"""A consumable copy of sys.argv."""

# ... Other public attributes


def _run_command():
    global argv_copy
    assert len(argv_copy) > 0
    command = argv_copy.pop(0)
    if len(command) <= 0:
        print(unknown_command_info.format(command), end="")
        exit(1)
    elif command[0] == "-":
        print(unknown_arg_info.format(command), end="")
        exit(1)
    elif command == "help":
        from aidesign_widgets import help
        help.argv_copy = argv_copy
        help.run()
    elif command == "grid-crop":
        from aidesign_widgets import grid_crop
        grid_crop.argv_copy = argv_copy
        grid_crop.run()
    elif command == "rand-crop":
        from aidesign_widgets import rand_crop
        rand_crop.argv_copy = argv_copy
        rand_crop.run()
    else:
        print(unknown_command_info.format(command), end="")
        exit(1)


def main():
    """Starts the executable."""
    global argv_copy
    argv_length = len(sys.argv)
    assert argv_length >= 1
    if argv_length == 1:
        print(info, end="")
        exit(0)
    # elif argv_length > 1
    else:
        argv_copy = copy.deepcopy(sys.argv)
        argv_copy.pop(0)
        _run_command()


# Let main be the script entry point
if __name__ == '__main__':
    main()

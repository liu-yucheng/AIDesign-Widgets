""""widgets" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import pkg_resources
import sys

# Aliases

_argv = sys.argv
_deepcopy = copy.deepcopy
_exit = sys.exit
_stderr = sys.stderr

# -
# Initialize _version

_version = "<unknown version>"

try:
    _packages = pkg_resources.require("aidesign-widgets")

    if len(_packages) > 0:
        _version = _packages[0].version

except Exception as _:
    pass
# end try

# -

brief_usage = "widgets <command> ..."
"""Brief usage."""

usage = fr"""

Usage: {brief_usage}
Help: widgets help

""".strip()
"""Usage."""

info = fr"""

AIDesign-Widgets (aidesign-widgets) {_version}
{usage}

""".strip()
"""Primary info to display."""

unknown_cmd_info = fr"""

"{brief_usage}" gets an unknown command: {{}}
{usage}

""".strip()
"""Info to display when getting an unknown command."""

unknown_arg_info = fr"""

"{brief_usage}" gets an unknown argument: {{}}
{usage}

""".strip()
"""Info to display when getting an unknown argument."""

argv_copy = None
"""Consumable copy of sys.argv."""


def _run_command():
    global argv_copy
    argv_copy = list(argv_copy)

    assert len(argv_copy) > 0

    command = argv_copy.pop(0)
    command = str(command)

    if len(command) <= 0:
        print(unknown_cmd_info.format(command), file=_stderr)
        _exit(1)
    elif command[0] == "-":
        print(unknown_arg_info.format(command), file=_stderr)
        _exit(1)
    elif command == "help":
        from aidesign_widgets.exes import widgets_help
        widgets_help.argv_copy = argv_copy
        widgets_help.run()
    elif command == "grid-crop":
        from aidesign_widgets.exes import widgets_grid_crop
        widgets_grid_crop.argv_copy = argv_copy
        widgets_grid_crop.run()
    elif command == "rand-crop":
        from aidesign_widgets.exes import widgets_rand_crop
        widgets_rand_crop.argv_copy = argv_copy
        widgets_rand_crop.run()
    elif command == "path-name":
        from aidesign_widgets.exes import widgets_path_name
        widgets_path_name.argv_copy = argv_copy
        widgets_path_name.run()
    else:
        print(unknown_cmd_info.format(command), file=_stderr)
        _exit(1)
    # end if


def main():
    """Starts the executable."""
    global argv_copy
    argv_length = len(_argv)

    assert argv_length >= 1

    if argv_length == 1:
        print(info)
        _exit(0)
    else:  # elif argv_length > 1:
        argv_copy = _deepcopy(_argv)
        argv_copy.pop(0)
        _run_command()


if __name__ == '__main__':
    main()

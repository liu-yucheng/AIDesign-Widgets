""""widgets info" command executable."""

# Copyright 2022-2023 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import sys

from aidesign_widgets.libs import pack_info

# Aliases

_argv = sys.argv
_deepcopy = copy.deepcopy
_exit = sys.exit
_stderr = sys.stderr

# -

brief_usage = "widgets info"
"""Brief usage."""

usage = fr"""

Usage: {brief_usage}
Help: widgets help

""".strip()
"""Usage."""

info = fr"""

AIDesign-Widgets package info:
    Package name:   {pack_info.pack_name}
    Version:        {pack_info.ver}
    Author:         {pack_info.author}
    Copyright:      {pack_info.cr}
    Description:    {pack_info.desc}

""".strip()
"""Primary info to display."""

too_many_args_info = fr"""

"{brief_usage}" gets too many arguments
Expects 0 arguments; Gets {{}} arguments
{usage}

""".strip()
"""Info to display when the executable gets too many arguments."""

argv_copy = None
"""Consumable copy of sys.argv."""


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)

    assert argv_copy_length >= 0

    if argv_copy_length == 0:
        print(info)
        _exit(0)
    else:  # elif argv_copy_length > 0:
        print(too_many_args_info.format(argv_copy_length), file=_stderr)
        _exit(1)


def main():
    """Starts the executable."""
    global argv_copy
    argv_length = len(_argv)

    assert argv_length >= 1

    argv_copy = _deepcopy(_argv)
    argv_copy.pop(0)
    run()


if __name__ == "__main__":
    main()

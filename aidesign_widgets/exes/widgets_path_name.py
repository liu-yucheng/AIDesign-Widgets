""""widgets path-name" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import pathlib
import sys

from os import path as ospath

_argv = sys.argv
_deepcopy = copy.deepcopy
_isabs = ospath.isabs
_join = ospath.join
_Path = pathlib.Path
_stderr = sys.stderr

brief_usage = "widgets path-name <relative-path>"
"""Brief usage."""
usage = str(
    f"Usage: {brief_usage}\n"
    f"Help: widgets help"
)
"""Usage."""

info = f"{{}}"
"""Primary info to display."""

too_few_args_info = str(
    f"\"{brief_usage}\" gets too few arguments\n"
    f"Expects 1 arguments; Gets {{}} arguments\n"
    f"{usage}"
)
"""Info to display when getting too few arguments."""

too_many_args_info = str(
    f"\"{brief_usage}\" gets too many arguments\n"
    f"Expects 1 arguments; Gets {{}} arguments\n"
    f"{usage}"
)
"""Info to display when getting too many arguments."""

argv_copy = None
"""Consumable copy of sys.argv."""


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)

    if argv_copy_length <= 0:
        print(too_few_args_info.format(argv_copy_length), file=_stderr)
        exit(1)
    elif argv_copy_length == 1:
        path_name = argv_copy.pop(0)
        path_name = str(path_name)

        if not _isabs(path_name):
            path_name = _join(".", path_name)

        path_name = str(_Path(path_name).resolve())

        path_name = repr(path_name)[1: -1]
        path_name = f"\"{path_name}\""

        print(info.format(path_name))
    else:  # elif argv_copy_length > 1:
        print(too_many_args_info.format(argv_copy_length), file=_stderr)
        exit(1)
    # end if


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

""""widgets help" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import pydoc
import sys

# Aliases

_argv = sys.argv
_deepcopy = copy.deepcopy
_exit = sys.exit
_pager = pydoc.pager
_stderr = sys.stderr

# -

brief_usage = "widgets help"
"""Brief usage."""

usage = fr"""

Usage: {brief_usage}
Help: widgets help

""".strip()
"""Usage."""

info = fr"""

Usage: widgets <command> ...
==== Commands ====
help:
    When:   You need help info. For example, now.
    How-to: widgets help
info:
    When:   You need package info.
    How-to: widgets info
grid-crop:
    When:   You want to crop a large image into small pieces, with the crop positions having a grid-like alignment.
    How-to: widgets grid-crop
rand-crop:
    When:   You want to crop a large image into small pieces, with randomly picked crop positions.
    How-to: widgets rand-crop
path-name:
    When:   You want to show a path name as an escaped string with quotes, which can be directly used in JSON.
    How-to: widgets path-name <relative-path>
bulk-crop:
    When:   You want to crop all the images in a folder and save the crops into subfolders of another folder.
    How-to: widgets bulk-crop <command> ...
    ==== Commands ====
    grid:
        When:   You want to start a bulk grid cropping session.
        How-to: widgets bulk-crop grid
    rand:
        When:   You want to start a bulk random cropping session.
        How-to: widgets bulk-crop rand

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
        _pager(info)
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

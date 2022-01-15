""""widgets help" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import sys

# Private attributes ...

_brief_usage = "widgets help"
_usage = fr"""Usage: {_brief_usage}
Help: widgets help"""

# ... Private attributes
# Nominal info strings ...

info = r"""Usage: widgets <command> ...
==== Commands ====
help:
    When:   You need help info. For example, now.
    How-to: widgets help
grid-crop:
    When:   You want to crop a large image into small pieces, with the crop positions having a grid-like alignment.
    How-to: widgets grid-crop
rand-crop:
    When:   You want to crop a large image into small pieces, with randomly picked crop positions.
    How-to: widgets rand-crop
path-name:
    When:   You want to show a path name as an escaped string with quotes, which can be directly used in JSON.
    How-to: widgets path-name
"""
"""The primary info to display."""

# ... Nominal info strings
# Error info strings ...

too_many_args_info = f"\"{_brief_usage}\""r""" gets too many arguments
Expects 0 arguments; Gets {} arguments"""fr"""
{_usage}
"""
"""The info to display when the executable gets too many arguments."""

# ... Error info stirngs
# Other public attributes ...

argv_copy = None
"""A consumable copy of sys.argv."""

# ... Other public attributes


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)
    assert argv_copy_length >= 0
    if argv_copy_length == 0:
        print(info, end="")
        exit(0)
    # elif argv_copy_length > 0
    else:
        print(too_many_args_info.format(argv_copy_length), end="")
        exit(1)


def main():
    """Starts the executable."""
    global argv_copy
    argv_length = len(sys.argv)
    assert argv_length >= 1
    argv_copy = copy.deepcopy(sys.argv)
    argv_copy.pop(0)
    run()


# Let main be the script entry point
if __name__ == "__main__":
    main()

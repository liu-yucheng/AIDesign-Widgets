"""Utilities."""

# Copyright 2022-2023 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

# TimedInput imports

import asyncio
import sys
import threading

# jsonrw imports

import json

# randbool imports

import random

# batchlog imports

import typing

# TimedInput aliases

_create_subprocess_exec = asyncio.create_subprocess_exec
_executable = sys.executable
_PIPE = asyncio.subprocess.PIPE
_run = asyncio.run
_stdin = sys.stdin
_Thread = threading.Thread

# jsonrw aliases

_jsondump = json.dump
_jsondumps = json.dumps
_jsonload = json.load
_jsonloads = json.loads
_NoneType = type(None)

# randbool aliases

_randint = random.randint

# batchlog aliases

_IO = typing.IO

#


class TimedInput:
    """Timed input.

    Python "native" and platform independent timed input command prompt.
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    def __init__(self):
        """Inits self with the given args."""
        self._input_str = None

        subproc_code = fr"""

input_str = input()
print(input_str)

"""
        subproc_code = subproc_code.strip()
        subproc_code = subproc_code + "\n"
        self._subproc_code = subproc_code

        self._subproc = None

    async def _async_run_subproc(self):
        self._subproc = await _create_subprocess_exec(
            _executable, "-c", self._subproc_code, stdin=_stdin, stdout=_PIPE
        )
        data = await self._subproc.stdout.readline()
        self._input_str = data.decode("utf-8", "replace").rstrip()
        await self._subproc.wait()

    def _take(self):
        self._subproc = None
        _run(self._async_run_subproc())

    def take(self, timeout=5.0):
        """Takes and returns a string from user input with a given timeout.

        Args:
            timeout: the timeout period length in seconds

        Returns:
            self._input_str: the taken input string, or None if there is a timeout
        """
        timeout = float(timeout)
        self._input_str = None
        thread = _Thread(target=self._take)
        thread.start()
        thread.join(timeout)

        if self._input_str is None and self._subproc is not None:
            self._subproc.terminate()

        return self._input_str


def load_json(from_file):
    """Loads the data from a JSON file to an object and returns the object.

    Args:
        from_file: the JSON file location

    Returns:
        result: the object
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    from_file = str(from_file)

    file = open(from_file, "r")
    obj = _jsonload(file)
    file.close()

    if isinstance(obj, dict):
        result = dict(obj)
    elif isinstance(obj, list):
        result = list(obj)
    elif isinstance(obj, str):
        result = str(obj)
    elif isinstance(obj, bool):
        result = bool(obj)
    elif isinstance(obj, int):
        result = int(obj)
    elif isinstance(obj, float):
        result = float(obj)
    elif isinstance(obj, _NoneType):
        result = None
    else:
        result = None
    # end if

    return result


def save_json(from_obj, to_file):
    """Saves the data from an object to a JSON file.

    Args:
        from_obj: the object
        to_file: the JSON file location
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    if isinstance(from_obj, dict):
        from_obj = dict(from_obj)
    elif isinstance(from_obj, list):
        from_obj = list(from_obj)
    elif isinstance(from_obj, str):
        from_obj = str(from_obj)
    elif isinstance(from_obj, bool):
        from_obj = bool(from_obj)
    elif isinstance(from_obj, int):
        from_obj = int(from_obj)
    elif isinstance(from_obj, float):
        from_obj = float(from_obj)
    elif isinstance(from_obj, _NoneType):
        from_obj = None
    else:
        from_obj = None
    # end if

    to_file = str(to_file)

    file = open(to_file, "w+")
    _jsondump(from_obj, file, indent=4)
    file.close()


def load_json_str(from_str):
    """Loads the data from a JSON string to an object and returns the object.

    Args:
        from_str: the JSON string

    Returns:
        result: the object
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    from_str = str(from_str)

    obj = _jsonloads(from_str)

    if isinstance(obj, dict):
        result = dict(obj)
    elif isinstance(obj, list):
        result = list(obj)
    elif isinstance(obj, str):
        result = str(obj)
    elif isinstance(obj, bool):
        result = bool(obj)
    elif isinstance(obj, int):
        result = int(obj)
    elif isinstance(obj, float):
        result = float(obj)
    elif isinstance(obj, _NoneType):
        result = None
    else:
        result = None
    # end if

    return result


def save_json_str(from_obj):
    """Saves the data from an object to a JSON string and return the string

    Args:
        from_obj: the object

    Returns:
        result: the JSON string
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    if isinstance(from_obj, dict):
        from_obj = dict(from_obj)
    elif isinstance(from_obj, list):
        from_obj = list(from_obj)
    elif isinstance(from_obj, str):
        from_obj = str(from_obj)
    elif isinstance(from_obj, bool):
        from_obj = bool(from_obj)
    elif isinstance(from_obj, int):
        from_obj = int(from_obj)
    elif isinstance(from_obj, float):
        from_obj = float(from_obj)
    elif isinstance(from_obj, _NoneType):
        from_obj = None
    else:
        from_obj = None
    # end if

    to_str = _jsondumps(from_obj, indent=4)

    result = to_str
    return result


def rand_bool():
    """Produce a random boolean value.

    This is like flipping a fair coin.

    Returns:
        result: the random boolean
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    result = bool(_randint(0, 1))
    return result


def logstr(logs, string=""):
    """Logs a string on the log file objects.

    Args:
        logs: the log file objects
        string: the string to log
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    logs = list(logs)
    string = str(string)

    for log in logs:
        log: _IO
        log.write(string)


def logln(logs, line=""):
    """Logs a line on the log file objects.

    Args:
        logs: the log file objects
        line: the line to log
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    logs = list(logs)
    line = str(line)

    line = line + "\n"

    for log in logs:
        log: _IO
        log.write(line)


def flushlogs(logs):
    """Flushes the logs.

    Args:
        logs: the log file objects
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU GPL3 license.
    # GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt

    logs = list(logs)

    for log in logs:
        log: _IO
        log.flush()


def clamp_float(inval, bound1, bound2):
    """Clamps inval to the range bounded by bounds 1 and 2.

    Performs comparisons in floats.

    Args:
        inval: the input value
        bound1: bound 1
        bound2: bound 2

    Returns:
        result: the result
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU LGPL3 license.
    # GNU LGPL3 license copy: https://www.gnu.org/licenses/lgpl-3.0.txt
    # GNU LGPL3 is based on GNU GPL3, GNU GPL3 copy: https://www.gnu.org/licenses/gpl-3.0.txt

    inval = float(inval)
    bound1 = float(bound1)
    bound2 = float(bound2)

    if bound1 < bound2:
        floor = bound1
        ceil = bound2
    else:  # elif bound1 >= bound2:
        floor = bound2
        ceil = bound1
    # end if

    result = inval

    if result < floor:
        result = floor

    if result > ceil:
        result = ceil

    return result


def clamp_int(inval, bound1, bound2):
    """Clamps inval to the range bounded by bounds 1 and 2.

    Performs comparisons in integers.

    Args:
        inval: the input value
        bound1: bound 1
        bound2: bound 2

    Returns:
        result: the result
    """

    # Part of LYC-PythonUtils
    # Copyright 2022 Yucheng Liu. GNU LGPL3 license.
    # GNU LGPL3 license copy: https://www.gnu.org/licenses/lgpl-3.0.txt
    # GNU LGPL3 is based on GNU GPL3, GNU GPL3 copy: https://www.gnu.org/licenses/gpl-3.0.txt

    inval = int(inval)
    bound1 = int(bound1)
    bound2 = int(bound2)

    if bound1 < bound2:
        floor = bound1
        ceil = bound2
    else:  # elif bound1 >= bound2:
        floor = bound2
        ceil = bound1
    # end if

    result = inval

    if result < floor:
        result = floor

    if result > ceil:
        result = ceil

    return result

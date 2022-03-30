""""widgets grid-crop" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import datetime
import os
import sys
import traceback
import typing

from os import path as ospath
from PIL import Image as pil_image

from aidesign_widgets.libs import defaults
from aidesign_widgets.libs import utils

# Aliases

_abspath = ospath.abspath
_argv = sys.argv
_basename = ospath.basename
_deepcopy = copy.deepcopy
_exit = sys.exit
_flush_logs = utils.flushlogs
_format_exc = traceback.format_exc
_IO = typing.IO
_join = ospath.join
_load_json = utils.load_json
_logln = utils.logln
_logstr = utils.logstr
_makedirs = os.makedirs
_now = datetime.datetime.now
_pil_image = pil_image
_pil_image_open = pil_image.open
# _print_exc = traceback.print_exc  # Debug
_split_text = ospath.splitext
_stderr = sys.stderr
_stdout = sys.stdout
_TimedInput = utils.TimedInput

# -

brief_usage = "widgets grid-crop"
"""Brief usage."""

usage = fr"""

Usage: {brief_usage}
Help: widgets help

""".strip()
"""Usage."""

timeout = float(10)
"""Timeout in seconds."""

info = fr"""

"{brief_usage}" command config:
{{}}
-
Please confirm the above config file contents
Do you want to continue? [ Y (Yes) | n (no) ]: < default: Yes, timeout: {timeout} seconds >

""".strip()
"""Primary info to display."""

will_start_info = fr"""

Will start cropping
---- The following will be logged to {{}} ----

""".strip()
"""Info to display before cropping starts."""

stopped_info = fr"""

---- The above has been logged to {{}} ----
Cropping stopped

""".strip()
"""Info to display after cropping stops."""

completed_info = fr"""

---- The above has been logged to {{}} ----
Cropping completed

""".strip()
"""Info to display after cropping completes."""

aborted_info = fr"""

Aborted the image cropping process

""".strip()
"""Info to display when the user aborts the cropping process."""

too_many_args_info = fr"""

"{brief_usage}" gets too many arguments
Expects 0 arguments; Gets {{}} arguments
{usage}

""".strip()
"""Info to display when the executable gets too many arguments."""

argv_copy = None
"""Consumable copy of sys.argv."""
config_loc = None
"""Config location."""
log_loc = None
"""Log location."""


def _parse_image_loc(config):
    config: dict = config

    image_loc = config["image_location"]

    if image_loc is None:
        raise ValueError("Image location cannot be None")

    image_loc = str(image_loc)
    image_loc = _abspath(image_loc)
    return image_loc


def _parse_out_path(config):
    config: dict = config

    out_path = config["output_path"]

    if out_path is None:
        raise ValueError("Output path cannot be None")

    out_path = str(out_path)
    out_path = _abspath(out_path)
    return out_path


def _parse_crop_res(config):
    config: dict = config

    crop_res = config["crop_resolution"]

    if crop_res is None:
        raise ValueError("Crop resolution cannot be None")

    crop_res = int(crop_res)

    if crop_res == 0:
        crop_res = 1

    if crop_res < 0:
        crop_res *= -1

    return crop_res


def _parse_resize_res(config):
    config: dict = config

    resize_res = config["resize_resolution"]

    if resize_res is not None:
        resize_res = int(resize_res)

        if resize_res == 0:
            resize_res = 1

        if resize_res < 0:
            resize_res *= -1
    else:  # elif resize_res is None:
        resize_res = None
    # end if

    return resize_res


def _parse_start_pos(config, key):
    config: dict = config
    key = str(key)

    start_pos = config[key]

    if start_pos is None:
        start_pos = 0
    else:  # elif start_pos is not None:
        start_pos = int(start_pos)
    # end if

    if start_pos < 0:
        start_pos *= -1

    return start_pos


def _parse_start_pos_x(config):
    return _parse_start_pos(config, "start_position_x")


def _parse_start_pos_y(config):
    return _parse_start_pos(config, "start_position_y")


def _parse_max_crop_count(config, key):
    config: dict = config
    key = str(key)

    max_crop_count = config[key]

    if max_crop_count is None:
        max_crop_count = sys.maxsize
    else:  # elif max_crop_count is not None
        max_crop_count = int(max_crop_count)
    # end if

    if max_crop_count < 0:
        max_crop_count *= -1

    return max_crop_count


def _parse_max_crop_count_x(config):
    return _parse_max_crop_count(config, "max_crop_count_x")


def _parse_max_crop_count_y(config):
    return _parse_max_crop_count(config, "max_crop_count_y")


def _find_crop_name(image_name, pos_x, pos_y, crop_res, resize_res):
    image_name = str(image_name)
    pos_x = int(pos_x)
    pos_y = int(pos_y)
    crop_res = int(crop_res)

    if resize_res is None:
        resize_res = None
    else:  # elif resize_res is not None:
        resize_res = int(resize_res)
    # end if

    pos_tag = f"-At-{pos_x}-{pos_y}"
    crop_tag = f"-Crop-{crop_res}"

    if resize_res is None:
        resize_tag = ""
    else:  # elif resize_res is not None:
        resize_tag = f"-Resize-{resize_res}"
    # end if

    now = _now()

    timestamp = str(
        f"-Time-{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
        f"{now.microsecond:06}"
    )

    ext = ".jpg"
    name = f"{image_name}{pos_tag}{crop_tag}{resize_tag}{timestamp}{ext}"
    return name


def _prep_and_crop(logs):
    logs: list[_IO] = logs

    info = str(
        "Started preparation\n"
        "-"
    )

    _logln(logs, info)

    # Parse config
    config = _load_json(config_loc)

    image_loc = _parse_image_loc(config)
    _logln(logs, f"Image location: {image_loc}")
    out_path = _parse_out_path(config)
    _logln(logs, f"Output path: {out_path}")
    crop_res = _parse_crop_res(config)
    _logln(logs, f"Crop resolution: {crop_res}")
    resize_res = _parse_resize_res(config)

    if resize_res is None:
        _logln(logs, "No resize, keep crop resolution")
    else:
        _logln(logs, f"Resize resolution: {resize_res}")
    # end if

    start_pos_x = _parse_start_pos_x(config)
    _logln(logs, f"Start position X: {start_pos_x}")
    start_pos_y = _parse_start_pos_y(config)
    _logln(logs, f"Start position Y: {start_pos_y}")
    max_crop_count_x = _parse_max_crop_count_x(config)
    _logln(logs, f"Max crop count X: {max_crop_count_x}")
    max_crop_count_y = _parse_max_crop_count_y(config)
    _logln(logs, f"Max crop count Y: {max_crop_count_y}")

    # Edit PIL max image pixels to avoid zip bomb detection false alarm
    max_width = 65535
    max_height = 65535
    max_pixels = max_width * max_height
    _pil_image.MAX_IMAGE_PIXELS = max_pixels
    _logln(logs, f"Tweaked PIL safety max pixels:  Width: {max_width}  Height: {max_height}  Total: {max_pixels}")

    # Read image
    image = _pil_image_open(image_loc)
    image_name = _split_text(_basename(image_loc))[0]
    _logln(logs, "Completed loading image")

    # Ensure output folder
    _makedirs(out_path, exist_ok=True)

    info = str(
        "-\n"
        "Completed preparation"
    )

    _logln(logs, info)

    info = str(
        "Started grid cropping\n"
        "-"
    )

    _logln(logs, info)

    # Start actual cropping
    count_x = 0
    count_y = 0
    total_count = 0
    pos_x = start_pos_x
    pos_y = start_pos_y
    width, height = image.size

    while count_y < max_crop_count_y and pos_y + crop_res <= height:
        count_x = 0
        pos_x = start_pos_x

        while count_x < max_crop_count_x and pos_x + crop_res <= width:
            box = (pos_x, pos_y, pos_x + crop_res, pos_y + crop_res)
            cropped = image.crop(box)

            if resize_res is not None:
                cropped = cropped.resize(size=(resize_res, resize_res), resample=_pil_image.BICUBIC)

            name = _find_crop_name(image_name, pos_x, pos_y, crop_res, resize_res)
            loc = _join(out_path, name)
            cropped.save(loc, quality=95)
            total_count += 1

            if total_count == 1 or total_count % 500 == 0:
                _logln(logs, f"Saved {total_count} cropped images")

            count_x += 1
            pos_x += crop_res
        # end while

        count_y += 1
        pos_y += crop_res
    # end while

    _logln(logs, f"Saved {total_count} cropped images")

    info = str(
        "-\n"
        "Completed grid cropping"
    )

    _logln(logs, info)
    _flush_logs(logs)


def _start_cropping():
    global log_loc

    start_time = _now()
    log_file: _IO = open(log_loc, "a+")
    all_logs = [_stdout, log_file]
    err_logs = [_stderr, log_file]

    info = str(
        "AIDesign-Widgets grid cropping\n"
        "-"
    )

    _logln(all_logs, info)

    try:
        _prep_and_crop(all_logs)
    except BaseException as base_exception:
        _logstr(err_logs, _format_exc())
        end_time = _now()
        exe_time = end_time - start_time

        info = str(
            f"-\n"
            f"Execution stopped after: {exe_time} (days, hours: minutes: seconds)\n"
            f"-"
        )

        _logln(all_logs, info)
        log_file.close()
        raise base_exception
    # end try

    end_time = _now()
    exe_time = end_time - start_time

    info = str(
        f"-\n"
        f"Execution time: {exe_time} (days, hours: minutes: seconds)\n"
        f"-"
    )

    _logln(all_logs, info)
    log_file.close()


def run():
    """Runs the executable as a command."""
    global argv_copy
    global config_loc
    global log_loc
    argv_copy_length = len(argv_copy)

    assert argv_copy_length >= 0

    if argv_copy_length == 0:
        config_loc = _join(defaults.app_data_path, defaults.grid_crop_config_name)
        print(info.format(config_loc))

        timed_input = _TimedInput()
        answer = timed_input.take(timeout)

        if answer is None:
            answer = "Yes"
            print(f"\n{answer} (timeout)")
        elif len(answer) <= 0:
            answer = "Yes"
            print(f"{answer} (default)")
        # end if

        print("-")

        if answer.lower() == "yes" or answer.lower() == "y":
            log_loc = _join(defaults.app_data_path, "log.txt")
            print(will_start_info.format(log_loc))

            try:
                _start_cropping()
            except BaseException as base_exception:
                # _print_exc()  # Debug

                if isinstance(base_exception, SystemExit):
                    exit_code = base_exception.code
                else:
                    exit_code = 1

                print(stopped_info.format(log_loc), file=_stderr)
                _exit(exit_code)
            # end try

            print(completed_info.format(log_loc))
        else:  # elif answer.lower() == "no" or answer.lower() == "n" or answer is Others:
            print(aborted_info)
        # end if

        _exit(0)
    else:  # elif argv_copy_length > 0:
        print(too_many_args_info.format(argv_copy_length), file=_stderr)
        _exit(1)
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

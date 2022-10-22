""""widgets rand-crop" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import datetime
import os
import random
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
_clamp_int = utils.clamp_int
_deepcopy = copy.deepcopy
_exit = sys.exit
_flushlogs = utils.flushlogs
_format_exc = traceback.format_exc
_IO = typing.IO
_join = ospath.join
_load_json = utils.load_json
_logln = utils.logln
_logstr = utils.logstr
_makedirs = os.makedirs
_now = datetime.datetime.now
_pil_image = pil_image
# _print_exc = traceback.print_exc  # Debug
_rand_choice = random.choice
_randint = random.randint
_random_seed = random.seed
_split_text = ospath.splitext
_stderr = sys.stderr
_stdout = sys.stdout
_TimedInput = utils.TimedInput

# -

brief_usage = "widgets rand-crop"
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


def _parse_rand_seed(config):
    """Returns manual_seed, seed."""
    config: dict = config

    manual_seed = config["manual_seed"]

    if manual_seed is None:
        manual_seed = None
        _random_seed(manual_seed)
        seed = _randint(0, 2 ** 32 - 1)
    else:  # elif manual_seed is not None:
        manual_seed = int(manual_seed) % (2 ** 32 - 1)
        manual_seed = int(manual_seed)
        seed = manual_seed
    # end if

    return manual_seed, seed


def _parse_rand_flip(config):
    config: dict = config

    rand_flip = config["random_flipping"]
    rand_flip = bool(rand_flip)

    return rand_flip


def _parse_rand_rot(config):
    config: dict = config

    rand_rot_key = "random_rotating"

    if rand_rot_key in config:
        rand_rot = config[rand_rot_key]
        rand_rot = bool(rand_rot)
    else:
        rand_rot = False
    # end if

    return rand_rot


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

    if resize_res is None:
        resize_res = None
    else:  # elif resize_res is not None:
        resize_res = int(resize_res)

        if resize_res < 0:
            resize_res *= -1
    # end if

    return resize_res


def _parse_crop_quality(config):
    config: dict = config

    crop_quality_key = "crop_quality"

    if crop_quality_key in config:
        crop_quality = config[crop_quality_key]
        crop_quality = int(crop_quality)
        crop_quality = _clamp_int(crop_quality, 0, 100)
    else:
        crop_quality = 95
    # end if

    return crop_quality


def _parse_crop_count(config):
    config: dict = config

    crop_count = config["crop_count"]

    if crop_count is None:
        raise ValueError("Crop count cannot be None")

    crop_count = int(crop_count)

    if crop_count < 0:
        crop_count *= -1

    return crop_count


def _find_crop_name(image_name, pos_x, pos_y, crop_res, resize_res, flip, rot):
    image_name = str(image_name)
    pos_x = int(pos_x)
    pos_y = int(pos_y)
    crop_res = int(crop_res)

    if resize_res is None:
        resize_res = None
    else:  # elif resize_res is not None:
        resize_res = int(resize_res)
    # end if

    flip = str(flip)
    rot = str(rot)

    pos_tag = f"-At-{pos_x}-{pos_y}"
    crop_tag = f"-Crop-{crop_res}"

    if resize_res is None:
        resize_tag = ""
    else:  # elif resize_res is not None:
        resize_tag = f"-Resize-{resize_res}"
    # end if

    if flip != "":
        flip_tag = f"-Flip-{flip}"
    else:
        flip_tag = ""
    # end if

    if rot != "":
        rot_tag = f"-Rotation-{rot}"
    else:
        rot_tag = ""
    # end if

    now = _now()

    timestamp = str(
        f"-Time-{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
        f"{now.microsecond:06}"
    )

    ext = ".jpg"
    name = f"{image_name}{pos_tag}{crop_tag}{resize_tag}{flip_tag}{rot_tag}{timestamp}{ext}"
    return name


def _prep_and_crop(logs):
    global config_loc
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
    manual_seed, seed = _parse_rand_seed(config)
    _random_seed(seed)

    if manual_seed is None:
        _logln(logs, f"Auto random seed: {seed}")
    else:
        _logln(logs, f"Manual random seed: {seed}")
    # end if

    rand_flip = _parse_rand_flip(config)
    _logln(logs, f"Random flipping: {rand_flip}")

    if rand_flip:
        flips = ["", "x", "y", "xy"]
    else:
        flips = [""]
    # end if

    rand_rot = _parse_rand_rot(config)
    _logln(logs, f"Random rotating: {rand_rot}")

    if rand_rot:
        rots = ["", "180"]
    else:
        rots = [""]
    # end if

    crop_res = _parse_crop_res(config)
    _logln(logs, f"Crop resolution: {crop_res}")
    resize_res = _parse_resize_res(config)

    if resize_res is None:
        _logln(logs, "No resize, keep crop resolution")
    else:
        _logln(logs, f"Resize resolution: {resize_res}")
    # end if

    crop_quality = _parse_crop_quality(config)
    _logln(logs, f"Crop quality: {crop_quality}")
    crop_count = _parse_crop_count(config)
    _logln(logs, f"Crop count: {crop_count}")

    # Edit PIL max image pixels to avoid zip bomb detection false alarm
    max_width = 65535
    max_height = 65535
    max_pixels = max_width * max_height
    _pil_image.MAX_IMAGE_PIXELS = max_pixels
    _logln(logs, f"Tweaked PIL safety max pixels:  Width: {max_width}  Height: {max_height}  Total: {max_pixels}")

    # Read image
    image = _pil_image.open(image_loc)
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
        "Started random cropping\n"
        "-"
    )

    _logln(logs, info)

    # Start actual cropping
    total_count = 0
    width, height = image.size
    min_pos_x = 0
    max_pos_x = width - crop_res
    min_pos_y = 0
    max_pos_y = height - crop_res
    need_final_prog = False

    while total_count < crop_count:
        if (max_pos_x <= min_pos_x) or (max_pos_y <= min_pos_y):
            break

        pos_x = _randint(min_pos_x, max_pos_x)
        pos_y = _randint(min_pos_y, max_pos_y)

        flip = _rand_choice(flips)
        rot = _rand_choice(rots)

        box = (pos_x, pos_y, pos_x + crop_res, pos_y + crop_res)
        name = _find_crop_name(image_name, pos_x, pos_y, crop_res, resize_res, flip, rot)
        loc = _join(out_path, name)
        crop = image.crop(box)

        if resize_res is not None:
            crop = crop.resize(size=(resize_res, resize_res), resample=_pil_image.BICUBIC)

        if "x" in flip:
            crop = crop.transpose(_pil_image.FLIP_TOP_BOTTOM)

        if "y" in flip:
            crop = crop.transpose(_pil_image.FLIP_LEFT_RIGHT)

        if rot == "180":
            crop = crop.transpose(_pil_image.ROTATE_180)

        crop.save(loc, format="jpeg", quality=crop_quality)
        total_count += 1

        if total_count == 1 or total_count % 256 == 0:
            _logln(logs, f"Saved {total_count} cropped images")
            need_final_prog = False
        else:
            need_final_prog = True
    # end while

    if need_final_prog:
        _logln(logs, f"Saved {total_count} cropped images")

    info = str(
        "-\n"
        "Completed random cropping"
    )

    _logln(logs, info)
    _flushlogs(logs)


def start_cropping():
    """Starts the cropping."""
    global log_loc

    start_time = _now()
    log_file: _IO = open(log_loc, "a+")
    all_logs = [_stdout, log_file]
    err_logs = [_stderr, log_file]

    info = str(
        "AIDesign-Widgets random cropping\n"
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
        config_loc = _join(defaults.app_data_path, defaults.rand_crop_config_name)
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
                start_cropping()
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

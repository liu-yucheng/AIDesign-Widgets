""""widgets bulk-crop" command executable."""

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
_listdir = os.listdir
_load_json = utils.load_json
_logln = utils.logln
_logstr = utils.logstr
_makedirs = os.makedirs
_now = datetime.datetime.now
_pil_image = pil_image
_pil_image_open = pil_image.open
# _print_exc = traceback.print_exc  # Debug
_save_json = utils.save_json
_split_text = ospath.splitext
_stderr = sys.stderr
_stdout = sys.stdout
_TimedInput = utils.TimedInput

# -

brief_usage = "widgets bulk-crop <command> ..."
"""Brief usage."""

usage = fr"""

Usage: {brief_usage}
Help: widgets help

""".strip()
"""Usage."""

timeout = float(30)
"""Timeout in seconds."""
supported_crop_types = ["grid", "rand"]
"""Supported crop types"""

info = fr"""

"{brief_usage}", command "{{}}", command config:
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

Aborted the cropping process

""".strip()
"""Info to display when the user aborts the cropping process."""

too_few_args_info = fr"""

"{brief_usage}" gets too few arguments
Expects 1 arguments; Gets {{}} arguments
{usage}

""".strip()
"""Info to display when the executable gets too few arguments."""

too_many_args_info = fr"""

"{brief_usage}" gets too many arguments
Expects 1 arguments; Gets {{}} arguments
{usage}

""".strip()
"""Info to display when the executable gets too many arguments."""

unknown_crop_type_info = fr"""

"{brief_usage}" gets an unknown crop type: "{{}}"
Supported crop types: {supported_crop_types}
{usage}

""".strip()
"""Info to display when the executable gets an unknown crop type."""

argv_copy = None
"""Consumable copy of sys.argv."""
crop_type = None
"""Crop type."""
config_loc = None
"""Config location."""
log_loc = None
"""Log location."""


def _parse_in_path(config):
    config: dict = config

    in_path = config["bulk_input_path"]
    in_path = str(in_path)
    in_path = _abspath(in_path)

    return in_path


def _parse_out_path(config):
    config: dict = config

    out_path = config["bulk_output_path"]
    out_path = str(out_path)
    out_path = _abspath(out_path)

    return out_path


def _parse_grid_overrides(config):
    config: dict = config

    grid_overrides = config["grid_crop_config_overrides"]
    grid_overrides: dict

    return grid_overrides


def _parse_rand_overrides(config):
    config: dict = config

    rand_overrides = config["rand_crop_config_overrides"]
    rand_overrides: dict

    return rand_overrides


def _backup_config(config_loc, backup_loc):
    config_loc: str = config_loc
    backup_loc: str = backup_loc

    config = _load_json(config_loc)
    _save_json(config, backup_loc)


def _restore_config(config_loc, backup_loc):
    config_loc: str = config_loc
    backup_loc: str = backup_loc

    backup = _load_json(backup_loc)
    _save_json(backup, config_loc)
    _save_json(None, backup_loc)


def _override_config(config, overrides):
    config: dict = config
    overrides: dict = overrides

    for key in overrides:
        val = overrides[key]
        config[key] = val
    # end for


def _prep_and_crop(logs):
    global crop_type
    global config_loc
    global log_loc
    logs: list[_IO] = logs

    assert crop_type in supported_crop_types

    info = str(
        "Started preparation\n"
        "-"
    )

    _logln(logs, info)

    # Parse config

    config = _load_json(config_loc)
    in_path = _parse_in_path(config)
    _logln(logs, f"Bulk input path: {in_path}")
    out_path = _parse_out_path(config)
    _logln(logs, f"Bulk output path: {out_path}")

    if crop_type == "grid":
        cmd_config_overrides = _parse_grid_overrides(config)
    else:  # elif crop_type == "rand":
        cmd_config_overrides = _parse_rand_overrides(config)
    # end if

    # End
    # Prepare context
    # - Edit PIL max image pixels to avoid zip bomb detection false alarm

    max_width = 65535
    max_height = 65535
    max_pixels = max_width * max_height
    _pil_image.MAX_IMAGE_PIXELS = max_pixels
    _logln(logs, f"Tweaked PIL safety max pixels:  Width: {max_width}  Height: {max_height}  Total: {max_pixels}")

    # - End
    # - Filter the input path

    names = _listdir(in_path)
    in_locs = []

    for name in names:
        loc = _join(in_path, name)

        try:
            image = _pil_image_open(loc)
            image_format = image.format
        except Exception as _:
            image_format = None

        if image_format is not None:
            in_locs.append(loc)
    # end for

    in_locs_len = len(in_locs)
    _logln(logs, f"Bulk crop image count: {in_locs_len}")

    # - End

    # Ensure the output path
    _makedirs(out_path, exist_ok=True)

    if crop_type == "grid":
        from aidesign_widgets.exes import widgets_grid_crop
        cmd_config_loc = _join(defaults.app_data_path, defaults.grid_crop_config_name)
        cmd_backup_loc = _join(defaults.bulk_crop_backups_path, defaults.grid_crop_config_name)
        cmd_name = "widgets grid-crop"
        cmd_module = widgets_grid_crop
    else:  # elif crop_type == "rand":
        from aidesign_widgets.exes import widgets_rand_crop
        cmd_config_loc = _join(defaults.app_data_path, defaults.rand_crop_config_name)
        cmd_backup_loc = _join(defaults.bulk_crop_backups_path, defaults.rand_crop_config_name)
        cmd_name = "widgets rand-crop"
        cmd_module = widgets_rand_crop
    # end if

    # End

    info = str(
        "-\n"
        "Completed preparation"
    )

    _logln(logs, info)

    info = str(
        "Started bulk cropping\n"
        "-"
    )

    _logln(logs, info)
    in_loc_idx = 0

    for in_loc in in_locs:
        _logln(logs, f"- Started cropping image {in_loc_idx + 1} / {in_locs_len}")
        image_name = _split_text(_basename(in_loc))[0]

        if crop_type == "grid":
            out_name = f"GridCrop-{image_name}"
        else:  # elif crop_type == "rand":
            out_name = f"RandCrop-{image_name}"
        # end if

        out_subpath = _join(out_path, out_name)

        _backup_config(cmd_config_loc, cmd_backup_loc)
        cmd_config = _load_json(cmd_config_loc)
        _override_config(cmd_config, cmd_config_overrides)
        cmd_config["image_location"] = in_loc
        cmd_config["output_path"] = out_subpath
        _save_json(cmd_config, cmd_config_loc)

        cmd_module.argv_copy = argv_copy
        cmd_module.config_loc = cmd_config_loc
        cmd_module.log_loc = log_loc

        _logln(logs, f"---- The following will be the output from \"{cmd_name}\" ----")
        cmd_module.start_cropping()
        _logln(logs, f"---- The above has been the output from \"{cmd_name}\" ----")

        _restore_config(cmd_config_loc, cmd_backup_loc)
        _logln(logs, f"- Completed cropping image {in_loc_idx + 1} / {in_locs_len}")
        in_loc_idx += 1
    # end for

    info = str(
        "-\n"
        "Completed bulk cropping"
    )

    _logln(logs, info)
    _flush_logs(logs)


def _start_cropping():
    global crop_type
    global log_loc

    assert crop_type in supported_crop_types

    start_time = _now()
    log_file: _IO = open(log_loc, "a+")
    all_logs = [_stdout, log_file]
    err_logs = [_stderr, log_file]

    info = str(
        f"AIDesign-Widgets bulk {crop_type} cropping\n"
        f"-"
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
    global crop_type
    global config_loc
    global log_loc
    argv_copy_length = len(argv_copy)

    assert argv_copy_length >= 0

    if argv_copy_length < 1:
        print(too_few_args_info.format(argv_copy_length), file=_stderr)
        _exit(1)
    elif argv_copy_length == 1:
        crop_type = argv_copy.pop(0)
        crop_type = str(crop_type)

        if crop_type in supported_crop_types:
            config_loc = _join(defaults.app_data_path, defaults.bulk_crop_config_name)
            print(info.format(crop_type, config_loc))

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
                    # end if

                    print(stopped_info.format(log_loc), file=_stderr)
                    _exit(exit_code)
                # end try

                print(completed_info.format(log_loc))
            else:  # elif answer.lower() == "no" or answer.lower() == "n" or answer is Others:
                print(aborted_info)
            # end if

            _exit(0)
        else:  # elif crop_type not in supported_crop_types:
            print(unknown_crop_type_info.format(crop_type), file=_stderr)
            _exit(1)
        # end if
    else:  # elif argv_copy_length > 1:
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

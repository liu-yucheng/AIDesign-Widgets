""""widgets rand-crop" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

from PIL import Image
import copy
import datetime
import os
import random
import sys

from aidesign_widgets.libs import defaults
from aidesign_widgets.libs import utils

pil_image = Image

# Private attributes ...

_brief_usage = "widgets rand-crop"
_usage = fr"""Usage: {_brief_usage}
Help: widgets help"""
_timeout = 10

# ... Private attributes
# Nominal info strings ...

info = f"\"{_brief_usage}\":"r"""
{}
-
Please confirm the above config file contents
Do you want to continue? [ Y (Yes) | n (no) ]:"""fr""" < default: Yes, timeout: {_timeout} seconds >
"""
"""The primary info to display."""

aborted_cropping_info = r"""Aborted the image cropping process
"""
"""The info to display when the user aborts the cropping process."""

# ... Nominal info strings
# Error info strings ...

too_many_args_info = f"\"{_brief_usage}\""r""" gets too many arguments
Expects 0 arguments; Gets {} arguments"""fr"""
{_usage}
"""
"""The info to display when the executable gets too many arguments."""

# ... Error info strings
# Other public attributes ...

argv_copy = None
"""A consumable copy of sys.argv."""

config_loc = None
"""The config location."""

# ... Other public attributes


def _start_cropping():
    config = utils.load_json(config_loc)

    # read image location
    image_location = config["image_location"]
    if image_location is None:
        raise ValueError("image_location cannot be None")
    image_location = str(image_location)
    image_location = os.path.abspath(image_location)
    print(f"Image location: {image_location}")

    # read output path
    output_path = config["output_path"]
    if output_path is None:
        raise ValueError("output_path cannot be None")
    output_path = str(output_path)
    output_path = os.path.abspath(output_path)
    print(f"Output path: {output_path}")

    # read random seed
    manual_seed = config["manual_seed"]
    seed = manual_seed
    if manual_seed is None:
        random.seed(None)
        seed = random.randint(0, 2 ** 32 - 1)
    else:
        seed = int(manual_seed) % (2 ** 32 - 1)
    random.seed(seed)
    if manual_seed is None:
        print(f"Auto random seed: {seed}")
    else:
        print(f"Manual random seed: {seed}")

    # read random flipping switch
    random_flipping = config["random_flipping"]
    if random_flipping is None:
        random_flipping = False
    else:
        random_flipping = bool(random_flipping)
    print(f"Random flipping mode: {random_flipping}")

    # read crop resolution
    crop_resolution = config["crop_resolution"]
    if crop_resolution is None:
        raise ValueError("Crop resolution cannot be None")
    crop_resolution = int(crop_resolution)
    if crop_resolution <= 0:
        raise ValueError("crop_resolution needs to be > 0")
    print(f"Crop resolution: {crop_resolution}")

    # read resize resolution
    resize_resolution = config["resize_resolution"]
    if resize_resolution is not None:
        resize_resolution = int(resize_resolution)
        if resize_resolution <= 0:
            raise ValueError("resize_resolution (when set) needs to be > 0")
    if resize_resolution is None:
        print("No resize, keep crop resolution")
    else:
        print(f"Resize resolution: {resize_resolution}")

    # read crop count
    crop_count = config["crop_count"]
    if crop_count is None:
        raise ValueError("crop_count cannot be None")
    crop_count = int(crop_count)
    if crop_count < 0:
        raise ValueError("crop_count needs to be >= 0")
    print(f"Crop count: {crop_count}")

    # edit PIL max image pixels to avoid zip bomb detection false alarm
    pil_image.MAX_IMAGE_PIXELS = 65535 * 65535

    # read image
    image = pil_image.open(image_location)
    image_name = os.path.splitext(os.path.basename(image_location))[0]
    print("Completed loading image")
    print("-")

    # ensure output folder
    os.makedirs(output_path, exist_ok=True)

    # start actual cropping
    total_count = 0
    width, height = image.size
    min_pos_x = 0
    max_pos_x = width - crop_resolution
    min_pos_y = 0
    max_pos_y = height - crop_resolution

    print("Started image cropping")

    while total_count < crop_count:
        pos_x = random.randint(min_pos_x, max_pos_x)
        pos_y = random.randint(min_pos_y, max_pos_y)

        flip_around_x = False
        flip_around_y = False
        if random_flipping:
            flip_around_x = bool(random.randint(0, 1))
            flip_around_y = bool(random.randint(0, 1))

        box = (pos_x, pos_y, pos_x + crop_resolution, pos_y + crop_resolution)

        name = image_name
        name += f"-At-{pos_x}-{pos_y}-Crop-{crop_resolution}"
        if resize_resolution is not None:
            name += f"-Resize-{resize_resolution}"
        if flip_around_x or flip_around_y:
            name += "-FlippedAround-"
            if flip_around_x:
                name += "X"
            if flip_around_y:
                name += "Y"
        now = datetime.datetime.now()
        timestamp = f"-Time-{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"\
            f"{now.microsecond:06}"
        name += timestamp
        name += ".jpg"

        location = os.path.join(output_path, name)
        cropped = image.crop(box)
        if resize_resolution is not None:
            cropped = cropped.resize(size=(resize_resolution, resize_resolution), resample=pil_image.BICUBIC)
        if flip_around_x:
            cropped = cropped.transpose(pil_image.FLIP_TOP_BOTTOM)
        if flip_around_y:
            cropped = cropped.transpose(pil_image.FLIP_LEFT_RIGHT)
        cropped.save(location, quality=95)

        total_count += 1
        if total_count == 1 or total_count % 500 == 0:
            print(f"Saved {total_count} cropped images")

    # end while

    print(f"Saved {total_count} cropped images")
    print("Completed image cropping")


def run():
    """Runs the executable as a command."""
    global argv_copy
    global config_loc

    argv_copy_length = len(argv_copy)
    assert argv_copy_length >= 0
    if argv_copy_length == 0:
        config_loc = os.path.join(defaults.cmd_configs_path, defaults.rand_crop_config_name)
        print(info.format(config_loc), end="")

        timed_input = utils.TimedInput()
        answer = timed_input.take(_timeout)

        if answer is None:
            answer = "Yes"
            print(f"\n{answer} (timeout)\n", end="")
        elif len(answer) <= 0:
            answer = "Yes"
            print(f"{answer} (default)\n", end="")

        print("-\n", end="")
        if answer.lower() == "yes" or answer.lower() == "y":
            _start_cropping()
        # elif answer.lower() == "no" or answer.lower() == "n" or any other answer
        else:
            print(aborted_cropping_info, end="")

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

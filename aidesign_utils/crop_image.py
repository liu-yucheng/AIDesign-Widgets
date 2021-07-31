"""Executable for image cropping."""

from PIL import Image
import json
import os
import pathlib
import shutil

pil_image = Image
Path = pathlib.Path


def main():
    """Starts the executable."""
    curr_folder = str(Path(__file__).parent.resolve())
    config_location = str(Path(curr_folder + "/crop_image_config.json").absolute())
    default_config_location = str(Path(curr_folder + "/crop_image_default_config.json").absolute())
    config_file = None
    try:
        config_file = open(config_location, "r")
    except FileNotFoundError:
        shutil.copyfile(default_config_location, config_location)
        config_file = open(config_location, "r")
    config = json.load(config_file)
    print(f"Config location: {config_location}")

    image_location = config["image_location"]
    if image_location is None:
        raise ValueError("image_location cannot be None")
    output_path = config["output_path"]
    if output_path is None:
        raise ValueError("output_path cannot be None")
    crop_resolution = config["crop_resolution"]
    resize_resolution = config["resize_resolution"]
    start_index_x, start_index_y = config["start_index_x"], config["start_index_y"]
    crop_count_x, crop_count_y = config["crop_count_x"], config["crop_count_y"]

    pil_image.MAX_IMAGE_PIXELS = 60000 * 60000
    image = pil_image.open(image_location)
    image_name = os.path.splitext(os.path.basename(image_location))[0]
    print(f"Image location: {image_location}")

    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    Path(output_path).mkdir(exist_ok=True)
    print(f"Output path: {output_path}")

    if resize_resolution is not None:
        print(f"Image resize resolution: {resize_resolution}")
    else:
        print("Keep original image resolution")

    count_x, count_y, total_count = 0, 0, 0
    index_x, index_y = start_index_x, start_index_y
    width, height = image.size
    while count_y < crop_count_y and index_y + crop_resolution <= height:
        count_x = 0
        index_x = start_index_x
        while count_x < crop_count_x and index_x + crop_resolution <= width:
            box = (index_x, index_y, index_x + crop_resolution, index_y + crop_resolution)
            name = image_name
            name += f"_res-{crop_resolution}_at-{index_x}-{index_y}"
            if resize_resolution is not None:
                name += f"_resize-{resize_resolution}"
            name += ".jpg"
            location = str(Path(output_path + "/" + name).absolute())
            cropped_image = image.crop(box)
            if resize_resolution is not None:
                cropped_image = cropped_image.resize(
                    size=(resize_resolution, resize_resolution),
                    resample=pil_image.BICUBIC
                )
            cropped_image.save(location, quality=95)
            total_count += 1
            if total_count == 1 or total_count % 2000 == 0:
                print(f"Saved {total_count} cropped images")
            count_x += 1
            index_x += crop_resolution
        count_y += 1
        index_y += crop_resolution
    print(f"Saved {total_count} cropped images")
    print("Completed image cropping")


if __name__ == '__main__':
    main()

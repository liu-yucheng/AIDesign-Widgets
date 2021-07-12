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
    config_location = str(Path(curr_folder + "/crop_image_config.json").resolve())
    config_file = open(config_location, "r")
    config = json.load(config_file)

    image_location = config["image_location"]
    output_path = config["output_path"]
    image_resolution = config["image_resolution"]
    start_index_x, start_index_y = config["start_index_x"], config["start_index_y"]
    crop_count_x, crop_count_y = config["crop_count_x"], config["crop_count_y"]

    pil_image.MAX_IMAGE_PIXELS = 40000 * 30000
    image = pil_image.open(image_location)
    print(f"Image location: {image_location}")

    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    Path(output_path).mkdir(exist_ok=True)
    print(f"Output path: {output_path}")

    count_x, count_y, total_count = 0, 0, 0
    index_x, index_y = start_index_x, start_index_y
    width, height = image.size
    while count_y < crop_count_y and index_y + image_resolution <= height:
        count_x = 0
        index_x = start_index_x
        while count_x < crop_count_x and index_x + image_resolution <= width:
            box = (index_x, index_y, index_x + image_resolution, index_y + image_resolution)
            name = f"res-{image_resolution}_at-{index_x}-{index_y}.jpg"
            location = str(Path(output_path + "/" + name).absolute())
            cropped_image = image.crop(box)
            cropped_image.save(location, quality=95)
            total_count += 1
            if total_count == 1 or total_count % 2000 == 0:
                print(f"Saved {total_count} cropped images")
            count_x += 1
            index_x += image_resolution
        count_y += 1
        index_y += image_resolution
    print(f"Completed image cropping; Saved {total_count} cropped images")


if __name__ == '__main__':
    main()

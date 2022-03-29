<!---
Copyright 2022 Yucheng Liu. GNU GPL3 license.
GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
First added by username: liu-yucheng
Last updated by username: liu-yucheng
--->

# AIDesign-Widgets Application Data Folder

A folder that holds the subfolders and files that the AIDesign-Widgets application data needs.

# Documentation Files

Texts.

## `README.md`

This file itself.

# Configuration Files

Texts.

## `grid_crop_config.json`

Grid cropping configuration.

Configuration items. Type `dict[str, typing.Union[dict, list, str, bool, int, float, None]]`.

Configuration item descriptions are listed below.

- `image_location`. Type `str`.
- `output_path`. Type `str`.
- `crop_resolution`. Cropping resolution. Type `int`. Range [0, ).
- `resize_resolution`. Type `typing.Union[None, int]`. Range [0, ).
- `start_position_x`. X-axis start position. Type `int`. Range [0, ).
- `start_position_y`. Y-axis start position. Type `int`. Range [0, ).
- `max_crop_count_x`. X-axis maximum crop count. Type `typing.Union[None, int]`. Range [0, ).
- `max_crop_count_y`. Y-axis maximum crop count. Type `typing.Union[None, int]`. Range [0, ).

## `rand_crop_config.json`

Random cropping configuration.

Configuration items. Type `dict[str, typing.Union[dict, list, str, bool, int, float, None]]`.

Configuration item descriptions are listed below.

- `image_location`. Type `str`.
- `output_path`. Type `str`.
- `manual_seed`. Type `typing.Union[None, int]`. Range [0, ).
- `random_flipping`. Type `bool`.
- `crop_resolution`. Cropping resolution. Type `int`. Range [0, ).
- `resize_resolution`. Type `typing.Union[None, int]`. Range [0, ).
- `crop_count`. Type `int`. Range [0, ).

# Result Files

Texts.

## `log.txt`

**Note:** Not present until an AIDesign-Blend blending session completes.

Log.

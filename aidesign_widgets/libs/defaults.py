"""Default values.

Edit only when necessary.
"""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import pathlib

from os import path as ospath

_join = ospath.join
_Path = pathlib.Path

_libs_path = str(_Path(__file__).parent)
_main_package_path = str(_Path(_libs_path).parent)
_repo_path = str(_Path(_main_package_path).parent)

default_configs_path = _join(_repo_path, "aidesign_widgets_default_configs")
"""Default configs path."""

configs_path = _join(_repo_path, "aidesign_widgets_configs")
"""Configs path."""

grid_crop_config_loc = _join(configs_path, "grid_crop_config.json")
""""grid-crop" config location."""

rand_crop_config_loc = _join(configs_path, "rand_crop_config.json")
""""rand-crop" config location."""

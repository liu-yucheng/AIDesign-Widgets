"""Default values.

Edit only when necessary.
"""

import os

_curr_path = os.path.dirname(__file__)
_repo_path = os.path.abspath(os.path.join(_curr_path, ".."))

default_configs_path = os.path.join(_repo_path, "aidesign_widgets_default_configs")
"""Default configs path."""

configs_path = os.path.join(_repo_path, "aidesign_widgets_configs")
"""Configs path."""

grid_crop_config_loc = os.path.join(configs_path, "grid_crop_config.json")
""""grid-crop" config location."""

rand_crop_config_loc = os.path.join(configs_path, "rand_crop_config.json")
""""rand-crop" config location."""

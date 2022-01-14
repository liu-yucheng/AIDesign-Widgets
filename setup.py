"""Package setup executable.

To be called by a package manager (pip or conda or others).
NOT supposed to be executed directly (via python or py).
Tells the package manager the way to install the source directory as a package.
The "entry_points" parameter of the setup function specifies the function to call when the user enters the
    corresponding command via the command line.
"""

# Copyright (C) 2022 Yucheng Liu. GNU GPL Version 3.
# GNU GPL Version 3 copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by: liu-yucheng
# Last updated by: liu-yucheng

import setuptools
import shutil

from os import path as ospath

_copytree = shutil.copytree
_exists = ospath.exists
_find_packages = setuptools.find_packages
_setup = setuptools.setup


def main():
    _setup(
        name="aidesign-widgets",
        version="0.5.2",
        description="AIDesign Widget Application Collection",
        author="Yucheng Liu (From The AIDesign Team)",
        packages=_find_packages(),
        entry_points={
            "console_scripts": [
                "widgets = aidesign_widgets.exes.widgets:main"
            ]
        }  # ,
        # test_suite="tests"
    )

    # Initialize the configs with the defaults when necessary
    from aidesign_widgets.libs import defaults
    if not _exists(defaults.configs_path):
        _copytree(defaults.default_configs_path, defaults.configs_path)

    print(f"Configs ensured at: {defaults.configs_path}")
    print("Commands available: widgets")


if __name__ == '__main__':
    main()

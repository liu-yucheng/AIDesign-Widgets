"""Package setup executable.

To be called by a package manager (pip or conda or others).
NOT supposed to be executed directly (via python or py).
Tells the package manager the way to install the source directory as a package.
The "entry_points" parameter of the setup function specifies the function to call when the user enters the
    corresponding command via the command line.
"""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

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
        version="1.1.4",
        description="AIDesign Widget Application Collection",
        author="Yucheng Liu (From The AIDesign Team)",
        packages=_find_packages(),
        entry_points={
            "console_scripts": [
                "widgets = aidesign_widgets.exes.widgets:main"
            ]
        }  # ,
        # test_suite="aidesign_widgets.tests"
    )

    # Initialize the configs with the defaults when necessary
    from aidesign_widgets.libs import defaults

    if not _exists(defaults.app_data_path):
        _copytree(defaults.default_app_data_path, defaults.app_data_path)

    print(f"Configs ensured at: {defaults.app_data_path}")

    # Check main command availability
    from aidesign_widgets.exes import widgets as _
    print("Commands available: widgets")


if __name__ == '__main__':
    main()

"""Package setup script.

Inform the package manager (pip/conda/python) on how to install the source in the directory as a package. The
entry_points param of the setup function specifies the function to be called when the user enters the corresponding
command.
"""

import os
import setuptools
import shutil


def main():
    setuptools.setup(
        name="aidesign-widgets",
        version="0.4.1",
        description="AI Design project widgets.",
        author="The AI Design Team",
        packages=setuptools.find_packages(),
        entry_points={
            "console_scripts": [
                "widgets = aidesign_widgets.widgets:main"
            ]
        }
        # test_suite="tests"
    )

    # Initialize the configs with the defaults when necessary
    from aidesign_widgets import defaults
    if not os.path.exists(defaults.configs_path):
        shutil.copytree(defaults.default_configs_path, defaults.configs_path)

    print(f"Configs are at: {defaults.configs_path}")
    print("Commands available: widgets")


if __name__ == '__main__':
    main()

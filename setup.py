import setuptools
from src import settings

# Note on requirements.txt
# if we are using this setup.py file, we don't really need a requirements.txt file. Required modules can all be done from here, with some advantages.
# requirements.txt is for Apps being deployed on machines *I* (the original dev) control.
# Uses fixed version numbers
# Generated with pip freeze > requirements.txt

# Use the README for description
with open("README.md", "r") as fh:
    long_description = fh.read()


# Project Configuration
setuptools.setup(
    # Name on pip, what you pip-install
    name='labhack',
    url=settings.github,
    author=settings.author,
    author_email=settings.email,

    # 0.0.x - says that it is unstable.
    version=settings.version,

    description=settings.short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",

    python_requires='>=3.6',

    # Use this instead of package_dir) - looks simpler!
    # automatically discover all packages and subpackages.
    packages=setuptools.find_packages(),

    # Where the code is
    # package_dir={
        # '': '.',
        # '': 'components
        # '': 'src',
    # '},

    # list of the python code modules to install
    # If your project contains any single-file Python modules that aren’t part
    # of a package, set py_modules to a list of the names of the modules (minus
    # the .py extension) in order to make setuptools aware of them.

    # py_modules=["main"],

    # install_requires: For production dependencies
    # (Flask, Click, Numpy, Pandas)
    # Versions should be as relaxed as possible (>3.0, <4.0)
    install_requires = [
        "numpy ~=1.19",
        "tcod ~=11.19",
    ],

    # Development dependencies
    # For optional requirements (Pytest, Mock, Coverage.py, etc)
    # Versions should be as specific as possible.
    # people will need to install the 'dev' extras to develop upon this package.
    extras_require = {
        "dev": [
            "pytest>=3.8",
        ],
    },

    # Instead of manually handling images, manifest should do that...
    include_package_data=True,
    # data_files=[
        # ('images', ['dejavu10x10_gs_tc.png', 'menu_background.png'])
    # ],
)

# See https://pypi.org/classifiers
classifiers=[
    "Programming Language :: Python :: 3.8",
    # "Programming Language :: Python :: 3.9",
    "Development Status :: 2 - Pre-Alpha"
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: OS Independent",
    "Natural Language :: English",
],

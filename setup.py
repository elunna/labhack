from setuptools import setup


# Note on requirements.txt
# if we are using this setup.py file, we don't really need a requirements.txt file. Required modules can all be done from here, with some advantages.
# requirements.txt is for Apps being deployed on machines *I* (the original dev) control.
# Uses fixed version numbers
# Generated with pip freeze > requirements.txt

# Project Configuration
setup(
    # Name on pip, what you pip-install
    name='labhack',
    url="https://github.com/elunna/labhack",
    author="Erik Lunna",
    author_email="eslunna@gmail.com",)


    # 0.0.x - says that it is unstable.
    version='0.0.1',

    description='A super-science roguelike',

    # list of the python code modules to install
    py_modules=["helloworld"],

    # install_requires: For production dependencies
    # (Flask, Click, Numpy, Pandas)
    # Versions should be as relaxed as possible (>3.0, <4.0)

    # Development dependencies
    # For optional requirements (Pytest, Mock, Coverage.py, etc)
    # Versions should be as specific as possible.
    # people will need to install the 'dev' extras to develop upon this package.
    extras_require = {
        "dev": [
            "pytest>=3.y",
        ],
    },
    # Where the code is
    package_dir={'': '.', '': 'src', '': 'components'},
)

# See https://pypi.org/classifiers
classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Development Status :: 2 - Pre-Alpha"
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: OS Independent",
    "Natural Language :: English",
],

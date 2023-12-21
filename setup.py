#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def list_files(directory: str) -> list[str]:
    paths: list[str] = []
    for path, _, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    # print(path)
    return paths


long_description = open("README.MD", "r").read()

setup(
    name="dacutil",
    version="0.1.2",
    author="attapon.th",
    maintainer="attapon.th",
    maintainer_email="attapon.4work@gmial.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=open("requirements.txt").readlines(),
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    # entry_points={
    #     "console_scripts": ["dacutil=dacutil:main"],
    # },
    # py_modules=["dacutil"],
    package_data={"dacutil": list_files("dacutil")},
    # include_package_data=True,
)

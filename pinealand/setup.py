# -*- coding: utf-8 -*-
import os

import setuptools

try:
    with open(os.path.join(os.path.dirname(__file__), "../README.md"), "r", encoding='utf-8') as rd:
        long_description = rd.read()
except Exception as e:
    print("Warning: description info request from README.md failed.")
    print(e)
try:
    with open("requirements.txt", "r") as f:
        requirements = f.read().splitlines()
except Exception as e:
    print("reading requirements failed.")
    print(e)

setuptools.setup(
    name="Pinealand",
    version="0.1.0",
    maintainer='bittergreen from D&C squad',
    author="bittergreen",
    maintainer_email='bittergreen.wengqi@hotmail.com',
    description="Trying to understand the brain by coding it.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=requirements,
    url="https://github.com/bittergreen/pinealand",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7+",
        "Operating System :: OS Independent",
    ],
)
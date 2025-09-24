#!/usr/bin/env python3
"""
Setup script for PyAlarm.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="pyalarm",
    version="1.0.0",
    author="PyAlarm Contributors",
    author_email="",
    description="A cross-platform system tray time alarm application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyalarm",
    py_modules=["pyalarm"],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pyalarm=pyalarm:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Desktop Environment",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
    ],
    keywords="alarm, timer, system-tray, productivity, time-management",
    include_package_data=True,
    package_data={
        "": ["*.png", "*.wav", "*.md", "LICENSE"],
    },
    data_files=[
        ("", ["Active.png", "Inactive.png", "Paused.png", "Bell.wav", "HalfPast.wav"]),
    ],
    zip_safe=False,
)
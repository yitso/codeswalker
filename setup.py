# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="codeswalker",
    version="0.1.0",
    author="Yitso",
    author_email="yitso.zhang@gmail.com",
    description="CLI tool generating codebase context as AI-friendly Markdown docs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yitso/codeswalker",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements.splitlines(),
    entry_points={
        "console_scripts": [
            "codeswalker=codeswalker.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
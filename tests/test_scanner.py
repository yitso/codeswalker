# -*- coding: utf-8 -*-
import os
from pathlib import Path
import pytest
import git

from codeswalker.scanner import (
    generate_project_context,
    file_is_ignored_by_git,
    file_is_ignored_by_custom,
    get_git_context
)
from binaryornot.check import is_binary


def test_is_binary(tmp_path):
    # Create a text file.
    text_file = tmp_path / "test.txt"
    text_file.write_text("print('Hello world')")
    # Create a binary file.
    binary_file = tmp_path / "binary.dat"
    binary_file.write_bytes(b"\x00\x01\x02")
    assert not is_binary(str(text_file))
    assert is_binary(str(binary_file))


def test_generate_markdown_for_text_file(tmp_path):
    # Create a sample Python file.
    sample_py = tmp_path / "sample.py"
    sample_py.write_text("def foo():\n    return 42")
    md_output = generate_project_context(tmp_path)
    # Verify that the output includes the file and its content.
    assert "sample.py" in md_output
    assert "def foo():" in md_output
    # Check for the code block language.
    assert "```py" in md_output or "```python" in md_output


def test_generate_markdown_for_binary_file(tmp_path):
    # Create a binary file.
    binary_file = tmp_path / "image.png"
    binary_file.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00")
    md_output = generate_project_context(tmp_path)
    assert "> Binary file" in md_output


def test_custom_ignore(tmp_path):
    # Create files that should be subject to custom ignore rules.
    license_file = tmp_path / "LICENSE"
    license_file.write_text("MIT License")
    readme_file = tmp_path / "README.md"
    readme_file.write_text("README content")

    custom_rules = ["LICENSE", "*.md"]
    md_output = generate_project_context(tmp_path, custom_ignore_rules=custom_rules)
    # Ensure ignored files are not present.
    assert "LICENSE" not in md_output
    assert "README.md" not in md_output


def test_git_ignore(tmp_path):
    import git
    from codeswalker.scanner import generate_project_context

    # Initialize a Git repository in the temporary directory.
    repo = git.Repo.init(tmp_path)
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("ignored.txt")

    # Create the file that should be ignored (do not add it to the index).
    ignored_file = tmp_path / "ignored.txt"
    ignored_file.write_text("This file should be ignored by Git.")

    # Create a file that should be included.
    included_file = tmp_path / "included.txt"
    included_file.write_text("This file should be included.")

    # Add only the .gitignore and the included file to the index and commit.
    repo.index.add([str(gitignore), str(included_file)])
    repo.index.commit("Initial commit")

    md_output = generate_project_context(tmp_path)
    assert "included.txt" in md_output
    assert "ignored.txt" not in md_output

# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import pytest

from codeswalker.cli import main

def test_cli_run(tmp_path, monkeypatch):
    # Create a sample file in the temporary directory.
    sample_file = tmp_path / "sample.py"
    sample_file.write_text("def foo():\n    return 'bar'")

    # Change the working directory to the temporary path.
    monkeypatch.chdir(tmp_path)

    # Configure CLI arguments.
    test_args = ["codeswalker", str(tmp_path), "--output", "output.md", "--ignore", "LICENSE"]
    monkeypatch.setattr(sys, "argv", test_args)

    main()

    output_file = tmp_path / "output.md"
    assert output_file.exists()
    content = output_file.read_text()
    assert "sample.py" in content
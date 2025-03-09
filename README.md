# CodesWalker

CodesWalker is a simple CLI tool designed to quickly present your entire project code in a clean, structured Markdown format. Its primary goal is to let AI systems easily read and understand your codebase. The tool recursively scans project directories, preserves the folder structure, and marks binary files without displaying their content.

Features:

- Scans the complete project and organizes the code into one Markdown document.
- Maintains the original directory structure for easy navigation.
- Displays code files with basic formatting while flagging binary files.
- Usable both as a standalone CLI tool and as a Python module.
- Automatically respects Git ignore rules.

Installation:
For development, install CodesWalker in editable mode so changes take effect immediately:
```shell
pip install -e .
```

Usage:

As a CLI Tool:
```shell
codeswalker [directory] [--ignore <pattern_or_file>] [--output <output_file>]
```
For example, to scan the current directory and ignore LICENSE files:
```shell
codeswalker . --ignore LICENSE
```

As a Python Module:
```python
from codeswalker import generate_project_context

# Generate Markdown documentation for the specified directory with custom ignore rules
markdown_output = generate_project_context("path/to/directory", custom_ignore_rules=["LICENSE"])

# Write the output to a file
with open("output.md", "w", encoding="utf-8") as file:
    file.write(markdown_output)
```


Testing:
Ensure Pytest is installed:

```shell
pip install pytest
```

Then, from the project root directory, run:

```shell
pytest
```

License:
CodesWalker is released under the MIT License. See the LICENSE file for details.

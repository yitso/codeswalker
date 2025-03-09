# -*- coding: utf-8 -*-
import os
from pathlib import Path
from git import Repo, InvalidGitRepositoryError
from binaryornot.check import is_binary
import fnmatch

def get_git_context(directory):
    """
    Get the Git repository context starting from the specified directory.

    Args:
        directory (str): Directory to search for a Git repository.

    Returns:
        tuple: (Repo object, Git repository root) or (None, None) if not found.
    """
    try:
        repo = Repo(directory, search_parent_directories=True)
        return repo, repo.working_dir
    except InvalidGitRepositoryError:
        return None, None
    except Exception:
        return None, None

def file_is_ignored_by_git(repo, file_path):
    """
    Check if the file is ignored by Git based on .gitignore rules.

    Args:
        repo: Git repository object.
        file_path (str): Absolute file path.

    Returns:
        bool: True if file is ignored by Git, False otherwise.
    """
    if not repo:
        return False
    try:
        rel_path = os.path.relpath(file_path, repo.working_dir)
        ignored = repo.git.check_ignore(rel_path)
        return bool(ignored.strip())
    except Exception:
        return False

def file_is_ignored_by_custom(rel_path, custom_ignore_rules):
    """
    Check if the file should be ignored based on custom ignore patterns.

    Args:
        rel_path (str): File path relative to repository root.
        custom_ignore_rules (list): List of glob patterns.

    Returns:
        bool: True if file matches a custom ignore pattern, False otherwise.
    """
    for pattern in custom_ignore_rules:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False

def generate_markdown_for_file(file_path, rel_path):
    """
    Generate Markdown formatted content for a single file.

    Args:
        file_path (str): Absolute file path.
        rel_path (str): File path relative to repository root for display.

    Returns:
        str: Markdown formatted representation of the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        ext = Path(file_path).suffix[1:]
        language = ext if ext else "text"
        return f"## `{rel_path}`\n\n```{language}\n{content}\n```\n\n"
    except Exception as e:
        return f"## `{rel_path}`\n\n> Read error: {str(e)}\n\n"

def generate_project_context(root_directory=".", custom_ignore_rules=[]):
    """
    Generate Markdown documentation for all files in the codebase.

    The function recursively scans the provided directory,
    preserving the directory structure in the output. It outputs
    each file's content in a Markdown code block. Binary files are
    flagged, and files ignored by Git or custom ignore rules are omitted.

    Args:
        root_directory (str): The directory to scan.
        custom_ignore_rules (list): List of custom ignore patterns.

    Returns:
        str: Generated Markdown documentation.
    """
    output_lines = ["# PROJECT CONTEXT\n\n"]
    abs_root = os.path.abspath(root_directory)
    repo, git_root = get_git_context(abs_root)
    if git_root is None:
        git_root = abs_root

    for current_root, dirs, files in os.walk(abs_root):
        # Skip hidden directories.
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.startswith('.'):
                continue
            file_path = os.path.join(current_root, file)
            rel_path = os.path.relpath(file_path, git_root)

            if repo and file_is_ignored_by_git(repo, file_path):
                continue
            if file_is_ignored_by_custom(rel_path, custom_ignore_rules):
                continue

            if is_binary(str(file_path)):
                output_lines.append(f"## `{rel_path}`\n\n> Binary file\n\n")
            else:
                output_lines.append(generate_markdown_for_file(file_path, rel_path))
    return "".join(output_lines)

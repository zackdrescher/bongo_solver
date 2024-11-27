"""Utilities for Jupyter notebooks."""

import os
from pathlib import Path


def ensure_working_project_dir() -> None:
    """Ensure that the current working directory is the project root."""
    if Path.cwd().name == "notebooks":
        os.chdir(Path.cwd().parent)

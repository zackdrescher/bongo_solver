"""Bongo Solver package initialization file.

Sets up beartype for the entire package.
"""

from beartype.claw import beartype_this_package

beartype_this_package()

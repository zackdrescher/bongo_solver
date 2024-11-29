"""Bongo Solver package initialization file.

Sets up beartype for the entire package.
"""

from beartype import BeartypeConf, BeartypeStrategy, beartype
from beartype.claw import beartype_this_package

beartype_this_package()

# Dynamically create a new @nobeartype decorator disabling type-checking.
nobeartype = beartype(conf=BeartypeConf(strategy=BeartypeStrategy.O0))

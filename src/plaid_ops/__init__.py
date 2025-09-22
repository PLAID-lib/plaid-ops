"""Package that implement standardized operations for plaid datasets."""

try:
    from ._version import __version__
except ImportError:  # pragma: no cover
    __version__ = "None"

import os

os.environ["OMP_PROC_BIND"] = "spread"
os.environ["OMP_PLACES"] = "thread"

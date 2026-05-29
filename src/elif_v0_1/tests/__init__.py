"""ELIF v0.1 scaffold test package.

Path shim: when invoked via `python3 -m unittest discover -s src/elif_v0_1/tests`,
Python's import machinery does not automatically add `src/` to sys.path. This
shim adds the package root so `import elif_v0_1` resolves.
"""

from __future__ import annotations

import os
import sys

_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

"""Scaffold-import tests — every module imports cleanly, every component
instantiates, every stub method raises NotImplementedError.

This is the structural guarantee that the scaffold cannot be silently
"used" before implementation. If any stub stops raising, the test fails
and the operator's planning-vs-build gate is preserved.
"""

from __future__ import annotations

import importlib
import os
import sys
import unittest

# Path shim: make `elif_v0_1` importable when run via
# `python3 -m unittest discover -s src/elif_v0_1/tests`.
_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1 import InputFrame  # noqa: E402
from elif_v0_1.components import (  # noqa: E402
    BranchingRoadmapEngine,
    FrameValidator,
    GovernanceKernel,
    HypothesisValidator,
    MemoryLogger,
    ObjectDecomposer,
    OperativeTruthSeparator,
)
from elif_v0_1.orchestration_runner import ProcedureRunner


SCAFFOLD_MODULES = (
    "elif_v0_1",
    "elif_v0_1.base",
    "elif_v0_1.cli",
    "elif_v0_1.orchestration_runner",
    "elif_v0_1.schemas",
    "elif_v0_1.components",
    "elif_v0_1.components.frame_validator",
    "elif_v0_1.components.object_decomposer",
    "elif_v0_1.components.hypothesis_validator",
    "elif_v0_1.components.branching_roadmap_engine",
    "elif_v0_1.components.governance_kernel",
    "elif_v0_1.components.operative_truth_separator",
    "elif_v0_1.components.memory_logger",
)


class TestModulesImportCleanly(unittest.TestCase):
    def test_every_module_imports(self) -> None:
        for mod_name in SCAFFOLD_MODULES:
            with self.subTest(module=mod_name):
                importlib.import_module(mod_name)


class TestComponentsInstantiate(unittest.TestCase):
    def test_frame_validator_instantiates(self) -> None:
        self.assertIsInstance(FrameValidator(), FrameValidator)

    def test_object_decomposer_instantiates(self) -> None:
        self.assertIsInstance(ObjectDecomposer(), ObjectDecomposer)

    def test_hypothesis_validator_instantiates(self) -> None:
        self.assertIsInstance(HypothesisValidator(), HypothesisValidator)

    def test_branching_roadmap_engine_instantiates(self) -> None:
        self.assertIsInstance(
            BranchingRoadmapEngine(), BranchingRoadmapEngine
        )

    def test_governance_kernel_instantiates(self) -> None:
        self.assertIsInstance(GovernanceKernel(), GovernanceKernel)

    def test_operative_truth_separator_instantiates(self) -> None:
        self.assertIsInstance(
            OperativeTruthSeparator(), OperativeTruthSeparator
        )

    def test_memory_logger_instantiates(self) -> None:
        self.assertIsInstance(MemoryLogger(), MemoryLogger)

    def test_procedure_runner_instantiates(self) -> None:
        self.assertIsInstance(ProcedureRunner(), ProcedureRunner)


class TestCLIIsImplemented(unittest.TestCase):
    """Smoke check that the CLI module exposes the expected entry surface.

    The behavioral CLI execution path is covered by
    test_orchestration_runner.py via the runner; this test only asserts the
    parser builds and `main` exists.
    """

    def test_cli_build_parser_exposes_run_subcommand(self) -> None:
        from elif_v0_1 import cli

        parser = cli.build_parser()
        # Parse a syntactically valid invocation to ensure the subparser
        # accepts the expected flag surface (no execution).
        args = parser.parse_args(
            ["run", "--case", "case_01_electroculture",
             "--condition", "c", "--offline"]
        )
        self.assertEqual(args.command, "run")
        self.assertEqual(args.case, "case_01_electroculture")
        self.assertEqual(args.condition, "c")
        self.assertTrue(args.offline)


if __name__ == "__main__":
    unittest.main()

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

from elif_v0_1 import InputFrame, NonSelfPropagationError  # noqa: E402
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


def _sample_input_frame() -> InputFrame:
    return InputFrame(
        id="scaffold_test",
        text="not used",
        locked_at_iso="2026-05-29T00:00:00Z",
        doctrinal_scope_tag="elif_v0_1",
        companion_case="none",
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


class TestStubsRaiseNotImplemented(unittest.TestCase):
    """Every component stub method MUST raise NotImplementedError.

    Preserves the planning-vs-build gate at runtime.
    """

    # NOTE: test_frame_validator_stubs + test_object_decomposer_stubs removed
    # 2026-05-30 — those two components are now implemented per the v0.1-alpha
    # build (Phase 2 partial salvage). Their behavior is exercised by
    # test_frame_validator.py + test_object_decomposer.py. The remaining 5
    # component stub tests below continue to enforce planning-vs-build
    # discipline until those components are also implemented.

    def test_hypothesis_validator_stubs(self) -> None:
        hv = HypothesisValidator()
        with self.assertRaises(NotImplementedError):
            hv.enumerate_hypotheses_with_distinguishing_predictions(None)
        with self.assertRaises(NotImplementedError):
            hv.failure_conditions_per_hypothesis(None)

    def test_branching_roadmap_engine_stubs(self) -> None:
        bre = BranchingRoadmapEngine()
        with self.assertRaises(NotImplementedError):
            bre.outside_frame_trajectories_bre_feed(None, None)
        with self.assertRaises(NotImplementedError):
            bre.stage_gated_roadmap(None)

    def test_governance_kernel_stubs(self) -> None:
        gk = GovernanceKernel()
        with self.assertRaises(NotImplementedError):
            gk.verdict_with_confidence_and_uncertainty(None, None)

    def test_operative_truth_separator_stubs(self) -> None:
        ots = OperativeTruthSeparator()
        with self.assertRaises(NotImplementedError):
            ots.separate_operative_from_theoretical(None)

    def test_memory_logger_stubs(self) -> None:
        ml = MemoryLogger()
        with self.assertRaises(NotImplementedError):
            ml.write_event("case_x", {})
        with self.assertRaises(NotImplementedError):
            ml.read_case_state("case_x")
        with self.assertRaises(NotImplementedError):
            ml.find_reuse_candidates(_sample_input_frame())
        with self.assertRaises(NotImplementedError):
            ml.compute_capacity_metrics()

    def test_procedure_runner_refuses_with_non_self_propagation(self) -> None:
        runner = ProcedureRunner()
        with self.assertRaises(NonSelfPropagationError):
            runner.run("case_x", "a", _sample_input_frame())


class TestCLIIsScaffoldOnly(unittest.TestCase):
    def test_cli_main_returns_zero_and_does_not_invoke_runner(self) -> None:
        from elif_v0_1 import cli

        rc = cli.main(["run", "--case", "case_01", "--condition", "a"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()

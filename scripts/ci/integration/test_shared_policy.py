"""Offline consumer integration with exact frozen ci-actions source.

No action is vendored, activated or executed on GitHub. Structural graph tests use
the SHARED LIBRARY'S OWN adversarial fixture sentinels for route/lifecycle only;
they are not this consumer's installed helper, reviewer, receipt or admission.
No review, dispatch, bridge or status publication is simulated as a real result.
"""

import copy
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


CONSUMER = Path(__file__).resolve().parents[3]
REPOSITORY = "MinkTec/awesome_notifications"
LIBRARY_SHA = "afb382373b467b45216c7c08f5fe899c3c053471"
LIBRARY_TREE = "b866797a27ff7bcaec7f4bf8038fc5e59c19b817"
SHARED_REF = "feat/min-93-main-policy"
BINDING = {
    "repository": "MinkTec/ci-actions", "ref": SHARED_REF,
    "sha": LIBRARY_SHA, "tree": LIBRARY_TREE,
    "coordinated_override": "MIN-93-2026-11-01",
}
PRODUCT_COMMANDS = [
    "flutter clean", "flutter pub get", "flutter analyze --no-fatal-infos",
    "flutter test", "flutter test --coverage",
]


def git(*args, cwd=CONSUMER):
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    ).strip()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CanonicalMetadataSnapshot:
    """Read-only fixture using the consumer's actual checked-in master identity."""

    def __init__(self, branch="master"):
        self.branch = branch
        self.calls = []

    def call(self, method, path, body=None):
        self.calls.append((method, path))
        if method != "GET" or body is not None:
            raise AssertionError("Offline snapshot cannot dispatch/write a status")
        if path == "/repos/" + REPOSITORY:
            return {"default_branch": self.branch}
        if path == "/repos/" + REPOSITORY + "/git/ref/heads/master":
            return {"object": {"sha": MASTER_SHA}}
        if "/contents/.github/main-policy.json?ref=" + MASTER_SHA in path:
            raise mp.Rejected("offline snapshot: reviewed consumer policy absent")
        raise AssertionError("No fixture response for " + path)


class ConsumerIntegration(unittest.TestCase):
    def setUp(self):
        # A stray real API call is a hard test failure, never a fallback.
        self.no_network = patch.object(
            mp.GitHub, "call", side_effect=AssertionError("Real API forbidden")
        )
        self.no_network.start()
        self.addCleanup(self.no_network.stop)
        self.protocol = mp.Protocol(None, REPOSITORY, SHARED_REF)
        self.protocol.binding = mp.verify_library_binding(BINDING, SHARED_REF)
        self.protocol.shared = LIBRARY_SHA

    def structural_graph(self):
        # Reuse upstream test data instead of inventing an installed Infra API.
        policy, workflow = upstream.fixture()
        policy["jobs"] = {"build": policy["jobs"]["product"]}
        workflow["jobs"] = {"build": workflow["jobs"]["product"]}
        workflow["jobs"]["build"]["name"] = "build"
        policy.pop("reviewer_ids")  # No synthetic execution approval is used.
        policy["repository"] = REPOSITORY
        policy["definition_ref"] = "master"
        policy.update(shared_sha=LIBRARY_SHA, shared_ref=SHARED_REF,
                      shared_binding=copy.deepcopy(BINDING))
        steps = workflow["jobs"]["build"]["steps"]
        steps[0]["uses"] = mp.ACTION + SHARED_REF
        steps[2]["uses"] = "actions/checkout@a37ce9120846195fa4ece8f58b268e6043cb2f26"
        steps[3]["run"] = "\n".join(PRODUCT_COMMANDS)
        # The required artifact sentinel remains; this does NOT qualify Codecov.
        return policy, workflow

    def test_exact_frozen_full_tree_and_consumer_head(self):
        self.assertEqual(git("rev-parse", "HEAD", cwd=LIBRARY), LIBRARY_SHA)
        self.assertEqual(mp.source_tree(LIBRARY), LIBRARY_TREE)
        self.assertRegex(CONSUMER_SHA, r"^[0-9a-f]{40}$")

    def test_literal_development_binding_measures_real_loaded_tree(self):
        self.assertEqual(mp.verify_library_binding(BINDING, SHARED_REF), BINDING)

    def test_wrong_tree_rejected(self):
        with self.assertRaisesRegex(mp.Rejected, "loaded library tree differs"):
            mp.verify_library_binding({**BINDING, "tree": "0" * 40}, SHARED_REF)

    def test_wrong_library_repository_rejected(self):
        with self.assertRaisesRegex(mp.Rejected, "wrong shared library binding"):
            mp.verify_library_binding({**BINDING, "repository": REPOSITORY}, SHARED_REF)

    def test_unapproved_ref_and_missing_override_rejected(self):
        for ref, binding in [
            ("latest", BINDING),
            ("main", BINDING),
            (SHARED_REF, {**BINDING, "coordinated_override": ""}),
        ]:
            with self.subTest(ref=ref), self.assertRaises(mp.Rejected):
                mp.verify_library_binding(binding, ref)

    def test_changed_loaded_source_rejected_without_touching_frozen_tree(self):
        with tempfile.TemporaryDirectory(prefix="library-mutation-") as directory:
            target = Path(directory) / "library"
            shutil.copytree(LIBRARY, target,
                            ignore=shutil.ignore_patterns(".git", "__pycache__"))
            with (target / "README.md").open("a") as output:
                output.write("\nOffline adversarial fixture mutation.\n")
            with self.assertRaisesRegex(mp.Rejected, "loaded library tree differs"):
                mp.verify_library_binding(BINDING, SHARED_REF, target)
        self.assertEqual(mp.source_tree(LIBRARY), LIBRARY_TREE)

    def test_actual_legacy_product_commands_and_codecov_options_preserved(self):
        source = (CONSUMER / ".github/workflows/dart.yml").read_text()
        self.assertEqual(re.findall(r"^\s*run: (flutter[^\n]+)$", source, re.M),
                         PRODUCT_COMMANDS)
        for setting in ("directory: coverage", "fail_ci_if_error: false",
                        "token: ${{ secrets.CODECOV_TOKEN }}"):
            self.assertIn(setting, source)

    def test_actual_recipes_preserve_all_commands_with_only_concurrency_bound(self):
        result = subprocess.run(
            ["just", "--dry-run", "flutter-check"], cwd=CONSUMER,
            env={**os.environ, "FLUTTER": "flutter"}, capture_output=True,
            text=True, check=True, timeout=10,
        )
        commands = (result.stdout + result.stderr).strip().splitlines()
        self.assertEqual([c.removesuffix(" --concurrency=1") for c in commands],
                         PRODUCT_COMMANDS)

    def test_build_graph_structurally_accepts_real_commands_with_upstream_sentinels(self):
        policy, workflow = self.structural_graph()
        self.protocol.workflow(policy, workflow)
        self.assertNotIn("artifacts_required", policy["jobs"]["build"])

    def test_original_secret_bearing_codecov_upload_cannot_enter_test_stage(self):
        policy, workflow = self.structural_graph()
        workflow["jobs"]["build"]["steps"].insert(-2, {
            "id": "coverage_upload", "name": "coverage_upload",
            "uses": "codecov/codecov-action@ab904c41d6ece82784817410c45d8b8c02684457",
            "with": {"token": "${{ secrets.CODECOV_TOKEN }}",
                     "fail_ci_if_error": False, "directory": "coverage"},
        })
        with self.assertRaisesRegex(mp.Rejected, "test stage cannot inherit secrets"):
            self.protocol.workflow(policy, workflow)

    def test_required_coverage_artifact_role_cannot_be_silently_removed(self):
        policy, workflow = self.structural_graph()
        workflow["jobs"]["build"]["steps"] = [
            s for s in workflow["jobs"]["build"]["steps"] if s["id"] != "artifacts"
        ]
        with self.assertRaisesRegex(mp.Rejected, "missing mandatory lifecycle steps"):
            self.protocol.workflow(policy, workflow)

    def test_hosted_linux_is_not_a_product_fallback(self):
        policy, workflow = self.structural_graph()
        policy["jobs"]["build"]["runs_on"] = "ubuntu-latest"
        workflow["jobs"]["build"]["runs-on"] = "ubuntu-latest"
        with self.assertRaisesRegex(mp.Rejected, "missing explicit accepted group/selector"):
            self.protocol.workflow(policy, workflow)

    def test_online_pilot_label_does_not_become_ordinary_route(self):
        policy, workflow = self.structural_graph()
        policy["jobs"]["build"]["runs_on"]["labels"] = ["fixture-pilot-not-admitted"]
        with self.assertRaisesRegex(mp.Rejected, "not ordinary fresh routing"):
            self.protocol.workflow(policy, workflow)

    def test_cleanup_must_be_always_and_match_reviewed_invocation(self):
        for mutation, message in [("if", "cleanup must run always"),
                                  ("with", "wrong infra lifecycle invocation")]:
            policy, workflow = self.structural_graph()
            cleanup = workflow["jobs"]["build"]["steps"][-1]
            if mutation == "if":
                cleanup.pop("if")
            else:
                cleanup["with"] = {"unreviewed": True}
            with self.subTest(mutation=mutation), self.assertRaisesRegex(mp.Rejected, message):
                self.protocol.workflow(policy, workflow)

    def test_checkout_cannot_persist_credentials_or_choose_feature_ref(self):
        for key, value in [("persist-credentials", True), ("ref", "master")]:
            policy, workflow = self.structural_graph()
            workflow["jobs"]["build"]["steps"][2]["with"][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(mp.Rejected, "checkout must test only validated head"):
                self.protocol.workflow(policy, workflow)

    def test_changed_display_name_cannot_spoof_original_build_check(self):
        policy, workflow = self.structural_graph()
        workflow["jobs"]["build"]["name"] = "build (claimed success)"
        with self.assertRaisesRegex(mp.Rejected, "job name must match reviewed display name"):
            self.protocol.workflow(policy, workflow)

    def test_legacy_push_pr_graph_is_not_authoritative_dispatch_graph(self):
        policy, workflow = self.structural_graph()
        workflow["on"] = {"push": {}, "pull_request": {}}
        with self.assertRaisesRegex(mp.Rejected, "test graph must be dispatch-only"):
            self.protocol.workflow(policy, workflow)

    def test_expressions_in_action_uses_cannot_select_policy(self):
        policy, workflow = self.structural_graph()
        workflow["jobs"]["build"]["steps"][0]["uses"] = mp.ACTION + "${{ inputs.ref }}"
        with self.assertRaisesRegex(mp.Rejected, "missing trusted per-job runtime validator"):
            self.protocol.workflow(policy, workflow)

    def test_real_master_identity_is_read_from_snapshot_not_feature_caller(self):
        api = CanonicalMetadataSnapshot()
        protocol = mp.Protocol(api, REPOSITORY, SHARED_REF)
        self.assertEqual(protocol.main_sha(), MASTER_SHA)
        self.assertEqual(protocol.definition_ref, "master")
        self.assertEqual(api.calls[-1][1], "/repos/" + REPOSITORY + "/git/ref/heads/master")

    def test_dev_is_not_a_canonical_default_workaround(self):
        protocol = mp.Protocol(CanonicalMetadataSnapshot("dev"), REPOSITORY, SHARED_REF)
        with self.assertRaisesRegex(mp.Rejected, "unsupported canonical default branch"):
            protocol.main_sha()

    def test_actual_missing_master_policy_still_rejects_authoritative_execution(self):
        self.assertNotIn(".github/main-policy.json", git("ls-tree", "-r", "--name-only", MASTER_SHA).splitlines())
        api = CanonicalMetadataSnapshot()
        with self.assertRaisesRegex(mp.Rejected, "reviewed consumer policy absent"):
            mp.Protocol(api, REPOSITORY, SHARED_REF).policy()
        self.assertTrue(all(method == "GET" for method, _ in api.calls))

    def test_token_free_provenance_entrypoint_is_only_a_measurement(self):
        with tempfile.TemporaryDirectory(prefix="provenance-fixture-") as directory:
            output, summary = [Path(directory) / name for name in ("output", "summary")]
            # Numeric run/attempt below are fixture inputs, NOT real GitHub IDs.
            # Their synthetic URLs are discarded with this temporary directory.
            env = {
                "MAIN_POLICY_MODE": "provenance", "MAIN_POLICY_SHARED_REF": SHARED_REF,
                "MAIN_POLICY_LIBRARY_BINDING": json.dumps(BINDING),
                "GITHUB_SHA": CONSUMER_SHA, "GITHUB_WORKFLOW_SHA": CONSUMER_SHA,
                "GITHUB_WORKFLOW_REF": REPOSITORY + "/.github/workflows/dart.yml@refs/heads/" + CONSUMER_BRANCH,
                "GITHUB_REPOSITORY": REPOSITORY, "GITHUB_RUN_ID": "1",
                "GITHUB_RUN_ATTEMPT": "1", "GITHUB_JOB": "offline-fixture-not-a-job",
                "GITHUB_OUTPUT": str(output), "GITHUB_STEP_SUMMARY": str(summary),
            }
            with patch.dict(os.environ, env, clear=True), patch.object(
                mp, "GitHub", side_effect=AssertionError("Provenance must not construct API")
            ):
                mp.main()
            result = json.loads(output.read_text().removeprefix("provenance="))
            self.assertEqual(result["caller_sha"], CONSUMER_SHA)
            self.assertEqual(result["shared_binding"], BINDING)
            self.assertTrue(result["loaded_tree_verified"])
            for flag in ("authoritative_pr_validation", "ordinary_admission", "test_execution_claimed"):
                self.assertIs(result[flag], False)

    def test_provenance_does_not_allow_validate_without_token(self):
        with patch.dict(os.environ, {"MAIN_POLICY_MODE": "validate"}, clear=True):
            with self.assertRaisesRegex(mp.Rejected, "missing token"):
                mp.main()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: test_shared_policy.py EXACT_FROZEN_LIBRARY_WORKTREE")
    LIBRARY = Path(sys.argv[1]).resolve()
    if git("rev-parse", "HEAD", cwd=LIBRARY) != LIBRARY_SHA or git("status", "--porcelain", cwd=LIBRARY):
        raise SystemExit("Frozen library identity/cleanliness mismatch")
    CONSUMER_SHA = git("rev-parse", "HEAD")
    CONSUMER_BRANCH = git("branch", "--show-current")
    MASTER_SHA = git("rev-parse", "origin/master")
    mp = load("frozen_min93_protocol", LIBRARY / ".github/actions/main-policy/protocol.py")
    upstream = load("frozen_min93_fixture_data", LIBRARY / "tests/test_main_policy.py")
    if mp.source_tree(LIBRARY) != LIBRARY_TREE:
        raise SystemExit("Loaded frozen full tree mismatch")
    unittest.main(argv=[sys.argv[0]], verbosity=2)

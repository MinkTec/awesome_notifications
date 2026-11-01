"""Consumer graph preservation checks, not main-policy/runtime acceptance."""

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[3]


class ProductCommandsTest(unittest.TestCase):
    def test_legacy_product_graph_is_preserved(self):
        workflow = (ROOT / ".github/workflows/dart.yml").read_text()
        for command in (
            "flutter clean",
            "flutter pub get",
            "flutter analyze --no-fatal-infos",
            "flutter test",
            "flutter test --coverage",
        ):
            self.assertIn("run: " + command, workflow)
        self.assertIn("fail_ci_if_error: false", workflow)
        self.assertIn("directory: coverage", workflow)

    def test_recipes_execute_every_product_command(self):
        expected = {
            "flutter-clean": ["clean"],
            "flutter-dependencies": ["pub get"],
            "flutter-locked-dependencies": ["pub get --enforce-lockfile"],
            "flutter-analyze": ["analyze --no-fatal-infos"],
            "flutter-test": ["test --concurrency=1"],
            "flutter-coverage": ["test --coverage --concurrency=1"],
            "flutter-check": [
                "clean",
                "pub get",
                "analyze --no-fatal-infos",
                "test --concurrency=1",
                "test --coverage --concurrency=1",
            ],
        }
        # Dry run invokes no SDK and cannot upload coverage or mutate issues.
        for recipe, commands in expected.items():
            with self.subTest(recipe=recipe):
                result = subprocess.run(
                    ["just", "--dry-run", recipe], cwd=ROOT,
                    capture_output=True, text=True, check=True,
                )
                lines = (result.stdout + result.stderr).strip().splitlines()
                self.assertEqual(lines, ["flutter " + item for item in commands])

    def test_local_recipes_do_not_publish_or_install_toolchains(self):
        recipes = (ROOT / "Justfile").read_text()
        for forbidden in (
            "CODECOV_TOKEN", "GITHUB_TOKEN", "sudo ", "flutter upgrade",
            "sdkmanager", "actions/stale", "curl ", "docker ",
        ):
            self.assertNotIn(forbidden, recipes)


if __name__ == "__main__":
    unittest.main()

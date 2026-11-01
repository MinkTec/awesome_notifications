# Product commands from .github/workflows/dart.yml. Select an installed Flutter
# SDK/private writable state before running; these recipes install no toolchain.
flutter := env_var_or_default("FLUTTER", "flutter")
# The existing hosted Linux tests expect UTC, not the workstation's timezone.
export TZ := "UTC"

flutter-clean:
    {{flutter}} clean

flutter-dependencies:
    {{flutter}} pub get

# Qualification of the committed lock is separate from the legacy resolver.
flutter-locked-dependencies:
    {{flutter}} pub get --enforce-lockfile

flutter-analyze:
    {{flutter}} analyze --no-fatal-infos

flutter-test:
    {{flutter}} test --concurrency=1

flutter-coverage:
    {{flutter}} test --coverage --concurrency=1

flutter-check: flutter-clean flutter-dependencies flutter-analyze flutter-test flutter-coverage

ci-source-test:
    uv run --no-project python -B -m unittest discover -s scripts/ci/tests -v

# Explicit frozen external dependency; never installs/copies a private dispatcher.
ci-policy-fixtures shared_source:
    uv run --no-project --no-managed-python python -B scripts/ci/integration/test_shared_policy.py "{{shared_source}}"

# Product commands from .github/workflows/dart.yml. Select an installed Flutter
# SDK/private writable state before running; these recipes install no toolchain.
flutter := env_var_or_default("FLUTTER", "flutter")

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
    uv run --no-project python -m unittest discover -s scripts/ci/tests -v

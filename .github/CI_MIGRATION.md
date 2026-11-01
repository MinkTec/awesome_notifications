# MIN-93: awesome_notifications

## Evidence and authority

This is an **incomplete consumer migration increment**, not ordinary runner
admission or a production switch. Sole writer: `ses_e6a5fbf02ffe80NRWOBXohQvEE`,
branch `ci/min-93-fresh-awesome_notifications`, product/master base
`9db1b355e74f073025238c2484461c193bce859d`. Existing workflows remain intact until
the concrete integration edges below are resolved; no failing placeholder gate
or invented runner binding has been added.

Canonical policy self-read: `MinkTec/agent-skills`
`d25f5e5d570341bb72d748882c209a2266d43327`, minktec-ci **1.3.1**, skill blob
`0d182c1c07cdd440bb5d47d2e543aa6bd12b7ab3`, SHA256
`9d84ddf2a704fbb9ed70a51b4c3e9643dff8055bb0a658483caaf9fd91750d79`.
All six same-commit main-branch/shared-actions/fresh-routing/compatibility/
checklist/S3 references were read. The task-specific coordinated-development
override permits literal `MinkTec/ci-actions/...@feat/min-93-main-policy` only on
the isolated migration branch; eventual once-only `@main` integration is separate
from review, merge and production authority. No expression in `uses` is allowed.

## Complete current graph

Live API on 2026-11-01: public, non-archived, non-disabled fork; Actions enabled;
two active workflows, zero returned workflow runs, no open PRs. Default branch
is **master**, not main. Remote master equals the product base above; `dev` is
absent. No repository or nested AGENTS.md, reusable workflows, local composites,
matrix dimensions, services, release/signing/publish workflows, or Actions/S3
artifact writers/readers exist. Plugin support for Apple/Windows/Android in
`pubspec.yaml` is not evidence of corresponding CI lanes.

| Workflow / job | Complete direct and transitive steps | Capability / old route | Migration classification / proposed path |
| --- | --- | --- | --- |
| `dart.yml` / `build` | checkout v3 (Node16 main+post); flutter-action v2 composite (setup.sh metadata + SDK download/setup; conditional actions/cache v5 Flutter/pub writers+readers, both **off** for current inputs); configuration output; `flutter clean`; `flutter pub get`; `flutter analyze --no-fatal-infos`; `flutter test`; `flutter test --coverage`; codecov v3 (Node16, external uploader) | Linux x64 Flutter/Dart unit tests, package network, coverage; `ubuntu-latest`; no explicit timeout (GitHub default 360min) | Ordinary Linux: fresh-worker-v1 with verified installed Flutter/private SDK and caches, bounded resources, pre/postflight + cleanup. Preserve `build`, every command/test and Codecov semantics. `Justfile` captures actual product commands, bounds test concurrency to one, and adds a **separate** committed-lock qualifier. No platform exception. |
| `stale.yml` / `stale` | actions/stale v5 Node16 `dist/index.js`, no nested action/checkout; daily `40 8 * * *`; issues+PR write token; existing stale text/label unchanged | Metadata-only maintenance, `ubuntu-latest`; no explicit timeout (360min default) | Separate write-authority metadata path; never combine with PR checkout/tests. No claim that this is a hosted-only security/lint specialist exemption or that its current route is accepted. Exact authorized metadata placement still needed. Do not run the bot as a test (would mutate issues/PRs). |

Formatting remains commented out exactly as before (not a newly skipped check).
Codecov remains `directory: coverage`, token step-only, `fail_ci_if_error: false`:
the existing optional upload must not become an excuse to skip coverage tests.
No new S3 bucket, credentials or transfer is warranted for this graph. Codecov is
an external coverage service, **not** a GitHub/S3 build-artifact reader. Flutter
SDK caches are dependencies, not cross-job build outputs.

Transitive action definitions were read at these actual tag resolutions, not
asserted immutable historic executions (there are no returned consumer runs):

| Existing reference | Resolved source on inspection |
| --- | --- |
| `actions/checkout@v3` | `a37ce9120846195fa4ece8f58b268e6043cb2f26` |
| `subosito/flutter-action@v2` | `1a449444c387b1966244ae4d4f8c696479add0b2` |
| `codecov/codecov-action@v3` | `ab904c41d6ece82784817410c45d8b8c02684457` |
| `actions/stale@v5` | `f7176fd3007623b69d27091f9b9d4ab7995f0a06` |

## Exact integration edges (not global safety waiting)

1. The consumer is **public**, but `MinkTec/ci-actions` is **private** and its
   Actions access API reports `access_level: none`. Direct private-action `uses`
   cannot be assumed to work for this consumer. No PAT, source vendoring,
   cross-private Contents API from consumer GITHUB_TOKEN, visibility change or
   action-sharing change has been introduced. Coordinator/shared owner notified.
2. Restricted group 4's actual ten-repository allowlist **does not include this
   repository**. The provisional grant does not override actual access denial;
   do not copy pilot labels, expand membership or claim a fresh runner was used.
   There is no currently accepted worker/profile/resource/lifecycle binding here.
3. Initial shared source `73fbd9675efe1555a5e847042228a140460eeba1` required default
   branch **main**, incompatible with this repository's **master**. The shared
   owner subsequently published `afb382373b467b45216c7c08f5fe899c3c053471` with
   explicit `definition_ref: master`, bound to the actual API-verified default.
   Its exact docs/action/source were read: this source compatibility edge is
   resolved, **not yet qualified in consumer CI**. No branch rename or duplicate
   dispatcher. Existing `pull_request` CI is **not main-controlled exact-head CI**.
4. The shared strict test graph prohibits step secrets. Existing Codecov token
   upload therefore needs an actually supported separate trusted transfer path
   or reviewed compatible extension; it must not be placed in read-only PR tests
   or silently removed. No new artifact identity/keys or fabricated review.

Published infra docs were read at
`fc6820c5a74acae67a545867f9b814cc44211f7a`: `fresh-runners`,
`fresh-runner-registration`, `shared-ci-toolchains`; candidate registration is
not ordinary admission. Lifecycle invocation must be the **actual installed**
reviewed helper API (run/shell/env is supported), not an invented composite.
Private digest-bound accepted infra snapshot belongs on reviewed consumer policy
branch; source/registration/tool receipt are distinct from accepted admission.

## Test and integration evidence matrix

| Job / test path | Worker/profile/resources | PR / shared revision | Real run / result / cleanup |
| --- | --- | --- | --- |
| Legacy `Dart/build` | Historical hosted selector only; no observed worker | No open PR; no shared action in legacy graph | Runs API total_count=0; no run URL or accepted result to cite |
| `stale/stale` | No observed worker | No open PR; no shared action | Not executed: write-authority bot is not a safe product test |
| `just ci-source-test` | Local stdlib tests; no runner admission | Exact caller/source hashes recorded externally; no library execution | Source/fixture evidence only, not GitHub runtime qualification |
| `just flutter-*` | Provisional local private replica + reflink SDK, CPU100% / RAM3GiB / 128tasks / 600s; actual SDK below | Tested source/caller/legacy-definition commit `ec6e4e5dc3dbf63f65b89b043add1dfe05fecde1`; no PR; shared ref observation is **not executed library provenance** | UTC: analyze PASS, 399 tests PASS, 399 coverage tests PASS; committed lock FAIL65; private scratch removed; no Codecov upload or GitHub run/admission claim |
| Future real consumer validation | **Unavailable**: no authorized group/private-library/master binding | Reuse this branch and at most one necessary integration PR after common development; no serial pin PRs | Not run; no fake URL, receipt, review, runner/profile or cleanup result |

### Actual first provisional local product execution

Source/caller `957ec2bd7f4467665e62e5acc3f5529defdbd2dc`; legacy workflow blob
`396ddb9952da68a2cdb270fad48705b2a2428a34` (not a main-controlled definition).
Installed local Flutter **3.41.0**, Dart **3.11.0**, SDK source revision
`44a626f4f0027bc38a46dc68aed5964b05a83c18`; this is an existing workstation
installation, **not** a fresh profile receipt. No SDK/toolchain installation.

The user transient service read back effective cgroup `cpu.max=100000 100000`,
`memory.max=3221225472`, `pids.max=128`; 600s outer wall bound. Actual runtime
77.8s, memory peak 1.5GiB, swap zero. Source and SDK were private replicas;
SDK used `--reflink=always`, distinct inodes, no hardlink/full-copy fallback.
Product subprocesses received only explicit private HOME/pub/tmp/XDG/tool paths,
no inherited GitHub/Codecov/provider credentials. No Docker lease was needed.

* `flutter clean`: PASS.
* Committed lock qualification: **FAIL 65**, Flutter 3.41.0 requires changes to 17
  dependencies. Repository lock remains unchanged.
* Legacy `flutter pub get`: PASS, lock changes in the disposable replica only.
* Original `flutter analyze --no-fatal-infos`: PASS, 121 information-level issues.
* Tests and coverage: each **398 passed, 1 failed**, not green. The failure is
  `notification_schedule_test.dart` / `toString prints the respective inherited
  notification model`: host timezone CET differs from expected UTC. No test is
  skipped or rewritten. `Justfile` now explicitly exports UTC to preserve the
  existing hosted Linux environment rather than depend on the future worker's
  timezone; repeat validation is recorded separately.
* Coverage file was generated (digest recorded), not uploaded. Private scratch
  removed; four measured shared SDK identity files unchanged before/after. This
  is **not** a full immutable catalogue verification.

External cache receipt/logs: `min93-awesome_notifications-local-20261101T054535Z`.
Library dev ref observed before/after is exactly
`73fbd9675efe1555a5e847042228a140460eeba1`, no drift; no shared action was executed.
An offline constructor probe of the exact downloaded shared source also rejects
`feat/min-93-main-policy` with `invalid full commit SHA`, before any API call.
The owner's then-uncommitted working tree differed and was not attributed to that
probe. Later `afb382373b467b45216c7c08f5fe899c3c053471` adds the explicit mutable-ref
override and master compatibility; it was **not executed in that earlier run**.
Its observed source-CI run was queued at inspection:
https://github.com/MinkTec/ci-actions/actions/runs/41278320809 .
No consumer runtime/PR status or exact-head source-CI success is claimed.

### UTC repeat (separate result, not retroactive correction)

Source/caller/legacy-definition commit
`ec6e4e5dc3dbf63f65b89b043add1dfe05fecde1`, same product and workflow blob as above.
The only test-environment correction is explicit `TZ=UTC`; same installed SDK,
private cold dependency state, verified cgroup limits and command bounds.
Actual service runtime 75.8s, memory peak 1.3GiB, swap zero.

* Analysis PASS with original `--no-fatal-infos`.
* **399 tests PASS**, then **399 tests with coverage PASS**, no exclusions.
* Committed-lock qualifier still **FAIL65** (same 17 dependency changes); the
  overall diagnostic service deliberately exits **1**, not green. Legacy resolver
  PASS and changed only the replica's lock. No repository lock/product edits.
* Coverage SHA256 `7f58207b44d67c3bac6d447d56b539c161a6331fb61f426ca67a507b1e52fa88`;
  no upload. Scoped scratch cleanup succeeded, four measured SDK identity hashes
  unchanged. Both transient services are inactive; post-run `/proc` inspection
  found no command references to either invocation's private scratch/evidence path.

Receipt/logs: `min93-awesome_notifications-local-20261101T054755Z` in external cache.
Observed library ref **drifted during this run**:
`73fbd9675efe1555a5e847042228a140460eeba1` →
`afb382373b467b45216c7c08f5fe899c3c053471`. Neither library revision was executed
by the local Flutter commands. **No shared-library equivalence or consumer
integration acceptance** can be inferred from this run.

An additional **offline fixture-only** probe of exact downloaded `afb3823` source
confirms constructor acceptance of the scoped development ref and API-fixture
resolution of canonical master. It does not test private access, loaded-tree
binding, a reviewed policy, dispatch/bridge or actual runner admission.

Recurring product/source commands are in `Justfile`; execute in a private owned
replica for provisional local tests, never mutate the shared SDK. Keep lock changes
in that replica and report them rather than editing product locks to obtain green.
Local real tests and mocked preservation tests remain separate from main-defined
normal/stale/dev PR qualification and from final admission/production evidence.
No merge, deployment, release, signing or live bot operation is authorized.

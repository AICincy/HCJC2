# V1 Acquisition and Publication Audit

- Snapshot audited: `Sol-072026.zip`
- Audit date: 2026-07-20
- Tests observed before this audit: 465 passing, Ruff clean
- Scope: acquisition, state transitions, persistence, evidence, static build, repository storage, and deployment

## Executive finding

V1 contains several mature safeguards, especially atomic snapshot writes, degraded-roster guards, build-directory swapping, hash-chain verification, and alert deduplication. Those safeguards are embedded in a workflow that can still publish partial or stale state after failed acquisition. The repository also acts simultaneously as source tree, runtime database, evidence store, public artifact store, and deployment trigger.

V1 is therefore a working operational prototype with accumulated reliability patches. It is not an appropriate structural foundation for HCJC2.

## Findings

| ID | Severity | Finding | Evidence | V2 disposition |
|---|---|---|---|---|
| F13 | Critical | A failure after the list guard passes can replace `current.json` with a partial roster. | `scraper/sweep.py:560-566` marks the list result healthy; `scraper/sweep.py:643-675` re-raises failures but the `finally` block saves `current` whenever `roster_ok` remains true. A controlled reproduction persisted 7 of 60 records after a simulated detail-stage exception. | Replace with transactional staging and explicit promotion. |
| F14 | Critical | The workflow can continue to build and commit after the HCSO sweep fails. | `.github/workflows/sweep.yml:68-88` uses `continue-on-error: true`; build and commit continue at lines 134-165. | Replace with a consolidated publish-readiness gate. |
| F15 | High | Six independent stages use `continue-on-error` without a machine-readable run decision. | `.github/workflows/sweep.yml` contains six `continue-on-error: true` declarations. | Preserve best-effort source independence, but require per-source status and an explicit final decision. |
| F16 | High | Runtime data and generated site output are committed directly to `main`. | `.github/workflows/sweep.yml:146-165` stages `data/` and `docs/`, commits, rebases, and falls back to `git merge -X ours`. | Replace repository-as-runtime-storage with artifact storage and immutable manifests. |
| F17 | High | The evidence ledger mixes unrelated event classes and publicly retains custody identifiers. | `data/waf_block_log.json` contains 56,644 records: 56,634 `empty_photo_observed`, 5 `blocked`, and 5 `recovered`; 1,660 unique inmate IDs occur in the ledger. `web/pages.py:256-275` copies the ledger into the public site. | Split evidence streams, classify fields, and keep identity-bearing operational evidence outside the public data plane. |
| F18 | High | Each evidence append rewrites the complete ledger. | `scraper/store.py:119-139` loads the full JSON array and atomically rewrites it for every record. The current file is 16,904,736 bytes. The latest minute added 36 photo events, implying about 1.13 GiB of current-size read/write amplification. | Replace with append-capable immutable objects or segmented logs plus periodic signed manifests. |
| F19 | High | The public evidence documentation does not describe the dominant event type. | `web/templates/data.html:59` documents only `blocked` and `recovered`, while `empty_photo_observed` represents more than 99.9 percent of ledger records. | Require generated schema documentation from the same versioned contract used by writers. |
| F20 | High | Open-data feeds write directly to canonical files without atomic replacement or schema validation. | `scraper/cfs.py`, `scraper/cfs_pdi.py`, `scraper/shootings.py`, and `scraper/open_data_feeds.py` call `Path.write_text` directly. Row-collapse checks warn but do not block. | Stage, validate, checksum, and promote each feed independently. |
| F21 | Medium | Build and acquisition mutate durable data during rendering. | `web/build.py:290-300` calls `update_orc_offenses()` before rendering; `web/history.py` mutates `data/history.json` during build preparation. | Builds must be pure over an approved input manifest. |
| F22 | Medium | Build output is atomically swapped locally, but publication is only indirectly observed through branch hosting. | `web/build.py:306-364` correctly renders to a temporary directory and restores the old directory if promotion fails. The workflow then relies on branch-based GitHub Pages and a later staleness alarm. | Preserve atomic build behavior and add explicit deploy creation, verification, promotion, and rollback. |
| F23 | Medium | Alert failures are intentionally swallowed and issue existence is the main durable notification state. | `scraper/deploy_alert.py` and `scraper/freeze_alert.py` return dry-run status on API errors. | Record alert delivery attempts in the run manifest and support multiple channels. |
| F24 | Medium | The type-checking contract differs between local configuration and CI. | `pyproject.toml` specifies mypy 2.3.0 and includes tests/scripts; `.github/workflows/ci.yml` installs mypy 2.1.0 and runs only `mypy scraper web`. | Use one locked toolchain and one declared scope. |
| F25 | Medium | CI explicitly permits an empty-data build. | `.github/workflows/ci.yml` includes “Build site from empty data”; `web/build.py` can render an empty site when `current.json` is missing. | Empty public roster output requires an explicit bootstrap or maintenance mode, never an implicit production candidate. |

## Safeguards worth preserving as contracts

| Safeguard | V1 evidence | V2 contract |
|---|---|---|
| Atomic canonical file replacement | `scraper/store.py:53-63` | Canonical state changes only by atomic promotion of a validated candidate. |
| Degraded list-sweep guard | `scraper/sweep_guards.py:86-97` | Source collapse and excessive failures prevent roster promotion. |
| Detail extraction watchdog | `scraper/sweep_guards.py:99-140` | Material field-quality collapse blocks promotion. |
| Photo-prune safety threshold | `scraper/sweep_guards.py:143-177` | Destructive retention changes require an approved canonical roster and deletion budget. |
| Atomic static build swap | `web/build.py:306-364` | Rendering failure cannot replace the last validated application artifact. |
| Hash-chain verification | `scraper/store.py:144-160` | Evidence segments and manifests must be independently verifiable. |
| Alert deduplication | `scraper/freeze_alert.py`, `scraper/deploy_alert.py` | Repeated incidents update one incident record instead of creating unbounded duplicates. |

## Reproduction of F13

The audit replaced network calls with controlled functions:

1. Seeded a valid 60-person previous snapshot.
2. Returned a healthy 60-person list phase.
3. Added seven records to the in-memory `current` mapping.
4. Raised a simulated exception during detail acquisition.
5. Allowed `run()` to execute its `finally` block.

Observed result:

```json
{"persisted_count": 7, "missing_count": 53}
```

The workflow's `continue-on-error` setting means this partial snapshot can be consumed by the static build and committed after the failed acquisition step.

## Storage observations

| Path | Approximate size | Role conflict |
|---|---:|---|
| `data/` | 42 MiB | Runtime state, public inputs, evidence, photos, and retained feeds |
| `docs/` | 83 MiB | Generated site, duplicate data, duplicate photos, and deployment source |
| `data/waf_block_log.json` | 16.1 MiB | Mixed evidence and identity-bearing operational observations |
| `docs/data/waf_block_log.json` | 16.1 MiB | Public duplicate of the same ledger |
| `data/photos/` | 1,180 files | Canonical photo working set |
| `docs/photos/` | 1,180 files | Deployment duplicate |

The V2 design must classify artifacts before choosing storage. Git history is not a substitute for a retention policy, object manifest, or deployment system.

## Enterprise-readiness assessment

| Dimension | V1 rating | Basis |
|---|---|---|
| Functional behavior | Strong prototype | Broad tests and multiple operational guards |
| Failure isolation | Weak | Partial state can cross stage boundaries after failure |
| State management | Weak | Repository files serve as runtime database and deployment source |
| Reproducibility | Partial | Pinned runtime packages, but builds mutate data and tool scopes drift |
| Observability | Partial | Alerts and evidence exist, but no unified run manifest or stage state |
| Privacy and retention | Weak | Identity-bearing evidence is publicly retained without a separate policy |
| Deployment control | Weak | No explicit immutable deploy verification or controlled promotion |
| Maintainability | Weak to moderate | Safeguards exist, but critical logic and effects remain concentrated |

## Final disposition

- Preserve verified behavioral safeguards.
- Replace the orchestration, storage, publication, and evidence architecture.
- Do not copy the V1 workflow or repository layout into HCJC2.

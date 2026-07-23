# Data-Plane Security and Privacy Boundaries

## Trust zones

| Zone | Contains | Public access |
|---|---|---|
| Publisher | Source inputs, candidate state, validation results | None |
| Release bucket | Approved and retained private release artifacts | Worker only |
| Photo bucket | Current active-roster photos | Worker only |
| Control bucket | Pointer, leases, promotion and rollback receipts | Worker read, publisher write |
| Evidence bucket | Internal logs and evidentiary material | Restricted operators only |
| Worker gateway | Logical current public API | Public documented routes only |
| Netlify application | UI shell and documentation | Public |

## Credential separation

- Publisher token can write release and control objects but cannot change DNS or Worker code.
- Worker binding can read release, photo, and control objects but cannot write or delete them.
- Photo-deletion role can delete current photos and purge exact URLs but cannot alter release manifests.
- Infrastructure role controls buckets, locks, lifecycle, Worker deployment, DNS, and CORS.
- Evidence role cannot publish to public buckets.

## Required denials

The Worker must deny:

- direct release identifiers,
- bucket listing,
- internal manifests not selected by the pointer,
- evidence and telemetry prefixes,
- source captures,
- correlation review notes,
- unapproved fields,
- non-GET methods except CORS preflight.

## Retention conflict rule

A retention lock that prevents a required privacy deletion is a configuration defect. Photos and other current-only personal artifacts must never inherit evidence-retention locks.

## Logging rule

Public access logs must not contain full roster bodies, query-string names, source credentials, or photo bytes. Query parameters used for name searches should be processed client side or normalized so raw personal search terms are not retained in edge logs.

## Incident classes

- unauthorized old-release access,
- current-photo deletion failure,
- pointer tampering,
- manifest mismatch,
- CORS expansion,
- credential overreach,
- bucket accidentally made public,
- Worker fail-open configuration,
- evidence copied into public release,
- cost or request-limit exhaustion.

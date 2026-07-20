# Privacy and Data Invariants

These invariants are release-blocking requirements.

1. Publish only records present in the current official custody roster, subject to documented source lag.
2. Remove public booking photos when the corresponding person leaves the active roster.
3. Prevent indexing of individual custody pages and names by search engines.
4. Do not create unique social-preview cards for individual custody records.
5. Do not publish private correlation outputs that associate custody identities with unrelated calls, incidents, locations, or complaints.
6. Keep internal operational logs, evidentiary records, request records, secrets, and personal correspondence outside the public build.
7. Apply explicit retention policies to every artifact containing personal data.
8. Preserve the presumption-of-innocence notice and the prohibition on consumer-reporting use.
9. Provide correction, sealing, and removal processes without charging a fee.
10. Require a privacy review before adding a new field, feed, index, export, preview deployment, or third-party integration.

## Required controls

- public/private path allowlists
- build-time leak detection
- schema-based field classification
- preview-deployment protection or exclusion
- retention enforcement tests
- robots and response-header verification
- checksum and provenance generation

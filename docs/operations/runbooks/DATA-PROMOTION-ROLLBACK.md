# Data Promotion and Rollback Runbook

## Promotion preconditions

- Acquisition run is complete.
- Candidate state passed all gates.
- Correlation and taxonomy outputs passed their contracts.
- Public/private allowlist scan passed.
- Manifest and object digests were generated.
- No conflicting publisher lease exists.

## Promotion procedure

1. Create a unique release identifier.
2. Upload release artifacts to a new immutable prefix.
3. Read every uploaded object back by API.
4. Verify size, content type, digest, and manifest membership.
5. Run schema and privacy scans against the uploaded release.
6. Write a promotion candidate receipt.
7. Read the existing pointer and capture its conditional-write token.
8. Replace the pointer only if the token still matches.
9. Read the pointer back and verify its digest.
10. Purge the logical public manifest, status, roster, activity, correlation, and affected feed URLs.
11. Probe the public routes and compare release headers to the pointer.
12. Record a successful promotion receipt.
13. Release the publisher lease.

## Rollback triggers

- Public manifest digest mismatch.
- Missing current artifact.
- Schema failure discovered after promotion.
- Material privacy leak.
- Material roster completeness regression.
- Worker routing defect.
- Incorrect correlation publication.
- Operator-declared incident.

## Rollback procedure

1. Select a prior release that has a validated promotion receipt and remains inside retention.
2. Confirm that the release still passes current privacy constraints.
3. Update the pointer conditionally to that release.
4. Purge logical public data routes.
5. Verify release and manifest headers on all critical routes.
6. Record the rollback reason, authority, prior release, replacement release, and verification results.
7. Place the rejected release on hold for investigation.

## Photo removal procedure

1. Confirm that the person is no longer present in the approved active roster.
2. Determine the exact public photo identifier.
3. Delete the photo object from the current-photo bucket.
4. Purge the exact public URL.
5. Verify the private origin returns no object.
6. Verify the public gateway returns `404` from at least two independent requests.
7. Confirm the current roster and manifest contain no photo reference.
8. Record a deletion receipt containing only identifiers, timestamps, hashes, and verification results.

## Emergency controls

- Promotion kill switch prevents pointer writes.
- Gateway maintenance mode serves a minimal status response, not stale unverified data.
- Secrets can be rotated without changing public URLs.
- A manual rollback requires two recorded approvals once more than one maintainer exists.

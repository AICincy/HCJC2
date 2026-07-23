# Deployment Control Runbook

## Application release

### Preconditions

- source commit is immutable
- dependency lock verifies
- synthetic fixture set is approved
- quality gates pass
- no real custody data exists in the application artifact
- prior production deploy ID and retained artifact bundle are known

### Procedure

1. Build the application artifact.
2. Generate an artifact manifest and SHA-256 checksums.
3. Create an unpublished Netlify deploy.
4. Record the deploy ID and immutable permalink.
5. Verify:
   - expected routes
   - 404 behavior
   - security headers
   - noindex policy for non-production URLs
   - CSP behavior
   - accessibility smoke tests
   - asset and manifest hashes
   - absence of prohibited files
6. Promote only the verified deploy.
7. Verify the production domain independently.
8. Finalize the release manifest.
9. Deliver notifications.

### Rollback

Rollback authority may:

1. lock auto publishing if enabled
2. publish the last validated retained deploy
3. verify the production domain and headers
4. restore the prior application-release pointer in the HCJC2 manifest
5. open or update the incident record
6. preserve the failed deploy and logs until review completes

If the prior Netlify deploy has expired, recreate it from the retained application artifact bundle and verify before promotion.

## Data publication

### Preconditions

- acquisition run reached `validated`
- candidate artifacts use approved schemas
- public allowlist passes
- prohibited-field scan passes
- retention and takedown filters pass
- checksums and source provenance exist

### Procedure

1. Upload artifacts under a new immutable version prefix.
2. Upload the version manifest last.
3. Read every required artifact back from the public edge.
4. Verify size, checksum, schema, freshness, and cache headers.
5. Atomically update the canonical manifest pointer with compare-and-swap.
6. Verify the canonical URL resolves to the new version.
7. Retain the prior canonical pointer for rollback.
8. Finalize the run manifest and notifications.

### Hold conditions

Do not promote when:

- required source acquisition failed
- candidate roster is partial
- identifier-set or count gates fail
- schema validation fails
- takedown processing fails
- photo deletion exceeds the approved budget
- artifact read-back differs from the manifest
- a newer run has already promoted

### Data rollback

1. Compare current pointer with the failed run's promoted version.
2. Atomically restore the prior approved pointer.
3. Verify public read-back.
4. preserve the failed version for investigation, subject to privacy and retention controls
5. issue a correction event when public consumers may have observed incorrect data

## Alert delivery

Every run records delivery status for each configured channel. Alert failure does not change the underlying publication decision, but it prevents the run from being marked operationally complete until the failed delivery is recorded and escalated through a fallback channel.

# V1 Disposition Policy

V1 remains the operational baseline and rollback target during HCJC2 development.

## Disposition labels

| Label | Meaning |
|---|---|
| Preserve | Correct behavior that becomes a V2 contract |
| Redesign | Requirement remains but implementation must change |
| Replace | Component should not be carried forward |
| Retire | Feature or file has no V2 purpose |
| Verify | Intent or correctness remains uncertain |
| Isolate | Historical, private, or evidentiary material must remain separate |

## Audit questions

For every authored V1 file or subsystem, determine:

- What requirement does it implement?
- Is that requirement still valid?
- What inputs, outputs, side effects, and failure modes exist?
- Which tests prove behavior?
- Which behavior is accidental?
- What privacy or legal boundary applies?
- Which disposition label applies?

## Migration rule

HCJC2 may reuse verified facts, schemas, fixtures, and legal requirements. It must not copy V1 implementation solely because it already exists.

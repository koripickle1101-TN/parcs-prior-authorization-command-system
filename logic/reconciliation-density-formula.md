# Reconciliation Density Formula

## PARCS 2.0

**Created by Kori Pickle**

## Purpose

Reconciliation density measures how much manual repair work is required to keep authorization cases moving. This metric exposes hidden labor that may not appear in basic productivity reports.

## Formula

```text
Reconciliation Density = Total Manual Repair Events / Total Authorization Cases
```

## Example

```text
40 manual repair events / 100 authorization cases = 0.40 reconciliation density
```

## Interpretation

| Reconciliation Density | Meaning |
|---:|---|
| 0.00-0.10 | Strong workflow stability |
| 0.11-0.25 | Moderate manual dependency |
| 0.26-0.50 | High hidden labor |
| 0.51+ | Critical workflow fragility |

## Manual Repair Events to Count

- Manual payer portal checks
- Manual eligibility verification
- Demographic corrections
- Documentation chasing
- Payer phone calls
- Email follow-ups
- Case rerouting
- Status corrections
- Manual overrides
- Resubmissions

## Control Rule

If reconciliation density rises, the workflow is becoming less reliable even if cases are still getting completed.

---

Created by Kori Pickle

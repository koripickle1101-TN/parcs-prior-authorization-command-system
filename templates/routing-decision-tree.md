# Routing Decision Tree

## PARCS 2.0

**Created by Kori Pickle**

## Purpose

This routing decision tree reduces confusion by assigning every exception a next step, owner, and deadline.

## Routing Logic

| Condition | Route To | Required Action |
|---|---|---|
| Eligibility conflict | Front-end verification owner | Reconcile payer and registration record |
| Demographics conflict | Registration correction owner | Correct patient record before submission |
| Documentation missing | Clinical documentation owner | Request missing support |
| Clinical note unsigned | Provider or clinical team | Obtain signed note |
| Payer response overdue | Authorization escalation owner | Escalate based on payer response threshold |
| Service date within 3 business days and authorization pending | Urgent pre-service review | Decide escalation, patient communication, or scheduling review |
| Authorization denied | Denial prevention review | Review denial reason and next action |
| Case has no assigned owner | Authorization workqueue lead | Assign owner same day |
| Duplicate tracking discovered | Workflow integrity review | Consolidate updates into source-of-truth tracker |

## Control Rule

Every exception must have a next step, an owner, and a deadline.

---

Created by Kori Pickle

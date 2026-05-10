# PARCS 2.0 Dashboard Wireframe

## Prior Authorization Reliability Command System

**Created by Kori Pickle**

## Brand Identity

| Brand Element | Standard |
|---|---|
| Background | White `#FFFFFF` |
| Primary text | Black `#111111` |
| Secondary text | Charcoal `#333333` |
| Accent | Tennessee Orange `#FF8200` |
| Structure | Warm Gray `#E8E2DC` |
| Layout style | Executive, editorial, high-whitespace, operational intelligence |

---

## Dashboard Purpose

The PARCS dashboard is designed to show which prior authorization cases are most likely to break, why they are at risk, who owns the next action, and what downstream damage may occur if the risk is not resolved.

This dashboard should not feel like a generic task board. It should feel like a healthcare operations command view.

---

## Top Header

```text
PARCS 2.0
Prior Authorization Reliability Command System
```

Subtitle:

```text
Predicting, prioritizing, and preventing authorization workflow failure before it becomes patient access disruption or denial risk.
```

Accent treatment:

- Thin Tennessee Orange `#FF8200` divider below title
- White background
- Black title text
- Charcoal subtitle
- Footer: Created by Kori Pickle

---

## Executive KPI Row

| KPI Card | Purpose | Brand Treatment |
|---|---|---|
| Total Active Cases | Shows volume currently under management | White card, warm-gray border |
| Critical Risk Cases | Shows immediate workflow threat | Tennessee Orange risk marker |
| Red Patient Access Risk | Shows cases that may disrupt care | Tennessee Orange label |
| Average Risk Score | Shows overall instability | Black number, charcoal label |
| Reconciliation Density | Shows hidden manual labor | Orange accent if above threshold |
| Clean Claim Readiness Rate | Shows downstream claim protection | Black number, warm-gray structure |

---

## Main Dashboard Sections

### 1. Risk Triage Queue

| Case ID | Service Date | Payer | Risk Score | Risk Level | Owner | Next Action |
|---|---|---|---:|---|---|---|
| PARCS-003 | 2026-05-16 | Example Plan C | 70 | Critical | Workqueue Lead | Immediate escalation |
| PARCS-005 | 2026-05-17 | Example Plan B | 62 | Critical | Authorization Specialist | Documentation review |
| PARCS-002 | 2026-05-18 | Example Plan B | 45 | High | Authorization Specialist | Obtain signed note |

Purpose:

```text
Show the highest-risk cases first so staff are not relying on memory or inbox order.
```

---

### 2. Trust Failure Events

| Event Type | Count | Operational Meaning |
|---|---:|---|
| Eligibility conflict | 6 | Staff cannot trust coverage data |
| Clinical note timing issue | 5 | Documentation readiness is weak |
| Routing mismatch | 3 | Ownership logic needs tightening |
| Payer status conflict | 2 | Source-of-truth confidence is weakening |

Purpose:

```text
Convert staff frustration into operational evidence.
```

---

### 3. Operational Drift Monitor

| Drift Signal | Current Status | Risk |
|---|---|---|
| Cases pending over threshold | 8 | High |
| Documentation readiness below target | 82 percent | Moderate |
| Payer response variance | +2.4 days | Moderate |
| Shift handoff gaps | 3 | Moderate |

Purpose:

```text
Detect small workflow inconsistencies before they compound into backlog.
```

---

### 4. Reconciliation Density Panel

Formula:

```text
Reconciliation Density = Total Manual Repair Events / Total Authorization Cases
```

| Metric | Value |
|---|---:|
| Manual repair events | 40 |
| Total authorization cases | 100 |
| Reconciliation density | 0.40 |
| Interpretation | High hidden labor |

Purpose:

```text
Expose the manual work keeping the workflow alive.
```

---

### 5. Clean Claim Readiness Gate

| Readiness Check | Pass Rate |
|---|---:|
| Authorization number captured | 96 percent |
| Authorized service matches scheduled service | 94 percent |
| Date range covers service date | 92 percent |
| Eligibility verified for date of service | 90 percent |
| Documentation supports medical necessity | 86 percent |

Purpose:

```text
Connect authorization approval to downstream claim readiness.
```

---

## Footer

```text
Created by Kori Pickle
```

Optional visual signature line:

```text
Kori Pickle
```

---

## Executive Design Rule

The dashboard should answer six questions:

```text
What is breaking?
Why is it breaking?
Who owns the fix?
How urgent is it?
What downstream risk does it create?
What metric proves improvement?
```

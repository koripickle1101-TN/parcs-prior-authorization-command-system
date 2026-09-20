# PARCS — Prior Authorization Command System

I built PARCS as a student-developed healthcare operations project to study a question that matters to me from both the patient side and the operational side: **what happens when a prior authorization looks like one task, but the real problem started earlier somewhere else in the workflow?**

As I work toward my Bachelor's of Science degree in Healthcare Administration at the University of Phoenix, I am especially interested in prior authorization because the patient usually experiences the delay without seeing the administrative chain behind it. A missing note, unclear requirement, unresolved eligibility issue, late payer follow-up, or ownership gap can eventually become another phone call, a rescheduled service, uncertainty about whether care can move forward, or a denial that is difficult to understand.

PARCS gives me a structured way to practice tracing those downstream problems back to the first point where the authorization workflow may have lost control.

## Why I Built PARCS

I do not have formal healthcare operations employment experience yet, so I use simulated projects to turn coursework and independent study into visible practice.

With PARCS, I wanted to move beyond the idea that prior authorization is simply a status to check. I use the project to study the relationships between:

- eligibility and benefit readiness,
- authorization requirements,
- documentation completeness,
- medical-necessity support,
- payer follow-up,
- aging and deadlines,
- escalation ownership,
- service clearance,
- downstream claim readiness,
- the patient impact when those pieces do not stay connected,
- pre-service versus post-service authorization exception handling,
- payer/program source review before selecting an exception path,
- active-movement tracking after service,
- submission, receipt/status, determination, downstream action, and closure verification.

The question I keep coming back to is:

> **Where did the authorization workflow first lose control?**

## What PARCS Studies

PARCS uses synthetic cases to model prior authorization workflow risks such as:

- an authorization requirement not being identified early,
- an authorization not being started,
- a pending request getting too close to the service date,
- incomplete or missing documentation,
- weak medical-necessity support,
- eligibility problems that affect authorization readiness,
- overdue payer follow-up,
- missed peer-to-peer or response deadlines,
- authorization approval that does not match the scheduled service,
- unresolved cases moving toward service without a clear decision,
- and manual rework created when ownership or information is unclear.

The project does not assume that every delay or denial has the same cause. The purpose is to practice finding the earlier workflow condition that made the later problem possible.

## Synthetic Case Set

The Streamlit dashboard currently uses **25 synthetic prior authorization cases**. The cases include different service types, payer categories, authorization statuses, documentation conditions, urgency levels, workflow failure points, and modeled rework hours.

Within that synthetic dataset:

| Measure | Simulated Value |
|---|---:|
| Total cases | 25 |
| Cases marked for retro-authorization review | 13 |
| High or Critical denial-risk cases | 15 |
| Cases with Partial or Incomplete documentation | 11 |
| Cases with No or Late eligibility verification | 5 |
| Total modeled rework hours | 122.5 |
| Average modeled rework hours per case | 4.9 |

These values come only from the synthetic case set. They are **not healthcare benchmarks, employer results, payer outcomes, productivity measurements, or predictions of real-world performance**.

## How I Think About the Workflow

I use PARCS to practice looking at prior authorization as a connected workflow rather than an isolated task:

```text
Scheduling / Intake
        ↓
Eligibility + Requirement Review
        ↓
Documentation Readiness
        ↓
Authorization Submission
        ↓
Payer Follow-Up + Aging
        ↓
Escalation / Additional Information
        ↓
Service Clearance
        ↓
Claim Readiness / Denial Prevention
```

A problem can become visible at any point in that chain, but the first loss of control may have happened several steps earlier.

## Pre-Service vs. Post-Service Authorization Exception Review™

PARCS now includes a premium interactive workspace for practicing what happens when a pre-service authorization control is missed or remains unresolved.

The operational lesson is:

> **When authorization is missing before service, the workflow does not become fixed simply because a retro or post-service request is started. A new exception workflow begins.**

The modeled exception path is:

**Missing pre-service authorization → trace earlier control → review applicable payer/program source → determine the permitted or qualified-review path → identify required evidence → assign ownership → submit → actively follow → receive determination → route downstream action → verify closure**

The interactive workbench includes:

- Authorization Requirement Identified?
- Applicable Payer / Program Source Reviewed?
- Service Already Performed?
- Pre-Service Authorization Completed?
- Reason Pre-Service Authorization Was Not Completed
- Post-Service / Retrospective Review Path
- Documentation Requirements Identified?
- Required Documentation Ready?
- Service / Date / Provider / Location Alignment Reviewed?
- Qualified Review Needed?
- Current Owner
- Last Meaningful Action
- Next Required Action
- Next-Action Due Date
- Escalation Threshold
- Request Submitted?
- Submission Evidence
- Receipt / Status Confirmed?
- Final Determination Received?
- Downstream Claim / Account Action Completed?
- Closure Evidence
- Potential Patient-Facing Effect

### Active-Movement Control™

PARCS uses the distinction:

> **Technically open ≠ actively moving.**

The simulation tracks the last meaningful action, next required action, owner, due date, escalation status, submission evidence, and closure evidence.

### Operational Distinctions

- **Retro request submitted ≠ authorization resolved**
- **Missing prior authorization ≠ automatic eligibility for post-service review**
- **Technically open ≠ actively moving**
- **Submission ≠ closure**

### PARCS Control Question

> **If a service has already occurred without completed authorization, what evidence should determine whether the case enters an allowable post-service review path, escalates for specialist review, or moves to another revenue-cycle workflow?**

### Patient-to-Professional Insight

> **The patient experiences the uncertainty after the service. The operations team has to reconstruct whether the required control happened before the service, what exception path is available now, who owns resolution, and what proves closure.**

PARCS does not determine whether a real payer must permit retroactive or retrospective authorization. It does not make medical-necessity, coverage, coding, legal, contractual, or payer-liability decisions. The workflow is a student-developed operational simulation using synthetic information.

## What the Dashboard Helps Me Practice

The Streamlit dashboard lets me review the synthetic cases by risk level, authorization status, workflow failure point, payer type, documentation condition, eligibility status, retro-authorization need, and estimated rework burden.

I use those views to practice questions such as:

- Which cases need attention first?
- What information is missing?
- Who should own the next action?
- How close is the case to the service date?
- Is the authorization problem actually an earlier eligibility, documentation, or order-matching problem?
- What unresolved issue could become a patient-access or denial problem later?

The dashboard does not make payer decisions. It is an educational tool for practicing workflow organization, prioritization, and operational reasoning.

## Patient-to-Professional Perspective

One reason prior authorization interests me is that patients often see the outcome but not the process that created it.

Inside a workflow, the issue may be labeled as documentation readiness, authorization aging, payer follow-up, or service clearance. From the patient side, it may simply feel like waiting, uncertainty, repeated calls, a changed appointment, or being told that something is still pending.

That gap between the internal workflow label and the patient experience is what I am trying to understand better. PARCS helps me practice connecting the two without assuming that a single person, department, or payer action explains every problem.

## Portfolio Evidence

This repository includes student-developed artifacts such as:

- `app.py` — interactive Streamlit dashboard using synthetic cases
- `index.html` — PARCS project overview
- `executive-summary.html` — simulated operational summary
- `dashboard-wireframe.html` — dashboard concept
- `stress-test-report.html` — workflow stress-test documentation
- `risk-scoring-model.html` — educational risk-scoring logic
- `authorization-risk-calculator.html` — interactive risk calculator
- `authorization-tracker-template.html` — authorization tracking structure
- `monthly-scorecard.html` — simulated monthly reporting
- `sample-authorization-cases.html` — synthetic case examples
- `system-architecture.html` — workflow architecture view
- `pre-post-service-authorization-review.html` — interactive pre-service versus post-service authorization exception workbench
- `data/` — synthetic project data

## What I Am Practicing Through PARCS

Through this project, I am practicing:

- Prior authorization workflow analysis
- Patient access risk awareness
- Eligibility and authorization readiness review
- Documentation readiness analysis
- Authorization aging and follow-up thinking
- Pre-service versus post-service authorization exception review
- Payer/program source review concepts
- Active-movement control logic
- Submission, receipt/status, determination, and closure verification
- Escalation and ownership logic
- Service-clearance thinking
- Denial-prevention awareness
- Root-cause analysis
- Risk prioritization using simulated data
- KPI and dashboard design
- Operational reporting
- Synthetic data analysis
- Clear separation between modeled evidence and real-world claims

## How PARCS Fits in the Portfolio

PARCS is the second project in the workflow path I use across my healthcare operations portfolio:

**EVIS → PARCS → DPIS → SBI → Habit Audit**

- **EVIS** looks at eligibility and intake risk.
- **PARCS** looks at prior authorization workflow risk, ownership, documentation, aging, and escalation.
- **DPIS** looks at upstream denial-prevention and claim-readiness risk.
- **SBI** asks where the first cross-workflow control loss occurred.
- **Habit Audit** looks at recurring operational habits that may make workflow risk more likely.

## What This Project Is — and Is Not

This is a **student-developed educational project**.

- All cases and data are synthetic.
- No protected health information (PHI) is used.
- No real patient, payer, employer, claim, EHR, or authorization data is used.
- The project does not represent formal healthcare employment experience.
- It has not been deployed in a healthcare organization.
- It does not make clinical, coding, medical-necessity, payer, or coverage decisions.
- I do not claim that PARCS has produced real-world denial reductions, authorization turnaround improvements, cost savings, productivity gains, or patient outcomes.

I want the project to show how I am learning to organize prior authorization workflow risk and think through downstream consequences without overstating what the evidence can support.

## Live Project

[View PARCS](https://parcs-prior-authorization-command-s.vercel.app/)

## Connect

- [Healthcare Operations Portfolio Hub](https://healthcare-operations-portfolio-hub.vercel.app/)
- [LinkedIn](https://www.linkedin.com/in/kori-pickle)
- [GitHub profile](https://github.com/koripickle1101-TN)

Created by Kori Pickle. Student-developed portfolio project. Synthetic data only. No PHI.
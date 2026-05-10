# Denial Risk Score

## PARCS 2.0

**Created by Kori Pickle**

## Purpose

The Denial Risk Score forecasts downstream revenue-cycle exposure before a claim is submitted. It connects prior authorization work to clean claim readiness.

## Scoring Factors

| Risk Factor | Points |
|---|---:|
| Missing authorization number | 25 |
| Authorization approved for wrong service | 25 |
| Authorization date range may not cover service date | 20 |
| Documentation does not support medical necessity | 25 |
| Eligibility conflict unresolved | 20 |
| Payer requested additional information | 15 |
| Manual override used | 10 |
| Demographic mismatch | 15 |
| Units or visits unclear | 15 |
| Authorized provider or facility does not match scheduled service | 20 |

## Risk Levels

| Score | Level | Action |
|---:|---|---|
| 0-20 | Low | Continue normal claim readiness review |
| 21-40 | Moderate | Review before claim release |
| 41-60 | High | Hold for correction or leadership review |
| 61+ | Critical | Do not release claim until corrected |

## Control Rule

Authorization approval is not the finish line. Clean claim readiness is the finish line.

---

Created by Kori Pickle

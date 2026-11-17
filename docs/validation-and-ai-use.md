# Validation and AI Use

**AI use:** OpenAI Codex assisted with repository construction, code, documentation, and tests; I am responsible for reviewing the work, and the final analysis and decision are mine.

**Educational use only:** This project is a course demonstration, not investment advice.

## Version and as-of boundary

- Decision and market-data cutoff: September 30, 2026.
- Price observations: October 2021 through September 2026; downloaded October 22, 2026.
- Point-in-time signal: DGS10 = 5.26% on September 29, 2026, as known September 30, 2026.
- Runtime: Python 3, pandas, and Streamlit; no credentials or runtime network calls.
- Frozen commit: enter the final Git commit after the package is reviewed and committed.

## Validation register

| Claim | Failure mode | Test or comparison | Result | Evidence |
|---|---|---|---|---|
| Base constrained portfolio | Optimizer or cost error | Known allocation and metrics | 60% SGOV / 40% SPGM; 6.74% net return; 6.02% volatility; PASS | `tests/test_portfolio.py` |
| Mandate verdicts | Rules hidden or misapplied | Name each failed baseline rule | Benchmark fails reserve; equal and inverse-volatility fail return | tests and visible output |
| Grid completeness | Missing/duplicated candidates | Four assets, five-point grid | 1,771 unique portfolios | grid test |
| Weight validation | Invalid allocation accepted | Weights total 90% | Explicit `ValueError` | failure test |
| Window stress | Window control disconnected | Latest 36 versus all 59 returns | 85% SGOV / 15% SPGM; 25-point change | stress test |
| Return stress | Estimate control disconnected | SPGM return minus one point | 55% SGOV / 45% SPGM | propagation test |
| Cost stress | Cost ignored | 100 bps versus 20 bps | 55% SGOV / 45% SPGM; remains feasible | visible output |
| Point-in-time signal | Future observation used | Observation date no later than vintage date | Pass; high-rate status reproduced | as-of test and saved card |
| Recommendation | Decision inconsistent with stress | More than 20 points must prevent adoption | PILOT; largest change 25 points | decision test |

Run the complete validation with:

```sh
python3 analysis.py
python3 -m unittest discover -s tests -v
python3 -m py_compile analysis.py app.py portfolio.py
```

## Data and convention ledger

| Input | Source and availability | Definition | Main risk |
|---|---|---|---|
| Monthly adjusted closes | Yahoo Finance history pages; saved 2026-10-22 | 60 month-start rows, four ETFs | Vendor adjustment and survivorship risk |
| Expected returns | Calculated from saved prices | Arithmetic mean monthly return × 12 | Historical mean is not a forecast |
| Volatility/correlation | Calculated from saved prices | Sample monthly statistics, volatility × √12 | Regime and window sensitivity |
| Transaction cost | Analyst assumption | Basis points × benchmark-relative one-way turnover | Omits impact, tax, and recurring turnover |
| DGS10 | Federal Reserve H.15 via FRED/ALFRED | 10-year constant-maturity yield; historical vintage | Release timing and regime interpretation |

## Baseline, mandate, and stress disposition

The base constrained portfolio passes all mandate rules. The benchmark, equal-weight, and
inverse-volatility comparisons expose why constraint checks matter rather than serving as hidden
optimizer inputs. All three specified stresses remain feasible. The latest-36-month result moves
25 points, exceeding the 20-point adoption threshold, so the evidence supports a pilot only.

## Locked Changed-Input Record

**Status: incomplete and student-owned.** The required AI-off prediction and pre-run commit do not
yet exist. Complete [`locked-changed-input-record.md`](locked-changed-input-record.md) before the
changed-input run. The automated SPGM stress is useful validation but is not a substitute.

## Named AI-use register

| Tool/version | Date | Material use | Independent check | Disposition |
|---|---|---|---|---|
| OpenAI Codex; exposed model/version not displayed | 2026-11-17 | Repository structure, Python engine, app, documentation, and tests | Recompute visible output; run eight automated tests; student reviews finance assumptions and decision | Accept only after student review |

## Limitations and decision rules

- Block automatic adoption if any specified stress has no feasible portfolio or the largest
  asset-weight change exceeds 20 points; the current 25-point result limits the recommendation to
  a pilot.
- Block automatic adoption while DGS10 remains in the high-rate regime unless the return estimates
  are revalidated and the exception is documented.
- Stop the paper pilot only if the base portfolio fails the mandate, a validation test fails, or
  the DGS10 as-of observation cannot be reproduced from the saved vintage rule.
- Reassess if defensible forward-looking returns, drawdown limits, inflation risk, or realized
  transaction costs materially change the allocation.
- Mechanical agreement validates implementation, not the truth of the estimates.

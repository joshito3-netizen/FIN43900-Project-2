# Project 2 — Visible Executed Output

**Decision: PILOT as of 2026-09-30.**

**Decision line:** Pilot the lowest-risk feasible process; adopt only if every specified stress remains feasible, the maximum absolute asset-weight change from the base case is no more than 20 percentage points, and the high-rate signal is cleared or the return estimates are revalidated.

**Reason:** The base mandate passes, but automatic adoption is blocked because the largest absolute asset-weight change from the base case across specified stresses is 25 percentage points, above 20; DGS10 is in the high-rate regime and the return estimates have not been revalidated.

## Mandate

- Objective: at least 6.5% net expected return
- Universe: SGOV, SCHR, USIG, SPGM
- Benchmark: 40% USIG / 60% SPGM
- Risk measure: Annualized volatility of monthly adjusted-close returns
- Limits: Long-only, fully invested, 5-point grid, at least 3% SGOV (effective SGOV minimum is 5% on the grid)
- Reserve definition: SGOV portfolio weight
- One-way transaction cost assumption: 20 bps
- Turnover convention: 0.5 × sum of absolute target-minus-benchmark weights

## Base decision numbers

- Allocation: **SGOV 60% / SCHR 0% / USIG 0% / SPGM 40%**
- Gross expected return: **6.86%**
- Net expected return: **6.74%**
- Annualized volatility: **6.02%**
- Reserve weight: **60%**
- Mandate verdict: **PASS**
- Base turnover and cost: **60% × 20 bps = 0.12% (12 bps)**

## Benchmark and baselines

| Portfolio | Weights | Net return | Volatility | Reserve | Verdict | Failed rules |
|---|---|---:|---:|---:|---|---|
| Mandate benchmark | SGOV 0% / SCHR 0% / USIG 40% / SPGM 60% | 6.91% | 11.56% | 0% | FAIL | reserve |
| Equal weight | SGOV 25% / SCHR 25% / USIG 25% / SPGM 25% | 3.69% | 6.52% | 25% | FAIL | net_return |
| Inverse volatility | SGOV 85% / SCHR 7% / USIG 5% / SPGM 3% | 3.32% | 1.30% | 85% | FAIL | net_return |
| Constrained portfolio | SGOV 60% / SCHR 0% / USIG 0% / SPGM 40% | 6.74% | 6.02% | 60% | PASS | none |

## Stress runs

| Case | Weights | Net return | Volatility | Base mandate | Max asset change from base |
|---|---|---:|---:|---|---:|
| Window: latest 36 returns | SGOV 85% / SCHR 0% / USIG 0% / SPGM 15% | 6.71% | 1.79% | PASS | 25 points |
| Estimate: SPGM return minus 1 point | SGOV 55% / SCHR 0% / USIG 0% / SPGM 45% | 6.69% | 6.76% | PASS | 5 points |
| Cost: 100 bps | SGOV 55% / SCHR 0% / USIG 0% / SPGM 45% | 6.70% | 6.76% | PASS | 5 points |
| Constraint: net-return objective 7.0% | SGOV 55% / SCHR 0% / USIG 0% / SPGM 45% | 7.14% | 6.76% | PASS | 5 points |

All 4 specified stresses are mandate-feasible. The adoption stability measure is the maximum absolute change in any asset weight from the base allocation, which is **25 percentage points**. The displayed 55%-85% SGOV and 15%-45% SPGM sensitivity ranges span 30 points across cases; that cross-case spread is descriptive and is not the adoption-gate calculation.

## Point-in-time signal

DGS10 was **5.26%** on 2026-09-29, the last observation available in the saved 2026-09-30 vintage. The rule labels values above 5.00% as a high-rate regime. Current status: **HIGH-RATE REGIME**. This prevents automatic adoption and requires monthly review; it does not silently alter portfolio weights.

## Decision conditions

**Automatic-adoption gate:** Do not automatically adopt if any specified stress has no feasible portfolio, the maximum absolute change in any asset weight from the base allocation exceeds 20 percentage points, or DGS10 remains in the saved high-rate regime without a documented revalidation of the return estimates.

**Paper-pilot stop rule:** Stop the paper pilot only if the base portfolio fails the mandate, a validation test fails, or the required point-in-time signal cannot be reproduced. Stress instability blocks adoption but does not by itself stop observation in the pilot. The validation tests are defined in [`docs/validation-and-ai-use.md`](../docs/validation-and-ai-use.md).

## Limitations

- Historical arithmetic means are estimates, not forecasts.
- The five-point grid can miss a lower-risk off-grid portfolio.
- Volatility is not a complete measure of drawdown, inflation, or liquidity risk.
- The cost model is a one-time linear estimate relative to the benchmark.
- DGS10 is point-in-time controlled, but the Yahoo adjusted-close history was downloaded later and is not a historical vintage; later corporate-action adjustments may revise it.
- The saved point-in-time signal is contextual and not a causal return forecast.

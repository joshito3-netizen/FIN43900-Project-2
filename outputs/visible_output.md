# Project 2 — Visible Executed Output

**Decision: PILOT as of 2026-09-30.**

**Decision line:** Pilot the lowest-risk feasible process; adopt only if the largest allocation change is no more than 20 percentage points across the specified stresses and every case remains mandate-feasible.

**Reason:** The process passes the base mandate but changes by more than 20 percentage points under a specified stress or loses feasibility.

## Mandate

- Objective: at least 6.5% net expected return
- Universe: SGOV, SCHR, USIG, SPGM
- Benchmark: 40% USIG / 60% SPGM
- Risk measure: Annualized volatility of monthly adjusted-close returns
- Limits: Long-only, fully invested, 5-point grid, at least 3% SGOV
- One-way transaction cost assumption: 20 bps

## Base decision numbers

- Allocation: **SGOV 60% / SCHR 0% / USIG 0% / SPGM 40%**
- Gross expected return: **6.86%**
- Net expected return: **6.74%**
- Annualized volatility: **6.02%**
- Reserve weight: **60%**
- Mandate verdict: **PASS**

## Benchmark and baselines

| Portfolio | Weights | Net return | Volatility | Reserve | Verdict | Failed rules |
|---|---|---:|---:|---:|---|---|
| Mandate benchmark | SGOV 0% / SCHR 0% / USIG 40% / SPGM 60% | 6.91% | 11.56% | 0% | FAIL | reserve |
| Equal weight | SGOV 25% / SCHR 25% / USIG 25% / SPGM 25% | 3.69% | 6.52% | 25% | FAIL | net_return |
| Inverse volatility | SGOV 85% / SCHR 7% / USIG 5% / SPGM 3% | 3.32% | 1.30% | 85% | FAIL | net_return |
| Constrained portfolio | SGOV 60% / SCHR 0% / USIG 0% / SPGM 40% | 6.74% | 6.02% | 60% | PASS | none |

## Stress runs

| Case | Weights | Net return | Volatility | Mandate | Change from base |
|---|---|---:|---:|---|---:|
| Window: latest 36 returns | SGOV 85% / SCHR 0% / USIG 0% / SPGM 15% | 6.71% | 1.79% | PASS | 25% |
| Estimate: SPGM return minus 1 point | SGOV 55% / SCHR 0% / USIG 0% / SPGM 45% | 6.69% | 6.76% | PASS | 5% |
| Cost: 100 bps | SGOV 55% / SCHR 0% / USIG 0% / SPGM 45% | 6.70% | 6.76% | PASS | 5% |

## Point-in-time signal

DGS10 was **5.26%** on 2026-09-29, the last observation available in the saved 2026-09-30 vintage. The rule labels values above 5.00% as a high-rate regime. Current status: **HIGH-RATE REGIME**. This prevents automatic adoption and requires monthly review; it does not silently alter portfolio weights.

## Stop condition

Stop rather than adopt if any specified stress has no feasible portfolio, the largest asset-weight change exceeds 20 points, or the saved signal cannot be reproduced with an as-of vintage.

## Limitations

- Historical arithmetic means are estimates, not forecasts.
- The five-point grid can miss a lower-risk off-grid portfolio.
- Volatility is not a complete measure of drawdown, inflation, or liquidity risk.
- The cost model is a one-time linear estimate relative to the benchmark.
- The saved point-in-time signal is contextual and not a causal return forecast.

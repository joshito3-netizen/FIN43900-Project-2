# Decision Memo — Portfolio Process Pilot

**AI use:** OpenAI Codex assisted with repository construction, code, documentation, and tests; I am responsible for reviewing the work, and the final analysis and decision are mine.

**Educational use only:** This project is a course demonstration, not investment advice.

**To:** Investment committee<br>
**Decision date:** September 30, 2026<br>
**Decision horizon:** Annual strategic allocation with monthly monitoring

## Recommendation and committee ask

**Pilot the process; do not adopt it as an automatic allocation rule.** Authorize a monitored
paper pilot using **60% SGOV and 40% SPGM**, with no allocation to SCHR or USIG in the base result.
Automatic adoption requires every specified stress to remain mandate-feasible, the maximum
absolute change in any asset weight from the base allocation to remain at or below 20 percentage
points, and the high-rate signal to clear or the return estimates to be revalidated for that regime.
The 20-point test is an adoption gate, not a base mandate rule. Stop the paper pilot only if the base
portfolio fails the mandate, a validation test defined in `docs/validation-and-ai-use.md` fails, or
the point-in-time signal cannot be reproduced from an as-of vintage.

The base portfolio has a **6.86% gross expected return**, **6.74% net expected return** after a
20-basis-point cost applied to 60% benchmark-relative turnover, **6.02% annualized volatility**,
and **60% SGOV reserve weight**. Reserve weight means the SGOV portfolio weight. It passes the 6.5%
net-return objective, 3% reserve minimum, long-only rule, and fully-invested rule. Because the grid
moves in five-point increments, the 3% setting creates a 5% effective positive minimum.

One-way turnover equals `0.5 × Σ|target weight − benchmark weight|`. For the base allocation, that
is `0.5 × (60% + 0% + 40% + 20%) = 60%`. The cost drag is therefore `60% × 20 bps = 12 bps`.
The 0.5 factor prevents purchases and sales from double-counting the same rebalance.

## Mandate and comparisons

The eligible universe is SGOV, SCHR, USIG, and SPGM. The benchmark is 40% USIG / 60% SPGM. Risk
is annualized volatility of monthly adjusted-close returns. Candidate weights are long-only,
fully invested, and searched in five-percentage-point steps.

The benchmark returns 6.91% net with 11.56% volatility but fails the reserve rule because it has
no SGOV. Equal weight has a 3.69% net return and 6.52% volatility; inverse volatility has a 3.32%
net return and 1.30% volatility. Both transparent baselines fail the return objective. The
constrained portfolio is the lowest-volatility grid point that passes every rule.

## Stress evidence and allocation range

The latest-36-month window changes the result to **85% SGOV / 15% SPGM**, a 25-point move, with
6.71% net return and 1.79% volatility. Reducing SPGM's expected return by one point changes the
mix to **55% SGOV / 45% SPGM**, with 6.69% net return and 6.76% volatility. Raising one-way cost
to 100 bps produces the same 55/45 mix and a 6.70% net return. Raising the mandate's net-return
objective from 6.5% to 7.0% also produces 55% SGOV / 45% SPGM and a 7.14% net return.

All four specified stresses remain mandate-feasible, but the window stress exceeds the 20-point
base-relative adoption threshold. That failure is why the recommendation is pilot rather than
adopt. The observed range is **55–85% SGOV and 15–45% SPGM**, with 0% SCHR and USIG. Its 30-point
cross-case spread is descriptive; the adoption gate uses the largest change from the 60% SGOV / 40%
SPGM base, which is 25 points. The range is a sensitivity result, not a discretionary trading band.

## Point-in-time signal and monitoring

The saved September 30, 2026 ALFRED vintage ends with DGS10 at **5.26% on September 29**. The
predefined rule labels values above 5.00% a high-rate regime. That status blocks automatic adoption
until the return estimates are revalidated and triggers monthly review because the historical bond
estimates may be unusually regime dependent. It does not stop the paper pilot or overwrite the
optimizer's inputs or weights.

Monitor the following:

- stability across expanding, rolling 36-month, and additional defensible windows;
- the gap between historical arithmetic returns and forward-looking capital-market assumptions;
- DGS10 using the vintage actually available on each review date;
- realized turnover and costs relative to the 20-basis-point assumption;
- whether adding drawdown or inflation-risk limits changes the allocation materially.

## Limitations

Historical means are estimates rather than forecasts. Volatility is incomplete as a risk measure,
the grid is coarse, and the transaction-cost model is linear. The result concentrates in two ETFs,
while the absence of SCHR and USIG is a model output rather than evidence that those assets lack
economic value. DGS10 uses an as-of vintage, but the Yahoo adjusted-close history was downloaded
after the decision date and may reflect later corporate-action adjustments. A paper pilot is
therefore proportional to the evidence; automatic adoption is not.

# Decision Memo — Portfolio Process Pilot

**AI use:** OpenAI Codex assisted with repository construction, code, documentation, and tests; I am responsible for reviewing the work, and the final analysis and decision are mine.

**Educational use only:** This project is a course demonstration, not investment advice.

**To:** Investment committee<br>
**Decision date:** September 30, 2026<br>
**Decision horizon:** Annual strategic allocation with monthly monitoring

## Recommendation and committee ask

**Pilot the process; do not adopt it as an automatic allocation rule.** Authorize a monitored
paper pilot using **60% SGOV and 40% SPGM**, with no allocation to SCHR or USIG in the base result.
Automatic adoption requires every specified stress to remain mandate-feasible, no asset to change
by more than 20 percentage points, and the high-rate signal to clear or the return estimates to be
revalidated for that regime. Stop the paper pilot only if the base portfolio fails the mandate, a
validation test fails, or the point-in-time signal cannot be reproduced from an as-of vintage.

The base portfolio has a **6.86% gross expected return**, **6.74% net expected return** after a
20-basis-point cost applied to 60% benchmark-relative turnover, **6.02% annualized volatility**,
and **60% SGOV reserve weight**. It passes the 6.5% net-return objective, 3% reserve minimum,
long-only rule, and fully-invested rule.

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
to 100 bps produces the same 55/45 mix and a 6.70% net return.

Every specified stress remains feasible, but the window stress exceeds the 20-point stability
limit. That failure is why the recommendation is pilot rather than adopt. The observed feasible
range is **55–85% SGOV and 15–45% SPGM**, with 0% SCHR and USIG; it is a sensitivity range, not a
discretionary trading band.

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
economic value. A paper pilot is therefore proportional to the evidence; automatic adoption is not.

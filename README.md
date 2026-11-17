# FIN 43900 Project 2 — Portfolio Process Pilot

**AI use:** OpenAI Codex assisted with repository construction, code, documentation, and tests; I am responsible for reviewing the work, and the final analysis and decision are mine.

**Educational use only:** This project is a course demonstration, not investment advice.

## Decision

**Pilot, do not yet adopt.** The lowest-volatility five-point-grid portfolio that passes the
mandate is **60% SGOV / 0% SCHR / 0% USIG / 40% SPGM**. After an estimated 20-basis-point
one-way transaction cost relative to the benchmark, it has a **6.74% net expected return**,
**6.02% annualized volatility**, and **60% reserve weight**. It passes every base rule.

The **automatic-adoption gate** requires every specified stress to remain feasible, no asset to
change by more than 20 percentage points, and the high-rate signal to clear or the return estimates
to be revalidated for that regime. The latest-36-month window moves 25 points from SPGM to SGOV and
DGS10 is above its 5.00% threshold, so automatic adoption is blocked. Those conditions do not stop
the paper pilot. Stop the pilot only if the base portfolio fails the mandate, a validation test
fails, or the required point-in-time signal cannot be reproduced. Across the specified feasible
cases, the observed allocation range is **55–85% SGOV and 15–45% SPGM**, with 0% SCHR and USIG.

## One command that produces the result

After completing setup, run:

```sh
python3 analysis.py
```

The command prints the recommendation and regenerates
[`outputs/visible_output.md`](outputs/visible_output.md) and
[`outputs/visible_output.json`](outputs/visible_output.json). No credentials or network access
are required.

## Clone, setup, validate, and open the app

```sh
git clone https://github.com/joshito3-netizen/FIN43900-Project-2.git
cd FIN43900-Project-2
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 analysis.py
python3 -m unittest discover -s tests -v
streamlit run app.py
```

Windows PowerShell activation is `.venv\Scripts\Activate.ps1`. Streamlit prints a local URL,
normally `http://localhost:8501`. Move any sidebar control; the app immediately displays the
constrained allocation and its mandate verdict.

## Mandate

| Element | Rule |
|---|---|
| Objective | At least 6.5% net expected return |
| Universe | SGOV, SCHR, USIG, and SPGM |
| Benchmark | 40% USIG / 60% SPGM |
| Risk measure | Annualized volatility from monthly adjusted-close returns |
| Portfolio limits | Long-only, fully invested, five-point grid, at least 3% SGOV |
| Cost convention | One-time linear cost on turnover from the benchmark; 20 bps base |
| Stability limit | No asset may move more than 20 points across specified stresses |

The app shows the benchmark, equal-weight baseline, inverse-volatility baseline, and constrained
portfolio together. Each receives a pass/fail verdict and the name of every failed rule.

## Point-in-time signal

DGS10 is admitted only through an ALFRED vintage knowable on the decision date. The frozen card
records **5.26% on September 29, 2026, as known September 30, 2026**. A value above 5.00% is a
high-rate regime: it blocks automatic adoption until the return estimates are revalidated and
triggers monthly review, but does not stop the paper pilot or silently change portfolio weights.
The complete card is in [`data/dgs10-signal.json`](data/dgs10-signal.json).

## Repository map

- `app.py` — bounded Streamlit committee interface.
- `portfolio.py` — estimates, baselines, mandate checks, costs, and grid optimization.
- `analysis.py` — frozen base/stress decision and visible-output exporter.
- `data/prices.csv` — saved monthly adjusted closes through September 2026.
- `data/dgs10-signal.json` — frozen point-in-time signal and data card.
- `outputs/visible_output.md` / `.json` — readable and machine-readable executed results.
- `tests/test_portfolio.py` — known-answer, stress-propagation, input-failure, and as-of tests.
- `docs/decision-memo.md` — committee recommendation.
- `docs/validation-and-ai-use.md` — evidence, limitations, AI use, and remaining locked-record step.
- `docs/lab20-readiness.md` — partner cold-run and checkout record.
- `docs/project-submission-manifest.csv` — final submission-link checklist.

## Data sources and conventions

The 60 saved monthly adjusted-close rows run from October 2021 through September 2026. They were
downloaded October 22, 2026 from the Yahoo Finance history pages for
[SGOV](https://finance.yahoo.com/quote/SGOV/history/),
[SCHR](https://finance.yahoo.com/quote/SCHR/history/),
[USIG](https://finance.yahoo.com/quote/USIG/history/), and
[SPGM](https://finance.yahoo.com/quote/SPGM/history/). The engine calculates 59 monthly returns,
annualizes their arithmetic mean by 12, and annualizes sample volatility by the square root of 12.
Historical estimates are not forecasts.

The point-in-time rate is the Federal Reserve Board's H.15 10-year Treasury constant-maturity
yield retrieved through [FRED/ALFRED](https://fred.stlouisfed.org/series/DGS10). The decision uses
the saved historical vintage rather than today's revised or extended series.

## Known limitations

- Arithmetic historical returns may not represent future expected returns.
- Volatility omits drawdown, inflation, credit-event, and liquidity dimensions.
- A five-point grid can miss a better off-grid allocation.
- The linear cost estimate does not model spreads, market impact, taxes, or recurring turnover.
- The benchmark-to-target cost convention is a comparison, not a funded-account implementation.
- The point-in-time rate is contextual; it is not a causal return forecast.

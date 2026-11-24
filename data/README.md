# Data provenance

## ETF prices

`prices.csv` contains 60 saved monthly adjusted-close observations from October 2021 through
September 2026. The file was downloaded October 22, 2026 from the Yahoo Finance historical-data
pages for SGOV, SCHR, USIG, and SPGM. The application never downloads replacement prices at run
time, so a stranger receives the same inputs and result.

Source pages:

- SGOV: <https://finance.yahoo.com/quote/SGOV/history/>
- SCHR: <https://finance.yahoo.com/quote/SCHR/history/>
- USIG: <https://finance.yahoo.com/quote/USIG/history/>
- SPGM: <https://finance.yahoo.com/quote/SPGM/history/>

Columns are ordered `Date,SGOV,SCHR,USIG,SPGM`. Dates are unique and ascending; prices must be
numeric, complete, and positive. The engine calculates monthly percentage changes before applying
the optional 36-return window.

Lineage and transformations:

- Saved-file SHA-256: `afeca2384f636613673adeef55fd815c38cdc00668eddca523e9b6e4a09a2a66`.
- Coverage: 60 month-start observations, producing 59 monthly returns from November 2021 through
  September 2026.
- Definition: vendor adjusted close, one value per ticker per month.
- Vintage limitation: the file was saved after the September 30 decision date and is not a
  point-in-time Yahoo vintage. Adjusted closes can be revised later for dividends, splits, or other
  corporate actions. The DGS10 card is vintage-controlled; the price history is not.
- Transformations: percentage change, arithmetic mean multiplied by 12, sample standard deviation
  multiplied by the square root of 12, and pairwise correlation on the same complete returns.
- Exclusions: no interpolation, winsorization, backfill, survivorship correction, or row deletion.
- Validation: the engine rejects a wrong schema, duplicate or unordered dates, missing values,
  nonnumeric values, and nonpositive prices.
- Licensing and privacy: vendor terms govern the source pages. The saved course dataset contains
  public market observations and no personal information.

## DGS10 signal

`dgs10-signal.json` is the point-in-time data card. It records the last DGS10 observation available
in the September 30, 2026 ALFRED vintage. It is intentionally frozen rather than refreshed with
today's FRED history.

The saved card's SHA-256 is
`1770827eb8dda68445372c6e8543a4a6b89ef1e845d3d392b7f811ef303ebe0d`. The
observation, vintage date, units, release-lag rule, threshold, status, source URL, and retrieval
date remain together so the signal can be audited without a live download.

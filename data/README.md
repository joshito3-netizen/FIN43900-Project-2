# Data provenance

## ETF prices

`prices.csv` contains 60 saved monthly adjusted-close observations from October 2021 through
September 2026. The file was downloaded October 22, 2026 from the Yahoo Finance historical-data
pages for SGOV, SCHR, USIG, and SPGM. The application never downloads replacement prices at run
time, so a stranger receives the same inputs and result.

Columns are ordered `Date,SGOV,SCHR,USIG,SPGM`. Dates are unique and ascending; prices must be
numeric, complete, and positive. The engine calculates monthly percentage changes before applying
the optional 36-return window.

## DGS10 signal

`dgs10-signal.json` is the point-in-time data card. It records the last DGS10 observation available
in the September 30, 2026 ALFRED vintage. It is intentionally frozen rather than refreshed with
today's FRED history.

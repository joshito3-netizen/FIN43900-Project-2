# Lab 20 — Project 2 Readiness

## Question

Could a committee member who has never met me reach my Project 2 decision from this repository,
and does the decision survive one changed input?

## Pre-partner readiness

The repository has a root README, one result-producing command, a runnable Streamlit app, frozen
visible output, matching memo and validation records, eight automated tests, two transparent
baselines, a mandate benchmark, a stress record, and a point-in-time signal card. The Locked
Changed-Input Record, partner cold run, videos, and final transcript replacements remain open.

## Independent AI preflight — does not replace the partner run

**Reviewer:** OpenAI Codex, not the required human partner<br>
**Run date:** November 17, 2026<br>
**Source:** Fresh public clone of `https://github.com/joshito3-netizen/FIN43900-Project-2.git`

Commands followed from the README:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 analysis.py
python3 -m unittest discover -s tests -v
streamlit run app.py
```

- First repository failure: `none`.
- Elapsed time through generated output and tests: approximately 18.5 seconds on the review machine.
- Result location: `outputs/visible_output.md`; the app opened locally through Streamlit.
- Result: `PILOT`; all eight tests passed; the app returned HTTP 200.
- Control check: changing the window to the latest 36 monthly returns displayed 85% SGOV / 15%
  SPGM and a PASS mandate verdict without an exception.
- Nonblocking warning: Streamlit recommends replacing deprecated `use_container_width=True` calls
  with `width="stretch"`.
- AI-preflight fix: no fix was required for execution. The required partner must still record the
  partner run and either its first fix or `No fix needed` below.

## Partner cold-run note — partner completes this section

- Command followed from the README:
- First failure, or `none`:
- Elapsed time to a readable decision:
- Where the result appeared:
- Rerun result after the first fix:

## Changed input — student completes with AI closed

Complete `docs/locked-changed-input-record.md`, commit and push the prediction before the run, then
record the before/after output and result commit. Do not use the automated SPGM stress as a claim
that this student-owned requirement has already been completed.

## Explain the code — complete with the partner and AI closed

Open `search_lowest_risk` in `portfolio.py`.

- Partner's question:
- My answer from the code:
- Line I could not explain, or `none`:

## First fix

- First failure fixed and pushed, with commit:
- Or, if the partner cold run was clean: `No fix needed`:

## Decision line

**Pilot the lowest-risk feasible portfolio process; adopt only if every specified stress remains
mandate-feasible and no asset allocation changes by more than 20 percentage points.**

## Reflection — complete with the partner

1. What the cold run found that I could not see:
2. What I will not touch before the deadline:

## Checkout links

Replace these branch links with commit permalinks after the required records are complete.

- [README](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/README.md)
- [App](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/app.py)
- [Engine](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/portfolio.py)
- [Visible output](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/outputs/visible_output.md)
- [Decision memo](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/docs/decision-memo.md)
- [Validation and AI use](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/docs/validation-and-ai-use.md)
- [Lab 20 record](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/docs/lab20-readiness.md)

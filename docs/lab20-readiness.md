# Lab 20 — Project 2 Readiness

## Question

Could a committee member who has never met me reach my Project 2 decision from this repository,
and does the decision survive one changed input?

## Readiness status

The repository has a root README, one result-producing command, a runnable Streamlit app, frozen
visible output, matching memo and validation records, fourteen automated tests, two transparent
baselines, a mandate benchmark, a stress record, and a point-in-time signal card. The changed-input
record and partner cold run are complete; the remaining student work is to record the videos and
replace the transcript and manifest placeholders with the actual recordings.

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
- AI-preflight fix: no fix was required for execution. A later cold-run note reports that JSON
  floats were rounded to 12 decimals and a fresh-clone rerun left the tree clean; that report is
  recorded below and remains separate from the human partner's original run.

## Partner cold-run note — Rocco Falls

**Partner:** Rocco Falls

**Run date:** November 17, 2026

**Source commit supplied:** `5ee3f04`

Claude organized Rocco's notes; the partner and run details below are Rocco's report.

Commands followed from the README:

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

- First failure, or `none`: none; every command ran as written.
- Elapsed time to a readable decision: about 28 seconds from clone through install, analysis, and tests.
- Where the result appeared: terminal `PILOT` line and `outputs/visible_output.md`; Streamlit app served normally.
- Test result: all eight tests passed; partner noted pandas 2.3.3 and Streamlit 1.67.0.
- Rerun result after the first fix: the partner's Claude-organized note reports a fresh-clone rerun
  on November 23, 2026, after JSON floats were rounded to 12 decimals; `git status` was clean after
  `analysis.py`, and all eight tests passed. The current local code now applies the same 12-decimal
  normalization, and this checkout passes 14 tests.

### Issues found by the partner

1. Running `analysis.py` changed the last digit of two correlation values in
   `outputs/visible_output.json`; the decision did not change. The partner recommended rounding
   floats before JSON export to make the clean-run check reproducible.
2. The GitHub repository lacked local project work, including the newer tests, rubric coverage,
   submission readiness, presentation, and recording script.
3. When publishing local changes, preserve the completed GitHub version of
   `docs/locked-changed-input-record.md`; do not replace it with a blank template.

### Partner feedback received

The partner could understand the investment recommendation from the repository alone and found the
allocation, mandate, stress results, and baseline comparisons clear. The partner recommended:

1. Distinguish the condition that blocks automatic adoption from the condition that stops the paper
   pilot, because the 25-point change has already triggered the adoption gate.
2. Add repository cloning instructions to the README.
3. Incorporate the high-rate signal into the final adoption criteria.
4. Prioritize decision-condition clarity rather than materially changing the optimization model.

## Changed input — completed

The student-authored prediction was committed before the changed-input run. The before/after
outputs, actual decision effect, and prediction comparison are recorded in
`docs/locked-changed-input-record.md` and `docs/changed-input-evidence/`.

## Explain the code — complete with the partner and AI closed

Open `search_lowest_risk` in `portfolio.py`.

- Partner's question (as captured in Claude-organized notes): Why does the optimizer compare
  `metrics["volatility"] < best["volatility"] - 1e-15` instead of using plain `<`?
- My answer from the supplied notes: `search_lowest_risk` evaluates each portfolio on the five-point
  grid, skips portfolios that fail a mandate rule, and retains the passing portfolio with the lowest
  volatility. The tolerance prevents floating-point noise from replacing the current best; effective
  ties are resolved by grid order. The function returns `None` when no portfolio passes.
- Line I could not explain, or `none`: none reported in the supplied notes.

## First fix

- Documentation and decision-logic fix: commit `49a0d97` distinguishes the automatic-adoption gate
  from the paper-pilot stop rule, adds clone instructions, and makes the high-rate signal an explicit
  adoption criterion.
- Partner rerun after the fix: reported above; all eight tests passed and `git status` was clean
  after regenerating the output.

## Decision line

**Pilot the lowest-risk feasible portfolio process; adopt only if every specified stress remains
feasible, no asset weight changes by more than 20 percentage points from the base allocation, and the high-rate signal clears
or the estimates are revalidated; stop the paper pilot only if the base mandate or validation fails.**

## Reflection — complete with the partner

1. What the cold run found that I could not see: the JSON export could differ in the last decimal
   place between runs even though the decision was unchanged; the note recommends rounding floats.
   It also noted that GitHub lagged behind the local project and warned not to overwrite the
   completed locked record.
2. What I will not touch before the deadline: the supplied note says not to change the price data,
   return and volatility estimates, optimizer, or decision logic; only documentation and JSON
   rounding should change.

## Checkout links

Replace these branch links with commit permalinks after the required records are complete.

- [README](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/README.md)
- [App](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/app.py)
- [Engine](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/portfolio.py)
- [Visible output](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/outputs/visible_output.md)
- [Decision memo](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/docs/decision-memo.md)
- [Validation and AI use](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/docs/validation-and-ai-use.md)
- [Lab 20 record](https://github.com/joshito3-netizen/FIN43900-Project-2/blob/main/docs/lab20-readiness.md)

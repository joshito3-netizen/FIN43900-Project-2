# Project 2 Rubric Coverage

This map directs a reviewer to the evidence for each grading criterion. It does not replace the
decision memo, validation record, visible output, or videos.

| Criterion | Decision-ready evidence | Main locations |
|---|---|---|
| Problem definition and decision usefulness | Investment committee decides whether to pilot or adopt an annual strategic allocation process. The mandate, one-year monitoring horizon, constraints, Project 2 no-edition boundary, reversal conditions, and committee ask are explicit. | `README.md`; `docs/decision-memo.md`; Video 3 |
| Data integrity and traceability | Saved market inputs include source pages, download and as-of dates, definitions, transformations, exclusions, file hashes, input validation, point-in-time vintage rules, and no personal information. | `data/README.md`; `data/prices.csv`; `data/dgs10-signal.json`; `docs/validation-and-ai-use.md` |
| Financial soundness and judgment | Arithmetic-return, volatility, covariance, turnover, cost, benchmark, reserve, and grid conventions are explicit. The recommendation is a paper pilot with a sensitivity range, monitoring triggers, an adoption gate, and a stop rule. | `portfolio.py`; `outputs/visible_output.md`; `docs/decision-memo.md` |
| Technical execution and usability | One engine supplies the batch output and Streamlit app. After clone and dependency installation, the frozen run requires no credentials or network call. Invalid inputs fail loudly. | `README.md`; `analysis.py`; `app.py`; `portfolio.py`; `requirements.txt` |
| Validation, sensitivity, and reproducibility | Thirteen tests cover known answers, the cost bridge, baselines, grid completeness, four stress dimensions, the cross-case range distinction, lineage, invalid inputs, as-of timing, and the final decision. The Locked Changed-Input Record remains a student-only completion item. | `tests/test_portfolio.py`; `docs/validation-and-ai-use.md`; `docs/locked-changed-input-record.md` |
| Professional communication | Memo, README, visible output, validation record, manifest, video scripts, transcripts, and committee deck use the same decision, dates, numbers, conditions, and audience framing. | `docs/`; `outputs/visible_output.md`; videos after recording |

## Final student-controlled evidence

Before the submission freeze, complete the AI-off Locked Changed-Input Record through its pre-run
commit and preserved result, record and upload the three distinct videos, correct the transcript
files to the spoken words, and replace every manifest placeholder with stable URLs, timestamps,
access checks, and immutable identifiers.

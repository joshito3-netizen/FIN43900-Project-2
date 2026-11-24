# Locked Changed-Input Record — Student Completion Required

This required Project 2 record is intentionally **not completed by AI**. The student must write the
prediction with AI closed, commit and push it before changing or running the selected input, then
preserve the before/after output and result commit.

## Pre-run prediction — write with AI closed

- Material input:
- Input location:
- Old value and units:
- New value and units:
- Expected direction of allocation, net return, volatility, and mandate verdict:
- Expected decision effect:
- Failure condition:
- Prediction commit hash:

## Post-run result

- Before output: [`changed-input-evidence/before_visible_output.md`](changed-input-evidence/before_visible_output.md) — 6.5% net-return objective; 60% SGOV / 40% SPGM; 6.74% net expected return; 6.02% annualized volatility; mandate PASS; overall decision PILOT.
- After output: [`changed-input-evidence/after_visible_output.md`](changed-input-evidence/after_visible_output.md) — 7.0% net-return objective; 55% SGOV / 45% SPGM; 7.14% net expected return; 6.76% annualized volatility; mandate PASS; overall decision PILOT.
- Decision changed or unchanged: Unchanged. The portfolio passes the higher return floor, but the overall recommendation remains PILOT because the DGS10 adoption gate remains blocked. The stress output also continues to report a 25-point maximum asset change from the base across specified stresses.
- Prediction matched, partly matched, or failed: Partly matched. The predicted 55% / 45% allocation, approximately 7.14% net return, approximately 6.8% volatility, feasibility, and unchanged PILOT decision match the after output. The stated failure condition should say a move of more than 20 points breaches the stability gate; exactly 20 points meets the limit.
- Explanation or failure diagnosis: Raising the net-return objective from 6.5% to 7.0% changes the selected portfolio from 60% SGOV / 40% SPGM to 55% SGOV / 45% SPGM. On the five-point grid, the new portfolio clears the floor at 7.14% net return. Its benchmark-relative one-way turnover is 55%, producing an 11-basis-point cost under the stated 20-basis-point convention. Volatility increases to 6.76%. All four specified stresses remain feasible. The changed objective alone does not alter the committee recommendation.
- Result commit hash:

The existing automated one-point SPGM stress validates propagation, but it is not represented as
the required human-authored, AI-off, precommitted record.

# Continuous research loop

Use this when the request includes optimization, self-evolution, a stronger model, or reaching/advancing the state of the art.

## State machine

Use these phases: `contract → validate → benchmark → screen → confirm → frozen_test → report`. Continuous research inserts repeated `hypothesize → experiment → audit` rounds between `screen` and `confirm`.

Persist every transition in `research-state.json`. A batch process returning exit code zero maps to `batch_complete`, not automatically to `complete`.

## One round

1. Diagnose the current Pareto frontier and the largest reproducible weakness.
2. Generate 1–3 falsifiable hypotheses, each with a mechanism, smallest useful treatment, control and expected metric signature.
3. Prioritize by expected information gain divided by compute and implementation risk.
4. Run the smallest fair experiment that can reject the hypothesis.
5. Compare on development evidence, including variance, key subsets and resource cost.
6. Keep, revise or reject the idea; record negative results.
7. Decide whether evidence justifies scale-up, multi-seed confirmation, another round or termination.

Do not stack many changes at once. When a combined model improves, run enough ablations to identify what caused the gain.

## Advancement rule

A candidate advances only if it beats the declared gate on development data and does not violate hard secondary constraints. A useful default is improvement larger than both a practical threshold and uncertainty/noise. Never claim superiority from one lucky seed.

## Terminal conditions

End in exactly one explicit state:

- `converged`: planned hypotheses exhausted and recent rounds fail to produce meaningful, stable gains;
- `budget_stop`: declared time/compute budget reached with best evidence preserved;
- `needs_new_data`: model changes no longer address the diagnosed limit;
- `blocked`: an external condition prevents safe continuation after the retry/blocking rules;
- `user_stop`: user explicitly stops the run;
- `complete`: frozen protocol, final test and report all completed.

Record why the state is justified and what evidence would reopen the research.

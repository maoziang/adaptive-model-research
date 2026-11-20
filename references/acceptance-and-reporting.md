# Acceptance and reporting

Run this after each batch and fully at the terminal stage.

## Completeness gates

Confirm every activated model, capacity, recipe, seed, target/subtask and evaluation slice has a valid atomic artifact. A registry option that was never activated does not require training; distinguish untried ideas, deliberately rejected branches, failed trials and incomplete required confirmation. Verify finite metrics, matching fingerprints, expected checkpoints, curves and no unauthorized test access. Missing or invalid activated candidates remain explicit; do not silently remove them from rankings.

## Report multiple views

Provide:

- primary metric with direction and uncertainty;
- all secondary and safety metrics;
- per-target, per-horizon, per-class, per-domain or other key slices;
- mean, standard deviation and worst seed for finalists;
- parameter count, peak memory, training time, inference latency/throughput and artifact size;
- failure, repair and excluded-run ledger;
- ablations and rejected hypotheses.

Use confidence intervals or paired tests where justified, but also state practical effect size. Avoid mixed-unit aggregates that hide poor components.

Recompute consequential metrics from saved prediction arrays and source labels,
including origin alignment and train-only scaling, before accepting a report.
Reload the selected checkpoints and replay representative forecasts. If CPU/GPU
outputs differ, preserve the failed comparison and investigate with the original
device, inference backend and batch boundaries. Do not silently widen tolerance
until a test passes: document measured per-target differences, exact-path replay
and any justified cross-device tolerance in meaningful units. A seed uncertainty
interval on fixed development data is not an unseen-data generalization interval.

Apply advancement thresholds to unrounded numbers. A gain displayed as 1.00% may
still fail a 1% gate; a stable sub-threshold gain remains a tradeoff candidate, not
automatic production promotion. State whether reported five-seed metrics describe
separate models or an actual prediction ensemble.

## Name the winners precisely

Do not force one model to be “best” in every sense. Identify:

- main-metric champion;
- key-subtask champion;
- efficiency knee;
- most stable candidate;
- production candidate under deployment constraints;
- exploratory result still needing new evidence.

## Final narrative

Explain what changed, why it was tested, what evidence supported or rejected it, why the selected model is credible, where it fails, and what would be tried next. Distinguish current-dataset superiority from cross-dataset or real-world generalization.

The final report must be proactively delivered in the same main chat that monitored training. A completed process without this report is unfinished work.

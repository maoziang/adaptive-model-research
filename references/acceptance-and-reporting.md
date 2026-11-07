# Acceptance and reporting

Run this after each batch and fully at the terminal stage.

## Completeness gates

Confirm every declared model, capacity, recipe, seed, target/subtask and evaluation slice has a valid atomic artifact. Verify finite metrics, matching fingerprints, expected checkpoints, curves and no unauthorized test access. Missing or invalid candidates remain explicit; do not silently remove them from rankings.

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

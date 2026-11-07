# Co-evolution axes

Do not reduce research to “try another architecture” or “add parameters.” Select the smallest axis that can explain the observed error.

## Data and sampling

Audit coverage, missingness, noise, imbalance, domain shift, temporal regimes and boundary handling. Compare sampling frequency or windowing only when it preserves the real deployment contract. More rows are not automatically more independent information.

## Task and target

Revisit target transforms, multi-task sharing, horizon formulation, calibration and uncertainty. Keep deployment semantics stable or record a new contract.

## Features and representation

Test raw versus derived features, categorical/time encodings, normalization, augmentation and representation learning. Fit learned transforms on training data only.

## Loss and optimization

Consider robust loss, task/horizon weighting, curriculum, optimizer, schedule, warmup, regularization, gradient clipping, mixed precision and early stopping. Treat each recipe as part of the candidate fingerprint.

## Capacity

Search a meaningful small/medium/large range around a credible literature- or scaling-informed center. Track parameter count, FLOPs or latency, memory, convergence and generalization. Find the capacity boundary rather than assuming bigger or smaller is better.

## Architecture

Use failure modes to motivate inductive biases: local patterns, long context, cross-variable interaction, spatial structure, recurrence, attention, decomposition, state-space dynamics or retrieval/memory. Preserve strong components through controlled hybrids and ablations.

## Ensembling and routing

Only after standalone candidates are validated, test averaging, stacking, horizon/task-specific experts or confidence-aware routing. Train selectors on development data, record oracle upper bounds separately and retain a deterministic fallback.

## Deployment

Evaluate batch/online latency, memory, throughput, calibration, drift behavior and rollback. The research champion and production candidate may differ; report both honestly.

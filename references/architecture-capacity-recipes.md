# Architecture, capacity and recipe search

## Build a factorial matrix

Separate three questions:

1. Which inductive bias or architecture helps?
2. At what capacity does it help?
3. Which training recipe allows that capacity to generalize?

Use at least two credible capacity points for important architectures and keep optimization budgets comparable. A tiny implementation does not represent the architecture family; an oversized model is not evidence that scale helps.

## Capacity ladder

Choose capacity points from data size, effective independent samples, input/target complexity, literature ranges and available compute. Use logarithmic or roughly multiplicative steps rather than tiny arbitrary increments. Record actual trainable parameters, activated parameters where relevant, peak memory, training time and inference cost.

If the larger model loses, diagnose under-training, optimization instability, regularization, context design, data diversity and noise before concluding that capacity is harmful. If it wins, still locate the next boundary; do not extrapolate indefinitely.

## Screening and confirmation

- Smoke test every family on a small deterministic slice to catch code errors, not to rank models.
- Screen candidates under a common development budget and one fixed seed.
- Promote only candidates passing the declared gate.
- Confirm finalists with multiple fixed seeds and complete curves.
- Freeze selection before final testing.

## Recipe dimensions

Tune only justified ranges for learning rate, batch/accumulation, optimizer, scheduler, warmup, weight decay, dropout, normalization, clipping, precision, early stopping and loss weighting. Changing a recipe produces a distinct fingerprint.

## Ablation discipline

For a new hybrid, compare the parent models, capacity-matched variants where possible, the combined model and removals of each claimed innovation. Report whether gains come from architecture, extra parameters, longer training or data treatment.

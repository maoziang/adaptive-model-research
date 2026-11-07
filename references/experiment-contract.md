# Experiment contract

Read this before data replacement, experiment design, or formal training.

## Freeze the question first

Write a machine-readable contract containing:

- task type, prediction target or label space, input fields and unit semantics;
- sampling rate, context/window definition, forecast horizon or decision point;
- grouping and temporal boundaries that windows may not cross;
- train/validation/test policy and any rolling development folds;
- primary metric, secondary metrics, per-target/per-horizon metrics and direction;
- simple baseline, strong baseline and the exact comparison budget;
- fixed seeds, early-stopping rule, resource budget and terminal conditions.

Hash the contract together with the dataset manifest, split manifest, code revision, environment lock and model configuration. Reuse an artifact only when its full fingerprint matches.

## Data gates

Before training, verify schema, types, units, timestamps or identifiers, duplicates, missingness, label validity, continuity, group boundaries, outliers and finite values. Generate a data-quality report rather than silently filling or dropping records.

Fit scalers, imputers, encoders, feature selectors, target transforms and learned augmentations on the training partition only. Persist fitted objects and hashes. For time series, split chronologically and prohibit input/target windows from crossing split, batch, subject or operational boundaries. For grouped i.i.d. tasks, prevent entity leakage.

## Fair comparison

All candidates in one comparison must share the same raw data version, split, inputs, targets, horizons, evaluation code and stated compute budget. If a model needs a different representation, record that as a treatment rather than hiding it.

Start with a trivial baseline and a credible classical or compact neural baseline. They reveal leakage, broken metrics and cases where complexity adds no value.

## Test discipline

Use training and validation or rolling development folds for all design decisions. Freeze code, configuration and selection rules before opening the test set. Run the final test only after the candidate is selected. Any idea inspired by test results becomes exploratory and requires fresh evidence.

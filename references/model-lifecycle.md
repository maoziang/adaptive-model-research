# Model lifecycle, switching and production selection

## Registry states

Use explicit states: `planned`, `screening`, `candidate`, `confirmed`, `frozen_tested`, `production`, `deprecated`, `failed`. Transitions require recorded evidence and actor/time metadata.

Keep immutable model IDs tied to dataset, split, code, configuration, seed and checkpoint hashes. A display name is not identity.

## Switching modes

- **Manual**: user selects one validated model; show task scope, evidence and limitations.
- **Static default**: production candidate selected from frozen evidence.
- **Rule-based routing**: deterministic mapping by task/horizon/domain, validated on development data.
- **Learned routing**: selector trained without test leakage, with an oracle ceiling and deterministic fallback.
- **Ensemble**: explicitly versioned combination; report incremental gain and cost over its members.

Never use random recall. Never let a language model directly choose a safety-critical action without deterministic constraints. A router may select a validated predictor, but downstream control or business rules still validate outputs.

## Promotion and rollback

Promotion requires acceptance gates, artifact integrity, inference compatibility and rollback readiness. Keep the previous production model until the new one passes shadow or staged verification where applicable. Log every switch and its reason.

Research winners may be too slow, unstable or expensive for production. Preserve both the research champion and the deployment choice.

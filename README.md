# Adaptive Model Research

A reusable Codex skill for rigorous model-training research: visible long-run monitoring in the current main chat, bounded self-repair, resumable experiment state, architecture/capacity/recipe co-evolution, leakage-safe selection, and evidence-based reporting.

## What makes it different

- Long training stays attached to the current main chat—never silently delegated to a background window or another chat.
- Stable runs use passive waiting and compact heartbeats about every 30 minutes, while faults and milestones are handled immediately.
- `batch_complete` triggers acceptance and the next research decision; it is not mistaken for final completion.
- Data, task, features, loss, training recipe, capacity, architecture, ensemble/routing, and deployment evolve together.
- Automatic repair is bounded, fingerprinted, auditable, and forbidden from quietly changing the experiment contract.
- Final selection separates metric champion, key-subtask champion, efficiency knee, stability winner, and production candidate.

## Install

Copy this repository folder to your Codex skills directory, keeping `SKILL.md`, `agents/`, `references/`, and `scripts/` together. Restart or reload Codex if the skill list does not refresh automatically.

On Windows the usual destination is:

```text
C:\Users\<you>\.codex\skills\adaptive-model-research
```

## Use

Invoke it explicitly:

```text
$adaptive-model-research Prepare and run this model comparison. Keep the long training visible in this main chat, check it about every 30 minutes, repair safe failures, and deliver the final research report here.
```

The skill is domain-independent and can support forecasting, classification, regression, vision, language, and multimodal experiments. Project-specific training code and data remain outside the skill.

## Repository layout

- `SKILL.md`: concise operating contract and routing.
- `references/`: experiment design, monitoring, repair, research, acceptance, and lifecycle rules.
- `scripts/inspect_training_run.py`: compact read-only heartbeat inspector.
- `scripts/test_inspect_training_run.py`: inspector regression tests.
- `agents/openai.yaml`: Codex skill metadata.

## Safety and scientific integrity

The skill never authorizes test leakage, fabricated superiority, hidden protocol changes, unbounded retry loops, or direct safety-critical control by an unconstrained model. Inspect every project-specific command before running it.

## License

MIT

# Automation
This directory holds the design and future implementation of the channel's production automation system.
The system is designed to support the documented pipeline (see docs/PRODUCTION_WORKFLOW.md) while keeping human judgment in charge of every important decision.
## What Lives Here
- README.md — orientation and conventions (this file)
- ARCHITECTURE.md — system shape, orchestrator, workers, state, and boundaries
- STATE_SCHEMA.md — the canonical record for each job and each video
- APPROVAL_GATES.md — the points where humans must approve before the system proceeds
## What Does NOT Live Here Yet
This directory currently holds design documents only.
- No runtime code
- No agent definitions
- No API or OAuth integrations
- No media downloads
- No YouTube publishing
Implementation is intentionally deferred until the manual Video #1 workflow has been performed, documented, and reviewed.
## Core Invariants
The automation system must remain:
- Stateful and resumable across machines
- Portable across Windows, macOS, Linux, and constrained devices such as phones
- GitHub-friendly — small text files committed in meaningful commits, no large binaries in the repo
- Safe with secrets — no secrets in repo, no secrets in state files, no secrets in logs
- Human-approved at the gates defined in APPROVAL_GATES.md
- Progressively automatable — every step can be run manually today
- Simple and maintainable — prefer readable Markdown state over clever runtime structures
- Honest about evidence — automation never fabricates sources, facts, or visuals
## Local State vs Repo State
Repo (committed):
- This design documentation
- Canonical job and video state (text only)
- Templates, scripts, and small utilities
- Notes, decisions, and review records
Local only (never committed):
- Rendered media files
- Downloaded source assets
- API keys and OAuth tokens
- Caches, logs, and intermediate outputs
The .gitignore already excludes media, output, renders, assets, cache, logs, and .env. Do not weaken it.
## Worker Roster (Future)
When implementation begins, the system expects to call these kinds of workers:
- Hermes — primary coordinator, owner of approvals and high-level decisions
- Claude Code — long-form writing, editing, code, and research synthesis
- Codex — code generation and code review
- Specialist agents — to be introduced only when a specific stage proves its value
Workers are interchangeable where the orchestrator can express the task as input/output. The orchestrator, not the worker, owns state.
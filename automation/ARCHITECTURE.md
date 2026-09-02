# Automation Architecture
## Purpose
Describe how the production pipeline is automated end to end, while keeping the channel's quality, restraint, and honesty standards intact.
This document defines the shape of the system. Implementation is deferred until Video #1 is complete.
## Pipeline
The system implements the documented workflow in docs/PRODUCTION_WORKFLOW.md:
1. Story Discovery
2. Story Evaluation
3. Research
4. Fact Checking
5. Outline
6. Script
7. Script Review
8. Narration
9. Visual Planning
10. Asset Collection or Creation
11. Production
12. Sound Design
13. Quality Control
14. Thumbnail and Title
15. Upload
16. Performance Review
17. Workflow Improvement
## Roles
### Orchestrator (Hermes)
Owns:
- The job and video state
- The current stage and the next eligible stage
- Approval gate enforcement
- Worker selection per stage
- Human-readable summaries of progress and blockers
The orchestrator does not generate content. It coordinates.
### Workers
Perform individual stages. Each worker:
- Reads inputs from the state record and from the repo (templates, research notes, scripts)
- Writes outputs into the appropriate file path under research/, production/, or scripts/
- Never modifies the state record directly — the orchestrator does that based on the worker's return value
- Returns a structured result with status, outputs, errors, and any approval requests
### Human (Channel Owner)
Owns:
- The final go / no-go at each approval gate (see APPROVAL_GATES.md)
- The publishing action (the system prepares, the human publishes, until explicitly authorized otherwise)
- Any irreversible external action not covered by an approved gate
## Boundaries
### What the system may do without further approval
- Run a stage whose inputs are present and whose prior gate is approved
- Write or update files under research/, production/, scripts/
- Read existing files in the repo
- Maintain state records under automation/state/
### What the system may NOT do without explicit human approval
- Skip an approval gate
- Promote a story from evaluation to production
- Promote a draft script into the narration / production stages
- Begin asset downloads at scale
- Render a final video for production use
- Make any external network call that costs money or alters an account
- Publish to YouTube or any platform
- Commit or push to GitHub on its own initiative
- Modify .gitignore, secrets handling, or this ARCHITECTURE.md
## State Model
See STATE_SCHEMA.md.
Every job has a canonical record. Workers are stateless. The orchestrator is the only writer to the state record.
## Approval Gates
See APPROVAL_GATES.md.
Six mandatory gates cover story selection, research and evidence, script, visual and asset plan, final video, and publishing.
## Failure and Retry
- A stage failure is recorded in the state record with stage, error, timestamp, and retry count.
- Transient failures (network, rate limit) retry with exponential backoff up to a configurable cap.
- Non-transient failures (missing evidence, reviewer rejection) return control to the human with a clear summary.
- The state record is updated on every transition, including failures. No silent progress.
## Portability
- All state is plain text (Markdown or JSON) under automation/state/.
- No local absolute paths in state; use repo-relative paths.
- No environment-dependent tooling assumed. Python 3 and Git are the only assumed tools.
- Any heavy media path stored in state must be a repo-relative path under a local-only directory excluded by .gitignore.
## Secret Handling
- No secrets in state files, templates, or example files.
- API tokens are loaded from environment variables or a local .env that is git-ignored.
- Any worker that needs credentials reads them at runtime and never logs them.
- The orchestrator redacts common secret patterns from logs and worker outputs before writing to state.
## Git Discipline
- The system never force-pushes, rewrites history, or amends other agents' commits.
- Each state transition that warrants a commit produces a clearly scoped commit.
- Commit messages follow the pattern documented in docs/PRODUCTION_WORKFLOW.md or any future COMMIT_GUIDELINES.md.
- Large media never enters the repo. Local-only directories are referenced by path, not by file content.
## Progressive Automation
Each pipeline stage is classified:
- Manual only (until proven) — initial stages, especially story discovery, evaluation, and final QC.
- Assisted — system drafts, human reviews and approves.
- Automated (with approval) — system runs, human approves the output.
- Fully automated — reserved for tasks with no quality or ethical risk.
The default for the first video is "manual only" or "assisted." The default never becomes "fully automated" for editorial decisions.
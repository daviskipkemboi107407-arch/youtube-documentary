# State Schema
## Purpose
Define the canonical records the orchestrator writes and reads. Two record types:
- Job — a unit of work, typically one documentary from discovery through performance review
- Stage Run — one execution of one pipeline stage for a specific job
All records are plain text (Markdown preferred, JSON acceptable where machine parsing helps) and live under automation/state/.
## Directory Layout
automation/state/
  jobs/
    <job-id>.md
  stages/
    <job-id>/
      <stage-id>.md
  errors/
    <job-id>.md
## Job Record
File: automation/state/jobs/<job-id>.md
Required fields:
- job_id — short kebab-case identifier, e.g. video-001
- title — working title, may change
- channel — fixed value: The World Is Stranger Than We Think
- created_at — ISO 8601 timestamp
- updated_at — ISO 8601 timestamp
- current_stage — one of the 17 pipeline stages
- status — one of: draft / in_progress / awaiting_approval / blocked / completed / archived
- approvals — see Approval sub-section
- inputs — repo-relative paths to source files (evaluation, research notes, outline, script, metadata)
- outputs — repo-relative paths to produced files
- errors — link or pointer to automation/state/errors/<job-id>.md when present
- notes — free-form human-readable summary
Optional fields:
- video_id — YouTube ID once published (never filled until after publishing)
- publish_at — scheduled publish time
- performance — populated only after performance review
## Stage Run Record
File: automation/state/stages/<job-id>/<stage-id>.md
Required fields:
- stage_id — kebab-case stage identifier, e.g. script-review
- stage_name — human-readable stage name
- job_id — owning job
- started_at — ISO 8601 timestamp
- finished_at — ISO 8601 timestamp, or empty if in progress
- status — one of: pending / running / succeeded / failed / awaiting_approval / skipped
- worker — name of the worker that ran the stage, e.g. hermes, claude-code, codex
- inputs — repo-relative paths read by this stage
- outputs — repo-relative paths written by this stage
- approvals_requested — list of approval gate IDs requested by this stage
- approvals_received — list of approval gate IDs approved for this stage
- retry_count — integer, default 0
- error — short error string if failed, otherwise null
- log_excerpt — short excerpt of useful log lines (with secrets redacted)
## Approval Sub-Section (in Job Record)
The approvals field is a list of approval entries. Each entry contains:
- gate — one of the six gate IDs defined in APPROVAL_GATES.md
- decision — pending / approved / rejected / changes-requested
- decided_by — name or handle
- decided_at — ISO 8601 timestamp
- notes — short free-form rationale
Approval state for a job is the union of its approval entries. A stage may not begin unless all gates it requires are in the approved state.
## Error Record
File: automation/state/errors/<job-id>.md
Append-only. Each entry:
- stage_id
- occurred_at
- error_class — transient / input / output / external / internal / unrecoverable
- message — short description
- retry_count at time of failure
- resolution — open / retried / escalated / resolved / abandoned
## Timestamps and Time Zones
All timestamps are ISO 8601 with explicit offset. Local times are not stored without offset.
## File Format
Markdown with stable headings is the default. JSON is acceptable for stage records where machine parsing is needed. Mixing formats across job vs stage records is allowed if documented here.
## Portability Rules
- No absolute paths.
- No machine-specific identifiers.
- No secrets in any field.
- No embedded media (paths only).
- No reference to files outside the repo unless that path is documented as local-only in .gitignore.
## Schema Versioning
This schema carries a version field at the top of each record:
- schema_version — integer, currently 1
Records with a higher schema_version than the orchestrator supports must be migrated or refused, never silently reinterpreted.
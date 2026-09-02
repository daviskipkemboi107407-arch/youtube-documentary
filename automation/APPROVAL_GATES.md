# Approval Gates
## Purpose
Define the points where the human (channel owner) must approve before the system advances.
No stage that requires a gate may begin until that gate is in the approved state.
## Gate Roster
| Gate ID | Stage After Which It Applies | What the Human Approves |
|---------|------------------------------|--------------------------|
| story-selection | Story Evaluation | Which candidate story becomes a video |
| research-evidence | Fact Checking | The verified research base is sound enough to write from |
| script | Script Review | The script is publishable-quality and honest |
| visual-asset-plan | Visual Planning | The visual approach and asset plan are acceptable and legal |
| final-video | Quality Control | The rendered video is ready to publish |
| publishing | Publishing | Title, thumbnail, description, tags, schedule are ready and accurate |
## Gate Mechanics
For each gate:
- The orchestrator records a request in the job record with decision: pending.
- The human reviews the linked files and records decision: approved / changes-requested / rejected.
- If changes-requested or rejected, the system returns to the prior stage and re-runs.
- The orchestrator may not skip a gate, may not auto-approve, and may not interpret silence as approval.
## Gate 1 — Story Selection
Approver reviews:
- research/STORY_EVALUATION_TEMPLATE.md (or the filled equivalent)
- Score against docs/STORY_EVALUATION.md
- Channel alignment against docs/CHANNEL_STRATEGY.md
- Any red flags
Decision criteria:
- Total score in a supported band
- No unchecked red flag that disqualifies the story
- Clear central question that fits the channel
## Gate 2 — Research and Evidence
Approver reviews:
- research/<job-id>_research_notes.md (or equivalent)
- Source inventory, reliability ratings, and certainty levels
- Conflict log and unresolved questions
Decision criteria:
- All load-bearing claims are sourced and rated
- Conflicts are documented, not hidden
- Unresolved questions are stated honestly
- No claim depends on excluded content (see docs/CHANNEL_STRATEGY.md)
## Gate 3 — Script
Approver reviews:
- scripts/<job-id>_script.md
- Alignment to approved outline and approved research
Decision criteria:
- Every factual claim is traceable to research
- No red-flagged or excluded framing
- Pacing, transitions, and closing pass the SCRIPT_TEMPLATE.md review checklist
- Restraint and honesty are intact
## Gate 4 — Visual and Asset Plan
Approver reviews:
- production/<job-id>_visual_plan.md (when created)
- License status of every planned asset
- Plan for any generated visuals
Decision criteria:
- Every asset is legally usable
- Visuals support the story, not filler
- No generated visual invents evidence
## Gate 5 — Final Video
Approver reviews:
- production/QUALITY_CONTROL_TEMPLATE.md (or the filled equivalent)
- The rendered video file (or its checksum and duration) referenced by repo-relative local-only path
Decision criteria:
- All QC checklist items resolved
- Audio, pacing, and on-screen text verified
- Title and thumbnail concepts honestly match content
## Gate 6 — Publishing
Approver reviews:
- production/PUBLISHING_METADATA_TEMPLATE.md (or filled equivalent)
- Final title, thumbnail, description, tags, chapters, schedule
- Disclosure if any
Decision criteria:
- All publishing checklist items resolved
- No clickbait, no fabricated framing
- Disclosure complete
- Publishing is the human's action until explicitly delegated
## What Happens After Each Gate
On approval:
- The orchestrator marks the gate approved in the job record
- The next stage becomes eligible
- A short note is appended to the job record
On changes-requested or rejection:
- The orchestrator returns the job to the prior stage
- The job status becomes blocked
- The orchestrator records what was requested
## Default Mode
Until a gate is explicitly defined as delegated, every gate requires human approval. Delegation is a future, documented decision — not an assumption.
#!/usr/bin/env python3
"""
yt — YouTube Documentary state CLI.

First automation layer. Reads and writes the canonical Job, Stage Run, and
Error records defined in automation/STATE_SCHEMA.md, and enforces the
approval gates defined in automation/APPROVAL_GATES.md.

Constraints (per AGENTS.md and the locked plan):
  - Python standard library only.
  - No network, no LLM calls, no Git operations, no scheduler.
  - State files are plain Markdown, repo-relative paths only.
  - Portable across Windows, macOS, Linux, and Android/Termux.

The CLI does no content work. The human (channel owner) drives the
pipeline; this tool records state honestly and refuses invalid transitions.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Constants derived from the project's own design documents.
# Changing these would mean changing those documents; do not do it here.
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1

CHANNEL = "The World Is Stranger Than We Think"

# The 17 pipeline stages from docs/PRODUCTION_WORKFLOW.md, in order.
# Strict enum used by `yt advance --to`.
PIPELINE_STAGES: tuple[str, ...] = (
    "story-discovery",
    "story-evaluation",
    "research",
    "evidence-verification",
    "story-outline",
    "scriptwriting",
    "script-review",
    "narration",
    "visual-planning",
    "asset-collection-or-creation",
    "video-editing",
    "sound-design",
    "quality-control",
    "thumbnail-and-title",
    "upload",
    "performance-review",
    "workflow-improvement",
)
STAGE_IDS = frozenset(PIPELINE_STAGES)

# Human-readable stage names, derived directly from PRODUCTION_WORKFLOW.md.
STAGE_NAMES: dict[str, str] = {
    "story-discovery": "Story Discovery",
    "story-evaluation": "Story Evaluation",
    "research": "Research",
    "evidence-verification": "Evidence Verification",
    "story-outline": "Story Outline",
    "scriptwriting": "Scriptwriting",
    "script-review": "Script Review",
    "narration": "Narration",
    "visual-planning": "Visual Planning",
    "asset-collection-or-creation": "Asset Collection or Creation",
    "video-editing": "Video Editing",
    "sound-design": "Sound Design",
    "quality-control": "Quality Control",
    "thumbnail-and-title": "Thumbnail and Title",
    "upload": "Upload",
    "performance-review": "Performance Review",
    "workflow-improvement": "Workflow Improvement",
}

# Allowed job statuses, from STATE_SCHEMA.md.
JOB_STATUSES = frozenset(
    {"draft", "in_progress", "awaiting_approval", "blocked", "completed", "archived"}
)

# Allowed Stage Run statuses, from STATE_SCHEMA.md.
STAGE_STATUSES = frozenset(
    {"pending", "running", "succeeded", "failed", "awaiting_approval", "skipped"}
)

# Allowed approval decisions, from STATE_SCHEMA.md.
APPROVAL_DECISIONS = frozenset(
    {"pending", "approved", "rejected", "changes-requested"}
)

# Gate-to-stage mapping, from APPROVAL_GATES.md "Stage After Which It Applies" column.
# A gate is required AFTER the named stage finishes and BEFORE the next stage begins.
GATE_AFTER_STAGE: dict[str, str] = {
    "story-selection": "story-evaluation",
    "research-evidence": "evidence-verification",
    "script": "script-review",
    "visual-asset-plan": "visual-planning",
    "final-video": "quality-control",
    "publishing": "upload",
}
GATE_IDS = frozenset(GATE_AFTER_STAGE.keys())


# ---------------------------------------------------------------------------
# Repo and path utilities
# ---------------------------------------------------------------------------

@dataclass
class Repo:
    root: Path  # absolute path to the repo root
    automation_dir: Path  # <root>/automation
    state_dir: Path  # <root>/automation/state
    jobs_dir: Path  # <root>/automation/state/jobs
    stages_dir: Path  # <root>/automation/state/stages
    errors_dir: Path  # <root>/automation/state/errors


def find_repo_root(start: Path) -> Path:
    """Walk upward until we find automation/STATE_SCHEMA.md. This is the
    single source of truth for the repo root — no environment variables,
    no absolute paths stored in state."""
    cur = start.resolve()
    for _ in range(20):  # generous upper bound; bail before infinite loops
        candidate = cur / "automation" / "STATE_SCHEMA.md"
        if candidate.is_file():
            return cur
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    raise RuntimeError(
        "Could not locate repo root: no automation/STATE_SCHEMA.md found above "
        + str(start)
    )


def load_repo() -> Repo:
    here = Path(__file__).resolve()
    root = find_repo_root(here)
    automation = root / "automation"
    state = automation / "state"
    return Repo(
        root=root,
        automation_dir=automation,
        state_dir=state,
        jobs_dir=state / "jobs",
        stages_dir=state / "stages",
        errors_dir=state / "errors",
    )


def ensure_state_dirs(repo: Repo) -> None:
    for d in (repo.state_dir, repo.jobs_dir, repo.stages_dir, repo.errors_dir):
        d.mkdir(parents=True, exist_ok=True)


def to_repo_relative(repo: Repo, p: Path) -> str:
    """Convert an absolute path to a path string relative to the repo root,
    using forward slashes. Used to keep STATE_SCHEMA.md's portability rules."""
    rp = Path(p).resolve()
    return rp.relative_to(repo.root).as_posix()


# ---------------------------------------------------------------------------
# Time handling — ISO 8601 with explicit offset, per STATE_SCHEMA.md.
# ---------------------------------------------------------------------------

def now_iso() -> str:
    """Local-time ISO 8601 with explicit offset. Never naive."""
    dt = datetime.now().astimezone()
    return dt.isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Job record (Markdown) — read/write, conform to STATE_SCHEMA.md.
# ---------------------------------------------------------------------------

JOB_ID_RE = re.compile(r"^video-(\d{3,})$")  # enforces the locked auto-increment rule


@dataclass
class ApprovalEntry:
    gate: str
    decision: str
    decided_by: str
    decided_at: str
    notes: str


@dataclass
class Job:
    job_id: str
    title: str
    channel: str
    created_at: str
    updated_at: str
    current_stage: str
    status: str
    schema_version: int = SCHEMA_VERSION
    approvals: list[ApprovalEntry] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    errors_path: str | None = None
    notes: str = ""
    video_id: str | None = None
    publish_at: str | None = None
    performance: str | None = None

    @property
    def path(self) -> Path:
        # caller passes Repo; we compute path dynamically
        raise NotImplementedError


def next_job_id(repo: Repo) -> str:
    """Find the next video-NNN id by scanning jobs_dir."""
    used: list[int] = []
    if repo.jobs_dir.is_dir():
        for p in repo.jobs_dir.glob("*.md"):
            m = JOB_ID_RE.match(p.stem)
            if m:
                used.append(int(m.group(1)))
    n = (max(used) + 1) if used else 1
    return f"video-{n:03d}"


def job_path(repo: Repo, job_id: str) -> Path:
    if not JOB_ID_RE.match(job_id):
        raise ValueError(
            f"Invalid job_id '{job_id}'. Expected pattern video-NNN (e.g. video-001)."
        )
    return repo.jobs_dir / f"{job_id}.md"


# --- minimal Markdown read/write ------------------------------------------------
# We treat the Job file as the source of truth. The format is plain Markdown with
# stable headings so it stays readable in Acode and diffable in Git.

def write_job(repo: Repo, job: Job) -> None:
    p = job_path(repo, job.job_id)
    lines: list[str] = []
    lines.append("---")
    lines.append(f"schema_version: {job.schema_version}")
    lines.append(f"job_id: {job.job_id}")
    lines.append(f"title: {job.title}")
    lines.append(f"channel: {job.channel}")
    lines.append(f"created_at: {job.created_at}")
    lines.append(f"updated_at: {job.updated_at}")
    lines.append(f"current_stage: {job.current_stage}")
    lines.append(f"status: {job.status}")
    if job.video_id is not None:
        lines.append(f"video_id: {job.video_id}")
    if job.publish_at is not None:
        lines.append(f"publish_at: {job.publish_at}")
    if job.performance is not None:
        lines.append(f"performance: {job.performance}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Job — {job.job_id}")
    lines.append("")
    lines.append("## Inputs")
    if job.inputs:
        for x in job.inputs:
            lines.append(f"- {x}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("## Outputs")
    if job.outputs:
        for x in job.outputs:
            lines.append(f"- {x}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("## Errors")
    if job.errors_path:
        lines.append(f"- {job.errors_path}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("## Notes")
    lines.append(job.notes if job.notes else "(none)")
    lines.append("")
    lines.append("## Approvals")
    if job.approvals:
        lines.append("")
        lines.append("| gate | decision | decided_by | decided_at | notes |")
        lines.append("|------|----------|------------|------------|-------|")
        for a in job.approvals:
            lines.append(
                f"| {a.gate} | {a.decision} | {a.decided_by} | {a.decided_at} | {a.notes} |"
            )
    else:
        lines.append("")
        lines.append("(none)")
    lines.append("")
    p.write_text("\n".join(lines), encoding="utf-8")


def _strip_inline_comment(val: str) -> str:
    # YAML-ish frontmatter lines are simple key: value; we don't parse YAML,
    # we just split on the first colon.
    return val.strip()


def _read_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Return (front_matter_dict, body). Expects --- delimited front matter."""
    if not text.startswith("---\n"):
        raise ValueError("Job file is missing the opening '---' front-matter delimiter.")
    rest = text[4:]
    end = rest.find("\n---")
    if end < 0:
        raise ValueError("Job file is missing the closing '---' front-matter delimiter.")
    fm_block = rest[:end]
    body = rest[end + 4 :].lstrip("\n")
    fm: dict[str, str] = {}
    for line in fm_block.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Malformed front-matter line: {line!r}")
        k, _, v = line.partition(":")
        fm[k.strip()] = _strip_inline_comment(v)
    return fm, body


def _parse_approvals_table(body: str) -> list[ApprovalEntry]:
    entries: list[ApprovalEntry] = []
    in_section = False
    in_table = False
    saw_table = False
    for line in body.splitlines():
        if line.startswith("## "):
            in_section = line.strip() == "## Approvals"
            in_table = False
            continue
        if not in_section:
            continue
        stripped = line.strip()
        if stripped.startswith("|"):
            in_table = True
            saw_table = True
            # skip header and separator rows
            if "gate" in stripped and "decision" in stripped:
                continue
            if re.match(r"^\|[\s\-:|]+\|", stripped):
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 5:
                entries.append(
                    ApprovalEntry(
                        gate=cells[0],
                        decision=cells[1],
                        decided_by=cells[2],
                        decided_at=cells[3],
                        notes=cells[4],
                    )
                )
        elif in_table:
            # left the table
            in_table = False
    if not saw_table:
        # The body said "(none)" — no entries.
        return []
    return entries


def _parse_bullets(body: str, heading: str) -> list[str]:
    in_section = False
    items: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            in_section = line.strip() == heading
            continue
        if not in_section:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == "(none)":
            continue
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def _parse_notes(body: str) -> str:
    in_section = False
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if in_section:
                break
            in_section = line.strip() == "## Notes"
            continue
        if in_section:
            stripped = line.strip()
            if stripped == "(none)":
                continue
            buf.append(line)
    return "\n".join(buf).strip()


def read_job(repo: Repo, job_id: str) -> Job:
    p = job_path(repo, job_id)
    if not p.is_file():
        raise FileNotFoundError(f"No job record at {to_repo_relative(repo, p)}")
    text = p.read_text(encoding="utf-8")
    fm, body = _read_front_matter(text)
    try:
        schema_version = int(fm.get("schema_version", "0"))
    except ValueError:
        raise ValueError(f"schema_version is not an integer in {p}")
    if schema_version > SCHEMA_VERSION:
        raise ValueError(
            f"Job record schema_version={schema_version} is newer than this CLI "
            f"(supports up to {SCHEMA_VERSION}). Refusing to interpret."
        )

    job = Job(
        job_id=fm["job_id"],
        title=fm.get("title", ""),
        channel=fm.get("channel", CHANNEL),
        created_at=fm.get("created_at", ""),
        updated_at=fm.get("updated_at", ""),
        current_stage=fm.get("current_stage", ""),
        status=fm.get("status", ""),
        schema_version=schema_version,
        video_id=fm.get("video_id"),
        publish_at=fm.get("publish_at"),
        performance=fm.get("performance"),
    )
    if job.current_stage not in STAGE_IDS:
        raise ValueError(
            f"current_stage '{job.current_stage}' in {p} is not a valid pipeline stage."
        )
    if job.status not in JOB_STATUSES:
        raise ValueError(f"status '{job.status}' in {p} is not a valid job status.")
    job.approvals = _parse_approvals_table(body)
    job.inputs = _parse_bullets(body, "## Inputs")
    job.outputs = _parse_bullets(body, "## Outputs")
    errs = _parse_bullets(body, "## Errors")
    job.errors_path = errs[0] if errs else None
    job.notes = _parse_notes(body)
    return job


# ---------------------------------------------------------------------------
# Stage Run record — conform to STATE_SCHEMA.md Stage Run section.
# ---------------------------------------------------------------------------

def stage_path(repo: Repo, job_id: str, stage_id: str) -> Path:
    if stage_id not in STAGE_IDS:
        raise ValueError(
            f"Invalid stage_id '{stage_id}'. Must be one of the 17 pipeline stages."
        )
    d = repo.stages_dir / job_id
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{stage_id}.md"


def write_stage_run(
    repo: Repo,
    job_id: str,
    stage_id: str,
    *,
    status: str,
    worker: str,
    started_at: str,
    finished_at: str = "",
    inputs: Iterable[str] = (),
    outputs: Iterable[str] = (),
    approvals_requested: Iterable[str] = (),
    approvals_received: Iterable[str] = (),
    retry_count: int = 0,
    error: str | None = None,
    log_excerpt: str = "",
) -> Path:
    if status not in STAGE_STATUSES:
        raise ValueError(f"Invalid Stage Run status '{status}'.")
    p = stage_path(repo, job_id, stage_id)
    lines: list[str] = []
    lines.append("---")
    lines.append(f"schema_version: {SCHEMA_VERSION}")
    lines.append(f"stage_id: {stage_id}")
    lines.append(f"stage_name: {STAGE_NAMES[stage_id]}")
    lines.append(f"job_id: {job_id}")
    lines.append(f"started_at: {started_at}")
    lines.append(f"finished_at: {finished_at}")
    lines.append(f"status: {status}")
    lines.append(f"worker: {worker}")
    lines.append(f"retry_count: {retry_count}")
    if error is not None:
        lines.append(f"error: {error}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Stage Run — {stage_id} ({STAGE_NAMES[stage_id]})")
    lines.append("")
    lines.append("## Inputs")
    inputs = list(inputs)
    lines.extend([f"- {x}" for x in inputs] if inputs else ["- (none)"])
    lines.append("")
    lines.append("## Outputs")
    outputs = list(outputs)
    lines.extend([f"- {x}" for x in outputs] if outputs else ["- (none)"])
    lines.append("")
    lines.append("## Approvals")
    apr = list(approvals_requested)
    arec = list(approvals_received)
    if apr:
        lines.append("Requested:")
        for g in apr:
            lines.append(f"- {g}")
    if arec:
        lines.append("Received:")
        for g in arec:
            lines.append(f"- {g}")
    if not apr and not arec:
        lines.append("(none)")
    lines.append("")
    lines.append("## Log Excerpt")
    lines.append(log_excerpt if log_excerpt else "(none)")
    lines.append("")
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Error record — append-only, per STATE_SCHEMA.md Error Record section.
# ---------------------------------------------------------------------------

def append_error(repo: Repo, job_id: str, entry: dict[str, str]) -> None:
    repo.errors_dir.mkdir(parents=True, exist_ok=True)
    p = repo.errors_dir / f"{job_id}.md"
    if not p.is_file():
        p.write_text(
            f"# Errors — {job_id}\n\n## Entries\n\n",
            encoding="utf-8",
        )
    rows = (
        f"| {entry['stage_id']} | {entry['occurred_at']} | "
        f"{entry['error_class']} | {entry['message']} | "
        f"{entry['retry_count']} | {entry['resolution']} |\n"
    )
    header_needed = not _errors_table_present(p)
    with p.open("a", encoding="utf-8") as f:
        if header_needed:
            f.write(
                "| stage_id | occurred_at | error_class | message | "
                "retry_count | resolution |\n"
            )
            f.write(
                "|----------|-------------|-------------|---------|"
                "------------|------------|\n"
            )
        f.write(rows)


def _errors_table_present(p: Path) -> bool:
    if not p.is_file():
        return False
    text = p.read_text(encoding="utf-8")
    return "| stage_id |" in text


# ---------------------------------------------------------------------------
# Gate logic — conforms to APPROVAL_GATES.md.
# ---------------------------------------------------------------------------

def gate_required_after(stage_id: str) -> str | None:
    """Return the gate id that must be approved after this stage, or None."""
    for gate, after in GATE_AFTER_STAGE.items():
        if after == stage_id:
            return gate
    return None


def gate_state(job: Job, gate_id: str) -> str:
    """Return the latest decision for a gate on this job, or 'pending' if none."""
    for a in reversed(job.approvals):
        if a.gate == gate_id:
            return a.decision
    return "pending"


def next_stage_after(stage_id: str) -> str | None:
    """The stage immediately following `stage_id` in the pipeline."""
    idx = PIPELINE_STAGES.index(stage_id)
    if idx + 1 >= len(PIPELINE_STAGES):
        return None
    return PIPELINE_STAGES[idx + 1]


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_create(repo: Repo, args: argparse.Namespace) -> int:
    title = args.title.strip()
    if not title:
        print("error: title is required and must be non-empty.", file=sys.stderr)
        return 2
    ensure_state_dirs(repo)
    job_id = next_job_id(repo)
    now = now_iso()
    job = Job(
        job_id=job_id,
        title=title,
        channel=CHANNEL,
        created_at=now,
        updated_at=now,
        current_stage=PIPELINE_STAGES[0],
        status="draft",
    )
    write_job(repo, job)
    rel = to_repo_relative(repo, job_path(repo, job_id))
    print(f"created {job_id} (title: {title})")
    print(f"  record: {rel}")
    print(f"  current_stage: {job.current_stage}")
    print(f"  status: {job.status}")
    print(f"  next action: `yt advance {job_id} --to {job.current_stage}` "
          "to begin Story Discovery.")
    return 0


def _job_summary_lines(job: Job) -> list[str]:
    lines = [
        f"job_id: {job.job_id}",
        f"title: {job.title}",
        f"current_stage: {job.current_stage}",
        f"status: {job.status}",
        f"updated_at: {job.updated_at}",
    ]
    if job.approvals:
        lines.append("approvals:")
        for a in job.approvals:
            lines.append(f"  - {a.gate}: {a.decision} (by {a.decided_by} at {a.decided_at})")
    else:
        lines.append("approvals: (none)")
    return lines


def cmd_status(repo: Repo, args: argparse.Namespace) -> int:
    ensure_state_dirs(repo)
    if args.job_id:
        try:
            job = read_job(repo, args.job_id)
        except FileNotFoundError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        for line in _job_summary_lines(job):
            print(line)
        return 0
    # list all
    jobs = _load_all_jobs(repo)
    if not jobs:
        print("no jobs.")
        return 0
    print(f"{'job_id':<12} {'status':<18} {'stage':<32} title")
    for j in jobs:
        print(
            f"{j.job_id:<12} {j.status:<18} {j.current_stage:<32} {j.title}"
        )
    return 0


def cmd_list(repo: Repo, args: argparse.Namespace) -> int:
    ensure_state_dirs(repo)
    jobs = _load_all_jobs(repo)
    if not jobs:
        print("no jobs.")
        return 0
    print(f"{'job_id':<12} {'status':<18} {'stage':<32} updated_at")
    for j in jobs:
        print(
            f"{j.job_id:<12} {j.status:<18} {j.current_stage:<32} {j.updated_at}"
        )
    return 0


def _load_all_jobs(repo: Repo) -> list[Job]:
    if not repo.jobs_dir.is_dir():
        return []
    out: list[Job] = []
    for p in sorted(repo.jobs_dir.glob("*.md")):
        try:
            out.append(read_job(repo, p.stem))
        except Exception as e:
            # surface the broken record but don't crash the whole listing
            print(f"warning: could not read {p.name}: {e}", file=sys.stderr)
    return out


def cmd_resume(repo: Repo, args: argparse.Namespace) -> int:
    """Read-only: report the next legal action from current state."""
    ensure_state_dirs(repo)
    try:
        job = read_job(repo, args.job_id)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"job_id: {job.job_id}")
    print(f"title: {job.title}")
    print(f"current_stage: {job.current_stage}")
    print(f"status: {job.status}")
    print()

    cur = job.current_stage
    gate = gate_required_after(cur)
    nxt = next_stage_after(cur)

    if job.status == "blocked":
        print("state: blocked")
        print("next legal action:")
        # last approval with a non-approved decision
        last_blocking = None
        for a in reversed(job.approvals):
            if a.decision in ("rejected", "changes-requested"):
                last_blocking = a
                break
        if last_blocking:
            after = GATE_AFTER_STAGE.get(last_blocking.gate, "?")
            print(
                f"  - Review the {last_blocking.gate} rejection on stage "
                f"'{after}' (notes: {last_blocking.notes or '(none)'})."
            )
            print(
                f"  - When ready: `yt advance {job.job_id} --to {after}` "
                "to redo the stage, then re-request approval."
            )
        else:
            print("  - Inspect the job record for the blocking condition.")
        return 0

    if job.status == "completed":
        print("state: completed")
        print("next legal action: none — job has finished the pipeline.")
        return 0

    if job.status == "archived":
        print("state: archived")
        print("next legal action: none — archived jobs are immutable.")
        return 0

    # active path
    print("next legal action:")
    if gate is None:
        # no gate after current stage — just advance.
        if nxt is None:
            print(f"  - `yt advance {job.job_id} --to {cur}` to mark this stage complete, "
                  "then the job will be `completed`.")
        else:
            print(f"  - Finish the '{cur}' work, then:")
            print(f"      `yt advance {job.job_id} --to {nxt}`")
    else:
        # a gate is required after this stage
        decision = gate_state(job, gate)
        if decision != "approved":
            print(
                f"  - Perform the '{cur}' stage. The '{gate}' gate must be "
                "approved before advancing."
            )
            print(
                f"  - When the stage work is done: "
                f"`yt advance {job.job_id} --to {cur}` to mark it complete."
            )
            print(
                f"  - Then: `yt approve {job.job_id} --gate {gate}` "
                "to record approval and unblock the next stage."
            )
        else:
            # gate is approved — the human still needs to advance
            if nxt is None:
                print(f"  - `yt advance {job.job_id} --to {cur}` to mark final stage complete "
                      "(this will mark the job completed).")
            else:
                print(f"  - Gate '{gate}' is approved. Next stage is '{nxt}'.")
                print(f"  - `yt advance {job.job_id} --to {nxt}` to begin it.")

    print()
    print("note: edit the state file directly only as a last resort. "
          "All transitions should go through `yt`.")
    return 0


def _require_active(job: Job) -> None:
    if job.status in ("completed", "archived"):
        raise RuntimeError(
            f"job {job.job_id} is '{job.status}'; no transitions allowed. "
            "Use `yt resume` to see the next legal action."
        )
    # 'blocked' is allowed: the human must be able to re-run the stage after
    # a rejection. The legitimate next move is `yt advance --to <current>` to
    # restart the stage, then close it again, then re-request approval.


def cmd_advance(repo: Repo, args: argparse.Namespace) -> int:
    """Advance the pipeline. This is the ONE authoritative transition mechanism.

    Semantics:
      - If --to equals the current stage: mark the current stage complete
        (close its Stage Run), set job status to 'awaiting_approval' if a
        gate is required after it, else set to 'in_progress' on the same stage
        until the next advance. If no further stage exists, mark job completed.
      - If --to equals the NEXT stage and the gate (if any) for the current
        stage is approved: move into --to, set status to 'in_progress',
        create the new Stage Run.
      - Otherwise: refuse.
    """
    ensure_state_dirs(repo)
    try:
        job = read_job(repo, args.job_id)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    target = args.to
    if target not in STAGE_IDS:
        print(
            f"error: --to must be one of the 17 pipeline stages. Got '{target}'.",
            file=sys.stderr,
        )
        print("valid stages:", ", ".join(PIPELINE_STAGES), file=sys.stderr)
        return 2

    _require_active(job)
    cur = job.current_stage
    nxt = next_stage_after(cur)
    now = now_iso()

    # Case A: target equals current stage.
    #   - If there is no existing Stage Run for this stage, this is the BEGIN
    #     action: create a running Stage Run.
    #   - If a Stage Run exists and is 'running', this is the CLOSE action:
    #     mark it succeeded (or awaiting_approval if a gate is required after
    #     this stage). The job status becomes 'awaiting_approval' in the gate
    #     case, else 'in_progress' ready for the next advance.
    if target == cur:
        sp = stage_path(repo, job.job_id, cur)
        existing_status: str | None = None
        if sp.is_file():
            existing_text = sp.read_text(encoding="utf-8")
            for line in existing_text.splitlines():
                if line.startswith("status:"):
                    existing_status = line.split(":", 1)[1].strip()
                    break
        if existing_status == "running":
            # CLOSE the stage
            gate = gate_required_after(cur)
            new_stage_status = "awaiting_approval" if gate else "succeeded"
            text = sp.read_text(encoding="utf-8")
            new_lines = []
            for line in text.splitlines():
                if line.startswith("status:"):
                    new_lines.append(f"status: {new_stage_status}")
                elif line.startswith("finished_at:"):
                    new_lines.append(f"finished_at: {now}")
                else:
                    new_lines.append(line)
            sp.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            if gate:
                job.status = "awaiting_approval"
            elif cur == PIPELINE_STAGES[-1]:
                # final stage closed out without a gate
                job.status = "completed"
            else:
                # no gate after this stage, more stages follow — keep active
                job.status = "in_progress"
            job.updated_at = now
            write_job(repo, job)
            if cur == PIPELINE_STAGES[-1]:
                print(f"{job.job_id}: final stage '{cur}' closed. Job completed.")
                return 0
            nxt = next_stage_after(cur)
            print(f"{job.job_id}: stage '{cur}' closed (status: {new_stage_status}).")
            if gate:
                print(
                    f"  next action: `yt approve {job.job_id} --gate {gate}` "
                    f"to record approval, then `yt advance {job.job_id} --to {nxt}`."
                )
            else:
                print(f"  next action: `yt advance {job.job_id} --to {nxt}`.")
            return 0

        # BEGIN the stage (file may be 'pending' from a prior advance-into,
        # or absent altogether). Mark the Stage Run running.
        if sp.is_file():
            text = sp.read_text(encoding="utf-8")
            new_lines = []
            for line in text.splitlines():
                if line.startswith("status:"):
                    new_lines.append("status: running")
                elif line.startswith("started_at:"):
                    new_lines.append(f"started_at: {now}")
                else:
                    new_lines.append(line)
            sp.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        else:
            write_stage_run(
                repo,
                job.job_id,
                cur,
                status="running",
                worker="human",
                started_at=now,
                inputs=job.inputs,
            )
        job.status = "in_progress"
        job.updated_at = now
        write_job(repo, job)
        print(f"{job.job_id}: stage '{cur}' is now running.")
        return 0

    # Case B: moving forward to the next stage.
    if target != nxt:
        print(
            f"error: invalid transition. current_stage is '{cur}'. The only "
            f"allowed target is the current stage (re-enter) or the immediate "
            f"next stage '{nxt}'. Skipping stages is forbidden.",
            file=sys.stderr,
        )
        return 2

    # We're moving to nxt. Gate enforcement per APPROVAL_GATES.md.
    gate = gate_required_after(cur)
    if gate is not None and gate_state(job, gate) != "approved":
        print(
            f"error: cannot advance to '{nxt}'. Gate '{gate}' is required "
            "after stage '" + cur + "' and is not yet approved.",
            file=sys.stderr,
        )
        print(
            f"hint: complete '{cur}', then `yt approve {job.job_id} --gate {gate}`.",
            file=sys.stderr,
        )
        return 2

    # Close out the previous stage's Stage Run as 'succeeded'.
    prev_path = stage_path(repo, job.job_id, cur)
    if prev_path.is_file():
        # Re-read and rewrite as succeeded; simplest is to append a new run
        # record tracking the close. To keep things honest, we open the
        # existing file and update finished_at + status in-place.
        text = prev_path.read_text(encoding="utf-8")
        # find the front-matter 'status:' and 'finished_at:' lines
        new_lines: list[str] = []
        for line in text.splitlines():
            if line.startswith("status:") and "running" in line:
                new_lines.append("status: succeeded")
            elif line.startswith("finished_at:"):
                new_lines.append(f"finished_at: {now}")
            else:
                new_lines.append(line)
        prev_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    # Open the new stage's Stage Run in 'pending' state. The human must call
    # `yt advance --to <this-stage>` again to mark it running (begin work).
    write_stage_run(
        repo,
        job.job_id,
        target,
        status="pending",
        worker="human",
        started_at=now,
        inputs=job.inputs,
        approvals_received=[gate] if gate else (),
    )

    job.current_stage = target
    job.updated_at = now
    job.status = "in_progress"
    write_job(repo, job)

    # Final stage entered — but we still need a closing advance to mark
    # the job completed. That's a follow-up call.
    if target == PIPELINE_STAGES[-1]:
        print(
            f"{job.job_id}: entered final stage '{target}' (status: pending)."
        )
        print(
            f"  next action: `yt advance {job.job_id} --to {target}` to begin it."
        )
    else:
        print(f"{job.job_id}: advanced '{cur}' -> '{target}' (status: pending).")
        print(
            f"  next action: `yt advance {job.job_id} --to {target}` to begin work."
        )
    return 0


def _resolve_approver(args: argparse.Namespace) -> str:
    if getattr(args, "by", None):
        return args.by.strip()
    # fall back to environment, then OS user
    by = os.environ.get("YT_APPROVER") or os.environ.get("USER") or os.environ.get("USERNAME")
    return (by or "human").strip() or "human"


def cmd_approve(repo: Repo, args: argparse.Namespace) -> int:
    ensure_state_dirs(repo)
    try:
        job = read_job(repo, args.job_id)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    gate = args.gate
    if gate not in GATE_IDS:
        print(
            f"error: --gate must be one of {sorted(GATE_IDS)}. Got '{gate}'.",
            file=sys.stderr,
        )
        return 2

    # Approval gate enforcement per APPROVAL_GATES.md and the locked plan:
    # `yt approve` ONLY records approval; it must NOT independently move stages.
    after_stage = GATE_AFTER_STAGE[gate]
    if job.current_stage != after_stage:
        print(
            f"error: gate '{gate}' applies after stage '{after_stage}', but the "
            f"job is currently at '{job.current_stage}'. Refusing to record an "
            "approval that does not correspond to the active transition.",
            file=sys.stderr,
        )
        return 2

    if job.status not in ("awaiting_approval", "blocked"):
        # Approval must follow a close-out. `yt advance --to <current>` on a
        # running stage flips status to 'awaiting_approval' (when a gate is
        # required). 'blocked' is allowed so a re-attempt after a prior
        # rejection can be recorded once the work has been redone and the
        # stage re-closed.
        print(
            f"error: job status is '{job.status}'. Approvals are accepted only "
            "after the current stage has been closed with `yt advance --to <current>`, "
            "which sets status to 'awaiting_approval'.",
            file=sys.stderr,
        )
        return 2

    now = now_iso()
    approver = _resolve_approver(args)
    notes = (args.notes or "").strip()

    job.approvals.append(
        ApprovalEntry(
            gate=gate,
            decision="approved",
            decided_by=approver,
            decided_at=now,
            notes=notes,
        )
    )
    # Mark the gate's closing Stage Run as approved (if it exists).
    stage_p = stage_path(repo, job.job_id, after_stage)
    if stage_p.is_file():
        text = stage_p.read_text(encoding="utf-8")
        new_lines: list[str] = []
        for line in text.splitlines():
            if line.startswith("status:") and "awaiting_approval" in line:
                new_lines.append("status: succeeded")
            else:
                new_lines.append(line)
        stage_p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    # Approval only records the decision; the actual stage transition is
    # done by `yt advance`. Status returns to 'in_progress' so the next
    # `yt advance --to <next>` is accepted.
    job.status = "in_progress"
    job.updated_at = now
    write_job(repo, job)

    nxt = next_stage_after(after_stage)
    print(f"{job.job_id}: recorded approval for gate '{gate}' (by {approver}).")
    if nxt:
        print(f"  next stage '{nxt}' is now eligible.")
        print(f"  next action: `yt advance {job.job_id} --to {nxt}`")
    else:
        print(f"  '{after_stage}' is the final stage; close it out with "
              f"`yt advance {job.job_id} --to {after_stage}`.")
    return 0


def cmd_reject(repo: Repo, args: argparse.Namespace) -> int:
    ensure_state_dirs(repo)
    try:
        job = read_job(repo, args.job_id)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    gate = args.gate
    if gate not in GATE_IDS:
        print(
            f"error: --gate must be one of {sorted(GATE_IDS)}. Got '{gate}'.",
            file=sys.stderr,
        )
        return 2

    after_stage = GATE_AFTER_STAGE[gate]
    if job.current_stage != after_stage:
        print(
            f"error: gate '{gate}' applies after stage '{after_stage}', but the "
            f"job is currently at '{job.current_stage}'.",
            file=sys.stderr,
        )
        return 2

    if job.status not in ("awaiting_approval", "blocked"):
        print(
            f"error: job status is '{job.status}'. Rejections are accepted only "
            "after the current stage has been closed with `yt advance --to <current>`, "
            "which sets status to 'awaiting_approval'.",
            file=sys.stderr,
        )
        return 2

    decision = "changes-requested" if args.changes else "rejected"
    now = now_iso()
    approver = _resolve_approver(args)
    notes = (args.notes or "").strip()

    job.approvals.append(
        ApprovalEntry(
            gate=gate,
            decision=decision,
            decided_by=approver,
            decided_at=now,
            notes=notes,
        )
    )
    job.status = "blocked"
    job.updated_at = now
    write_job(repo, job)

    print(f"{job.job_id}: recorded '{decision}' for gate '{gate}' (by {approver}).")
    print(f"  job status is now 'blocked'.")
    print(f"  next action: redo stage '{after_stage}', then re-request approval.")
    return 0


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="yt",
        description="YouTube Documentary state CLI (first automation layer).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create a new job.")
    p_create.add_argument("title", help="Working title / topic.")
    p_create.set_defaults(func=cmd_create)

    p_status = sub.add_parser("status", help="Show one job or list all.")
    p_status.add_argument("job_id", nargs="?", help="Job id; omit to list all.")
    p_status.set_defaults(func=cmd_status)

    p_list = sub.add_parser("list", help="List all jobs.")
    p_list.set_defaults(func=cmd_list)

    p_resume = sub.add_parser("resume", help="Show the next legal action (read-only).")
    p_resume.add_argument("job_id", help="Job id.")
    p_resume.set_defaults(func=cmd_resume)

    p_advance = sub.add_parser(
        "advance",
        help=(
            "Advance the pipeline. The single authoritative transition mechanism. "
            "--to is the stage to move INTO (must equal current_stage to begin work, "
            "or the immediate next stage to move forward)."
        ),
    )
    p_advance.add_argument("job_id", help="Job id.")
    p_advance.add_argument(
        "--to", required=True,
        help="Target stage. Must be one of the 17 pipeline stages.",
    )
    p_advance.set_defaults(func=cmd_advance)

    p_approve = sub.add_parser(
        "approve",
        help=(
            "Record a gate approval. Does NOT move stages by itself; only marks "
            "the gate approved so a subsequent `yt advance` can transition."
        ),
    )
    p_approve.add_argument("job_id", help="Job id.")
    p_approve.add_argument(
        "--gate", required=True,
        help="Gate id. One of: " + ", ".join(sorted(GATE_IDS)),
    )
    p_approve.add_argument("--notes", default="", help="Optional short rationale.")
    p_approve.add_argument(
        "--by", default=None,
        help="Approver name/handle. Defaults to $YT_APPROVER or the OS user.",
    )
    p_approve.set_defaults(func=cmd_approve)

    p_reject = sub.add_parser(
        "reject",
        help=(
            "Record a gate rejection (or changes-requested). Sets job to 'blocked'."
        ),
    )
    p_reject.add_argument("job_id", help="Job id.")
    p_reject.add_argument(
        "--gate", required=True,
        help="Gate id. One of: " + ", ".join(sorted(GATE_IDS)),
    )
    p_reject.add_argument(
        "--changes", action="store_true",
        help="Record as 'changes-requested' instead of 'rejected'.",
    )
    p_reject.add_argument("--notes", default="", help="Optional short rationale.")
    p_reject.add_argument(
        "--by", default=None,
        help="Approver name/handle. Defaults to $YT_APPROVER or the OS user.",
    )
    p_reject.set_defaults(func=cmd_reject)

    return p


def main(argv: list[str] | None = None) -> int:
    repo = load_repo()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(repo, args))
    except (RuntimeError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
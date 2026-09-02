#!/usr/bin/env bash
# Smoke test for the yt CLI. Wipes state first, then exercises every command
# plus the invalid-transition refusals the locked plan calls out.
set -e
cd "$(dirname "$0")/.."

rm -f automation/state/jobs/video-001.md automation/state/jobs/video-002.md
rm -rf automation/state/stages/video-001 automation/state/stages/video-002
rm -f automation/state/errors/video-001.md automation/state/errors/video-002.md

echo "=== T1. CREATE video-001 + video-002 ==="
python scripts/yt.py create "The Signal That Wasn't"
python scripts/yt.py create "Deep Sea Anomaly"

echo
echo "=== T2. STATUS / LIST ==="
python scripts/yt.py status
python scripts/yt.py list

echo
echo "=== T3. RESUME video-001 ==="
python scripts/yt.py resume video-001

echo
echo "=== T4. Begin story-discovery ==="
python scripts/yt.py advance video-001 --to story-discovery

echo
echo "=== T5. Skip ahead (must refuse) ==="
set +e
python scripts/yt.py advance video-001 --to research
echo "  exit=$?"
set -e

echo
echo "=== T6. Bogus stage (must refuse) ==="
set +e
python scripts/yt.py advance video-001 --to nope
echo "  exit=$?"
set -e

echo
echo "=== T7. Close story-discovery (no gate) ==="
python scripts/yt.py advance video-001 --to story-discovery

echo
echo "=== T8. Advance into story-evaluation ==="
python scripts/yt.py advance video-001 --to story-evaluation

echo
echo "=== T9. Begin story-evaluation ==="
python scripts/yt.py advance video-001 --to story-evaluation

echo
echo "=== T10. Try to advance past gate (must refuse) ==="
set +e
python scripts/yt.py advance video-001 --to research
echo "  exit=$?"
set -e

echo
echo "=== T11. Wrong-gate approve (must refuse) ==="
set +e
python scripts/yt.py approve video-001 --gate script
echo "  exit=$?"
set -e

echo
echo "=== T12. Close story-evaluation -> awaiting_approval ==="
python scripts/yt.py advance video-001 --to story-evaluation
echo "status now:"
python scripts/yt.py status video-001 | grep -E '^(current_stage|status):'

echo
echo "=== T13. APPROVE story-selection (records approval only) ==="
python scripts/yt.py approve video-001 --gate story-selection --notes "Central question clear and falsifiable"
echo "current_stage should still be story-evaluation:"
grep '^current_stage:' automation/state/jobs/video-001.md

echo
echo "=== T14. Approve while not awaiting_approval (must refuse on a fresh job) ==="
set +e
python scripts/yt.py approve video-002 --gate story-selection
echo "  exit=$?"
set -e

echo
echo "=== T15. RESUME after approval -> next stage eligible ==="
python scripts/yt.py resume video-001

echo
echo "=== T16. Advance into research ==="
python scripts/yt.py advance video-001 --to research
echo "status now:"
python scripts/yt.py status video-001 | grep -E '^(current_stage|status):'

echo
echo "=== T17. REJECT flow on video-002 ==="
python scripts/yt.py advance video-002 --to story-discovery
python scripts/yt.py advance video-002 --to story-discovery
python scripts/yt.py advance video-002 --to story-evaluation
python scripts/yt.py advance video-002 --to story-evaluation
python scripts/yt.py advance video-002 --to story-evaluation
echo "reject with --changes (changes-requested):"
python scripts/yt.py reject video-002 --gate story-selection --changes --notes "Need stronger evidence pull"
echo "status now:"
python scripts/yt.py status video-002 | grep -E '^(current_stage|status):'

echo
echo "=== T18. RESUME blocked job ==="
python scripts/yt.py resume video-002

echo
echo "=== T19. Full reject (without --changes) on a new attempt ==="
# redo: begin again, close again, then reject for real
python scripts/yt.py advance video-002 --to story-evaluation
python scripts/yt.py advance video-002 --to story-evaluation
python scripts/yt.py reject video-002 --gate story-selection --notes "Topic falls under channel exclusions"
echo "status now:"
python scripts/yt.py status video-002 | grep -E '^(current_stage|status):'

echo
echo "=== T20. Approve wrong gate on blocked job (must refuse) ==="
set +e
python scripts/yt.py approve video-002 --gate research-evidence
echo "  exit=$?"
set -e

echo
echo "=== T21. RESUME on unknown job (must refuse) ==="
set +e
python scripts/yt.py resume video-999
echo "  exit=$?"
set -e

echo
echo "=== T22. Bash wrapper ==="
bash scripts/yt status video-001 | head -3

echo
echo "=== T23. Final tree ==="
find automation/state -type f | sort
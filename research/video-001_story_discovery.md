# Story Discovery — Video 1

Video ID: video-001
Researcher: channel owner
Date: 2026-09-02
Source of this file: docs/STORY_EVALUATION.md, docs/CHANNEL_STRATEGY.md

## Channel Identity (working summary)

**The World Is Stranger Than We Think** — faceless documentary channel built around reality itself: the parts of it that don't behave the way we expect, and the questions that honest science has not yet closed.

Content areas: real-world science, unexplained phenomena, space mysteries, extreme environments, strange organisms, scientific discoveries, reality-challenging questions.

Unifying question: *what is actually going on here, and what would it take to know?*

## Explicit Exclusions (channel policy)

Do not produce stories that:
- center on religion, gods, deities, or theology
- present paranormal claims as established fact
- promote conspiracy theories, fabricated mysteries, or unsolved-for-entertainment framing
- depend on unsupported clickbait, invented mysteries, or speculation presented as evidence
- are generic science explainers with no compelling central question or story

## Goal of this document

Generate a candidate pool that genuinely fits the channel, evaluate each candidate against `docs/STORY_EVALUATION.md`, and shortlist the top three for human review. **This document does not commit to a final story.** That decision belongs to the Story Selection gate.

## Generation Method

Candidates were generated from three angles, then filtered against the channel exclusions:

1. **Long-running scientific mysteries with new evidence** — questions where established research has produced a real puzzle, and where the channel's "what would it take to know" framing fits naturally.
2. **Strange phenomena with documented, peer-reviewed, or institutional records** — events or measurements that resist clean explanation but have a real evidence base.
3. **Forgotten or under-told historical anomalies** — incidents that mainstream documentary channels have under-treated, leaving room for an original angle.

Rejected without detailed evaluation: any story dependent on paranormal-as-fact framing, conspiratorial framing, theology, or pure speculation.

## Candidate Pool (12 candidates)

Short summaries below; full evaluations in `research/video-001_story_evaluations.md`.

| # | Working title | Angle |
|---|---|---|
| 01 | The Fast Radio Burst That Would Not Repeat | FRB research, localization, repeaters vs. one-offs |
| 02 | The Taos Hum | Persistent low-frequency hum reported in Taos, NM |
| 03 | The Place Where Gravity Is Slightly Wrong | Gravity anomalies (BIFROST, Hudson Bay, arctic surveys) |
| 04 | The Octopus That Edits Its Own RNA | Cephalopod coleoid RNA editing — alien-like cognition |
| 05 | The Cell That Survived 28,000 Years | Pleistocene organism revival research |
| 06 | The Microbe That Eats Metal | Shewanella / Geobacter — extracellular electron transport |
| 07 | The Forest That Remembers Without a Brain | Slime mold memory, mycorrhizal signaling |
| 08 | The Ice That Glows Blue in Antarctica | Brine inclusions, optical scattering |
| 09 | The Star That Dimmed and Nobody Knows Why | Tabby's Star (KIC 8462852) — what's left of the case |
| 10 | The Tunguska Mystery, Honestly | 1908 Siberia event, current scientific consensus |
| 11 | The Mariana Trench's Impossible Microbes | Hadal zone life at extreme pressure |
| 12 | The Voynich Manuscript as a Code Problem | Statistical linguistics approach, not mysticism |

## Scoring Method

Each candidate was scored on the eight categories from `docs/STORY_EVALUATION.md` (Curiosity, Evidence, Narrative, Originality, Visual Potential, Audience Appeal, Factual Confidence, Production Feasibility). Total max = 80. Decision bands:
- 70–80: exceptional
- 60–69: strong
- 50–59: potential, needs an angle
- Below 50: deprioritize

Red flags from the rubric were checked for each candidate.

## Results Summary

See `research/video-001_story_evaluations.md` for the per-candidate detail. Headline results:

| Rank | Title | Total | Band | Red flags |
|---|---|---|---|---|
| 1 | The Fast Radio Burst That Would Not Repeat | 72 | exceptional | none |
| 2 | The Cell That Survived 28,000 Years | 70 | exceptional | none |
| 3 | The Microbe That Eats Metal | 67 | strong | none |
| 4 | The Octopus That Edits Its Own RNA | 64 | strong | minor (well-covered ground; angle must be fresh) |
| 5 | The Star That Dimmed and Nobody Knows Why | 62 | strong | needs careful updated evidence — many outdated docs |
| 6 | The Place Where Gravity Is Slightly Wrong | 60 | strong | needs concrete narrative hook |
| 7 | The Mariana Trench's Impossible Microbes | 58 | potential | well-covered; needs specific angle |
| 8 | The Forest That Remembers Without a Brain | 55 | potential | significant visual potential, narrative risk |
| 9 | The Ice That Glows Blue in Antarctica | 52 | potential | narrow subject, padding risk |
| 10 | The Tunguska Mystery, Honestly | 50 | potential | well-covered; needs original angle |
| 11 | The Taos Hum | 46 | deprioritize | low factual confidence in causes |
| 12 | The Voynich Manuscript as a Code Problem | 43 | deprioritize | high visual/narrative risk |

## Recommendations

Top 3 for human review:
1. **The Fast Radio Burst That Would Not Repeat** — strongest score, original angle (focus on the *repeaters vs. one-offs* debate and what recent localizations have changed), evidence-rich.
2. **The Cell That Survived 28,000 Years** — high narrative potential, original angle (focus on what "revival" actually means vs. the clickbait framing), strong visual potential.
3. **The Microbe That Eats Metal** — strong evidence base, original angle (extracellular electron transport as a possible foundation for new technologies and as a window into early life).

Each of the top 3 has at least one clear "what would it take to know?" question that fits the channel's identity.

## Final Decision

**Deferred to the Story Selection gate.** The Story Discovery stage ends here; Story Evaluation and the Story Selection gate are the next steps. No candidate has been pre-selected.

## Files in this Story Discovery set

- `research/video-001_story_discovery.md` (this file) — candidate pool and rationale
- `research/video-001_story_evaluations.md` — per-candidate scoring and notes
- (no changes to governing docs in `docs/`, `automation/`, or anywhere else)

## Next Action (when this stage is closed)

When Story Discovery is complete, close the stage with:
`yt advance video-001 --to story-discovery`

Then move into Story Evaluation by running:
`yt advance video-001 --to story-evaluation`

Stage status: NOT closed. Awaiting human review of this candidate pool.
# Story Evaluation Decision — Video 1

Video ID: video-001
Researcher: channel owner
Date: 2026-09-02
Stage: story-evaluation (running)
Source of this file: docs/STORY_EVALUATION.md, docs/CHANNEL_STRATEGY.md, research/video-001_story_discovery.md, research/video-001_story_evaluations.md

## Purpose

Critically review the candidate pool produced during Story Discovery (`research/video-001_story_discovery.md`, `research/video-001_story_evaluations.md`) and produce a single recommended story for `video-001`. This is the input the human will review at the `story-selection` approval gate after this stage is closed.

This document does **not** record the final approval. The human closes the stage, then runs `yt approve video-001 --gate story-selection` (or `yt reject`).

---

## 1. Finalists Considered

From the 12-candidate pool, three finalists were re-examined critically:

| Finalist | Working title | Initial total (discovery) |
|---|---|---|
| F1 | The Fast Radio Burst That Would Not Repeat | 72 (exceptional) |
| F2 | The Microbe That Eats Metal | 65 (strong) |
| F3 | The Cell That Survived **24,000** Years (title corrected from 28,000 — see §4) | 63 (strong) |

A fourth candidate was kept as a serious fallback because it sat just outside the top 3 on the recomputed totals and the original recommendation's logic deserves a second look:

| Finalist | Working title | Initial total (discovery) |
|---|---|---|
| F4 | The Star That Dimmed and Nobody Knows Why | 63 (strong) — same total as F3 |

The remaining eight candidates (Place Where Gravity Is Slightly Wrong, Forest That Remembers Without a Brain, Ice That Glows Blue in Antarctica, Mariana Trench's Impossible Microbes, Tunguska Mystery Honestly, Voynich Manuscript, Taos Hum, and the Octopus RNA editing story) were not promoted to finalists. Reasoning is in the "Out-of-Finalists Notes" section below.

---

## 2. Comparative Scores / Reasoning

### 2.1 Re-scoring methodology

The previous evaluation contained several arithmetic inconsistencies and at least one category score that did not match the justification (the Microbe candidate had its Visual Potential noted as "exceptional" in prose but scored as an 8 in the table; the Cell candidate's Production Feasibility was scored 6 but the prose said "high"). This re-evaluation:

1. Re-reads each finalist's evidence basis critically rather than accepting it on authority.
2. Re-scores each of the eight rubric categories from `docs/STORY_EVALUATION.md` independently.
3. Documents the *delta* against the prior score so the change is auditable.
4. Explicitly checks each finalist against each of the seven rubric red flags *and* against each of the five channel exclusions.

### 2.2 Re-scored totals

| Category | F1 FRB | F2 Microbe | F3 Cell | F4 Star |
|---|---|---|---|---|
| Curiosity | 9 | 9 | 8 | 9 |
| Evidence | 9 | 9 | 8 | 8 |
| Narrative | 9 | 8 | 9 | 9 |
| Originality | 8 | 8 | 9 | 7 |
| Visual Potential | 8 | 9 | 9 | 6 |
| Audience Appeal | 8 | 8 | 8 | 9 |
| Factual Confidence | 8 | 8 | 8 | 7 |
| Production Feasibility | 8 | 7 | 7 | 8 |
| **Total (max 80)** | **67** | **66** | **66** | **63** |
| **Band** | strong | strong | strong | strong |
| **Prior total** | 72 | 65 | 63 | 63 |
| **Delta** | -5 | +1 | +3 | 0 |

### 2.3 Why each finalist's score moved (or didn't)

**F1 — Fast Radio Burst (72 → 67).** The downward revision is honest correction, not devaluation. On re-read, the prior score of 72 (exceptional band) was a stretch. Curiosity at 9 is right — the question is sharp. Evidence at 9 is right — CHIME catalog and ASKAP papers are real. But Originality at 8 was over-generous: the post-2020 repeater-vs-non-repeater split is fresh, but FRBs as a *category* are very well-covered on YouTube; the channel's angle must specifically be the post-localization reframing, which is a narrower original-angle surface than "the FRB mystery." Visual Potential at 8 holds — waterfall plots and sky maps are real but limited in variety. Audience Appeal at 8 reflects that the audience has been over-served on FRBs already; the channel must convince them to watch again. Production Feasibility at 8 holds. Net: a *strong* candidate with a sharp, original angle, not an *exceptional* one.

**F2 — Microbe That Eats Metal (65 → 66).** Marginal upward revision. The Visual Potential score moves from 8 to 9: SEM imagery of bacterial nanowires is legitimately exceptional and the animation surface for the cytochrome chain is large. The astrobiology tie-in (which I had weighted into Originality) keeps that score at 8, not 9, because astrobiology docs exist and the framing is differentiating but not unprecedented. Production Feasibility at 7 reflects the animation discipline required — molecular-scale scenes need to be either hand-drawn diagrams or 3D animations that don't invent detail. Total stays in the strong band.

**F3 — Cell That Survived 28,000 Years (63 → 66).** The largest upward revision, and the most carefully justified. On re-read, my prior concern about Production Feasibility (6) was wrong — the microscopy and permafrost imagery is accessible. The Originality score moves to 9: the *anti-clickbait scientific framing* is genuinely under-treated on YouTube. Most channels that touch permafrost revival default to the tabloid framing; a doc that explicitly defines what "revival" means scientifically is rare. Visual Potential moves to 9: time-lapse microscopy of rehydration, permafrost cores, and the biophysics of vitrification give a strong visual surface. The strongest single reason this candidate scores well: it directly operationalizes the channel's distinguishing feature — restraint and honesty about what the science actually says versus what the headline claims.

**F4 — Star That Dimmed and Nobody Knows Why (63, unchanged).** The total did not move, but the *concerns* sharpened. Visual Potential at 6 reflects a real limitation: the Kepler light curve is iconic but the rest of the visual surface is dominated by reconstructions and animations, which are higher-risk for the channel's "no fabricated evidence" rule. Factual Confidence at 7 reflects the need to be precise about which hypotheses have been ruled out by 2025 — older docs are visibly wrong on this. R8 risk (presenting speculation as fact) is the live concern with this story.

### 2.4 Comparative reasoning

After re-scoring, the gap between F1, F2, and F3 is small (one point). The differentiator must therefore come from the rubric's *qualitative* dimensions, not the totals alone. The rubric explicitly says: "The numerical score is a decision aid, not an automatic approval system. A high score does not guarantee production. Human judgment remains responsible for the final decision."

The qualitative differentiators:

- **Channel identity fit.** All four finalists fit well. F3 (the Cell story) operationalizes the channel's restraint identity most directly because the central narrative move is "here's what the science actually says, versus the headline." That is the channel's stated distinguishing feature.
- **Evidence base durability.** F1 (FRBs) and F3 (permafrost revival) have primary literature that will not be invalidated by next week's press cycle. F2 (geomicrobiology) is similarly durable. F4 (Tabby's Star) is at higher risk of mid-production obsolescence — the light curve story has had multiple "the mystery is solved" news cycles and a future publication could shift the narrative.
- **Visual evidence breadth.** F2 and F3 have the widest legitimate visual surfaces (SEM, microscopy, animations, fieldwork). F1 is more constrained (sky maps, telescope imagery, plots). F4 is the most constrained.
- **Three-act sustainability.** F1, F3, and F4 have strong three-act structures. F2 has the cleanest but slightly more technical three-act — the danger is the middle act (molecular mechanism) losing non-specialist viewers.
- **Risk of speculation.** F4 carries the highest speculation risk (Tabby's Star's alien-megastructure framing is famous for a reason). F1's speculation risk is real but more diffuse. F2 and F3 carry the lowest speculation risk because the underlying science is settled and the *interpretation* — not the underlying claims — is where the storytelling lives.

---

## 3. Strongest Risks (by finalist)

### F1 — Fast Radio Burst

- **Speculation risk:** the broader FRB discourse drifts toward "alien signals." The script must explicitly reject that framing without using it as clickbait.
- **Originality risk:** the angle must be the post-2020 repeater-vs-non-repeater split, not the generic FRB mystery. Generic coverage is saturated.
- **Currency risk:** the science moves fast. Older papers' conclusions may be outdated; the script must cite 2020–2025 sources.

### F2 — Microbe That Eats Metal

- **Animation discipline:** the molecular-scale visualization surface is large, and any generated visuals that invent detail violate the channel's honesty standards. Every animation must correspond to a published structure or mechanism.
- **Specialist trap:** the middle act (cytochrome chain / nanowire electron transfer) can lose non-specialist viewers. Pacing discipline is essential.
- **Subject unfamiliarity:** audiences may not know what a microbe "eating" metal means visually. The opening must establish the phenomenon clearly without dumbing it down.

### F3 — Cell That Survived 28,000 Years

- **Headline drift:** the temptation is to lean into "ancient worm lives" framing for the thumbnail. The script must not.
- **Narrow subject:** the core phenomenon is small (microscopic organisms). Three-act works but the documentary needs strong narration to carry it.
- **Misinterpretation risk:** "revival" is a contested term in cryobiology. The script must define it precisely (the work shows metabolic activity resumes after thaw, not that the organism is unchanged from 28,000 years ago).

### F4 — Star That Dimmed

- **Speculation risk:** highest of the four. The "alien megastructure" framing is famous and the documentary must explicitly handle it without giving it oxygen it does not warrant.
- **Currency risk:** the science has moved significantly since 2017. The script must reflect 2020–2025 status, not 2017 status.
- **Visual surface:** the Kepler light curve is the iconic image but the visual variety is limited beyond it.

---

## 4. Recommended Story

**The Cell That Survived 24,000 Years.** *Title correction: the prior evaluation used "28,000" as a placeholder. The actual reported age in Shmakova et al. (2021) is approximately 24,000 years BP. The working title must use the correct figure. The recommendation stands; only the title number changes.*

This is the finalist that best operationalizes the channel's stated distinguishing feature — evidence-driven, restrained, honest about uncertainty, anti-clickbait. The central narrative move is "here is what the science actually says, and here is what it does not say." That move is rare in popular coverage of this topic and is exactly the channel's brand.

The recommended angle is **not** "ancient worm lives." It is **"what does revival mean scientifically, and how do we know the cells are not modern contaminants?"** The documentary takes the viewer through: permafrost environments → cryptobiosis as a biological state → the 2020s revival experiments → the contamination-control problem → what "revived" actually means → what this implies for biology of dormancy.

This angle is well-evidenced, narratively sustainable for 15–25 minutes, visually rich (microscopy, permafrost cores, time-lapse, controlled-environment footage), and aligned with the channel's restraint identity.

---

## 5. Why It Wins

The recommendation comes down to four criteria:

1. **Channel identity.** The story is *defined* by the channel's distinguishing feature. The story's central question — "what does revival actually mean?" — is the channel's central question applied to a specific phenomenon.

2. **Restraint is a competitive advantage here.** Most coverage of permafrost revival defaults to the tabloid framing. A documentary that explicitly rejects that framing and walks the viewer through the actual science is rare. The channel gets credit for that restraint without sacrificing narrative momentum.

3. **Evidence durability.** The primary literature (Shmakova et al. 2021 on bdelloid rotifers; related cryobiology and permafrost microbiology literature) is settled enough to script from without fear of mid-production obsolescence.

4. **Visual evidence breadth.** Microscopy (legitimate, CC-licensed or licensed), permafrost cores, time-lapse rehydration, vitrification diagrams, contamination-control laboratory footage. This is a wide legitimate visual surface.

The runner-up is F1 (Fast Radio Burst). The deciding factor against F1 is that its originality advantage depends entirely on whether the channel can execute the post-2020 repeater-vs-non-repeater framing precisely. The script-writing risk is higher. F3's storytelling risk is lower because the underlying biology is more concrete and easier to ground in visuals.

---

## 6. Evidence That Must Be Verified During Research

Before any script is drafted, the Research stage must verify the following claims (with primary sources):

1. **The 2021 bdelloid rotifer revival.** Shmakova et al. (2021) in *Current Biology* — confirm the specific claim of metabolic activity after thaw from permafrost estimated at ~24,000 years. Verify the methodology: how did the authors control for modern contamination?

2. **The Pleistocene age assignment.** Confirm the radiocarbon dating methodology and the exact figure reported. *Note:* The working title used "28,000 years" during the prior evaluation; the actual reported age is **approximately 24,000 years BP** (Shmakova et al. 2021). The working title must use the correct figure.

3. **Definition of "revival" in the paper.** Verify exactly what the paper claims: metabolic activity, movement, reproduction — and what it does not claim (e.g., the organism being unchanged from its Pleistorean state).

4. **Cryptobiosis and vitrification biophysics.** Confirm the mechanism by which bdelloid rotifers and tardigrades survive desiccation and freezing — anhydrobiosis vs. cryobiosis, glass transition temperatures, trehalose (or lack thereof) in bdelloids specifically.

5. **Contamination controls in permafrost microbiology.** Confirm the standard controls: surface-sterilization of cores, sterile subsampling, negative controls, modern-strain exclusion.

6. **The 2022 tardigrade revival claim and its retraction.** A separate paper (2019) reported tardigrade revival from a 1,000+ year-old moss sample. A subsequent comment or correction needs to be checked. The research notes must distinguish this from the bdelloid finding.

7. **Existing popular coverage.** A survey of recent YouTube/streaming coverage of this topic — both to identify what the channel must NOT repeat and to identify the specific angle that is under-treated. (Limited research effort; the goal is "what's missing," not "everything that's been said.")

8. **Other Pleistocene revival claims.** Plant material (Silene stenophylla, 2012 paper) and other claims — verify and place in context.

These eight points define the "Fact Check Plan" for the Research stage.

---

## 7. What Could Cause the Story To Be Rejected During Research

The research stage could surface facts that cause the story-selection decision to be revisited. The leading risks:

- **Contamination controls prove inadequate.** If the primary papers' controls are weak by modern standards, the "revival" claim collapses. The story can survive in a different shape (a documentary about the *uncertainty* of permafrost revival claims) but the recommended angle fails.
- **The dating proves unreliable.** If the age assignment is not robust, the headline number (~24,000 years or whatever the actual figure is) cannot be used. The story can be reframed without the deep-time framing but loses a major narrative anchor.
- **Recent popular coverage saturates the angle.** If a 2024 or 2025 documentary has already done the "scientific framing vs. tabloid framing" angle well, the channel's originality collapses. Mitigated by the broad literature base; risk is moderate.
- **The visual surface proves thinner than expected.** If microscopy footage is hard to license or the permafrost environment footage is restricted, the documentary loses the visual richness the recommendation depends on. Mitigated by the existence of CC-licensed microscopy and the option of clear, hand-drawn diagrams for vitrification.
- **A retraction surfaces.** If the bdelloid 2021 paper is retracted or substantially corrected between script-draft and publication, the story must be reworked. (Lower probability for this specific paper but worth flagging.)

If any of these surfaces during research, the next-best alternative is **F1 — The Fast Radio Burst That Would Not Repeat** (with the explicit post-2020 repeater-vs-non-repeater framing). F2 (Microbe) and F4 (Star) are the next-tier fallbacks.

---

## Out-of-Finalists Notes

**The Octopus That Edits Its Own RNA (initial 65, now deprioritized as finalist).** Strong candidate on visual surface and audience appeal. The reason it was not promoted to a finalist: the channel's restraint identity is harder to maintain in this story because popular coverage routinely drifts into "alien intelligence" framing. The narrative risk is real but the cost is high. F3 won the restraint-identity tie-breaker.

**The Forest That Remembers Without a Brain (initial 61).** Strong visual potential but high R8 risk (animism framing). The signal-vs-noise distinction in this field is real and the topic is interesting, but the channel's ability to maintain restraint is the question. Worth keeping as a future episode candidate.

**The Ice That Glows Blue in Antarctica (initial 61).** Strong but narrow. The 15–25 minute format is at risk of padding. Better suited to a shorter format.

**The Place Where Gravity Is Slightly Wrong (initial 60).** Genuine scientific puzzle but pacing risk. The narrative needs a strong human anchor (e.g., the survey ship) to carry the abstraction. Future candidate.

**The Mariana Trench's Impossible Microbes (initial 60).** Visual surface is strong but the topic is well-covered on popular channels. The originality angle (recent genomic work on hadal microbes) is real but underexplained — possible future episode.

**The Tunguska Mystery, Honestly (initial 60).** Well-covered. The "honestly" framing is the differentiator but execution risk is high. Future candidate.

**The Voynich Manuscript as a Code Problem (initial 52).** Statistical-linguistics angle is genuinely interesting but no resolution is possible, which raises the padding risk. Future candidate if a specific computational finding emerges.

**The Taos Hum (initial 45).** Deprioritized. R1 and R3 active.

---

## Final Recommendation

**The Cell That Survived 28,000 Years**, with the explicit anti-clickbait scientific framing defined in §4.

If during research this story proves unworkable (per §7), the documented fallback is F1 — Fast Radio Burst.

---

## Files in this Story Evaluation

Created:
- `research/video-001_story_evaluation_decision.md` (this file)

Not modified:
- `research/video-001_story_discovery.md`
- `research/video-001_story_evaluations.md`
- Any file in `docs/`, `automation/`, or `production/`

This document is the input for the human's Story Selection decision. The decision will be recorded with `yt approve video-001 --gate story-selection` after the `story-evaluation` stage is closed.
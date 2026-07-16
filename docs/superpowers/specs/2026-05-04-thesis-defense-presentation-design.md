# Thesis Defense Presentation Design

**Title:** Framework for Fusion of Laser Scanning Point Clouds with Panoramic Imagery to Enhance Indoor Measurement Reliability

**Author:** Ruoyu Yan
**Supervisor:** Jun.-Prof. Dr. R. Maalek
**Institute:** TMB, BGU, KIT
**Defense date:** 2026-05-13 (open defense)
**Audience:** Professor + PhD candidates + students (mixed)
**Format:** 30 min talk + 15 min Q&A
**Tooling:** PowerPoint, KIT_PPT Template_EN.potx (English)

**Scope of this spec:** Overall slide structure, asset mapping, and prerequisite work only. Slide-level visual details (fonts, exact layouts, animation choreography, speaker notes) are out of scope and will be worked out during slide construction.

---

## Goals

1. **Convey the contribution clearly to a mixed audience.** Students see the *what* and *why*; PhDs and the professor see the *how* and the *novelty*.
2. **Lead with the demo.** A 60–90 s captioned video of the Electron app run is the hook, placed early — before related work.
3. **Anchor the contribution in two framings:**
   - *Technical:* multi-room extension of FGPL (CVPR 2024), which only handles single-room scenes.
   - *Practical / academic:* transparent, reproducible reference pipeline for the colorless-TLS + separate-pano-camera workflow — alternative to black-box SaaS (Matterport).
4. **Validate end-to-end** by colorization fidelity against an original colored point cloud, in lieu of ground-truth poses.

## Non-goals

- Slide-level visual design.
- New experiments beyond the FGPL ablation (P3 below).
- Quantitative Matterport benchmarking (mentioned as future work).
- Rotation-error metrics (no GT rotations available; replaced by colorization-as-pose-proxy).

---

## Talk structure

22 content slides, ~30 min, 8 sections.

### 1. Opener (3 min)

| # | Slide | Time |
|---|-------|------|
| 1 | Title | 30 s |
| 2 | The practical problem — TLS + separate 360° camera, no automated fusion tool; Plan4 renovation use case | 1 min |
| 3 | The academic framing — AEC needs transparent multi-source fusion; FGPL is single-room only | 1 min |

### 2. Demo-first hook (2 min)

| # | Slide | Time |
|---|-------|------|
| 4 | What you'll see — single still + one-sentence framing | 30 s |
| 5 | **Video** — full-bleed, ~75–90 s, captioned, silent | 90 s |

### 3. Foundations (5 min)

Related work woven with framework integration. For each cited method, show the figure of where it sits in the pipeline.

| # | Slide | Time |
|---|-------|------|
| 6 | Pipeline at a glance — 13 stages → 4 phases, 2 confirmation gates | 1 min |
| 7 | Pano pose estimation lineage — feature → color → line+learned → fully geometric (FGPL) | 1.5 min |
| 8 | Foundation methods 2×2 — SAM3, FGPL, Screened Poisson, MVS Texturing (texrecon) | 1.5 min |
| 9 | The gap — cross-room lines pollute FGPL energy; need room assignment first | 1 min |

### 4. Core contribution: Multi-room assignment (8 min)

| # | Slide | Time |
|---|-------|------|
| 10 | Density image generation — RANSAC floor → Manhattan alignment → ortho projection | 1.5 min |
| 11 | Room segmentation (SAM3) — CLAHE pre-process + low-confidence prompt | 1.5 min |
| 12 | Pano footprint extraction | 1.5 min |
| 13 | Jigsaw match — M room polygons × N pano footprints → score → assign | 2 min |
| 14 | Confirmation gate — human-in-the-loop before downstream cascading | 1.5 min |

### 5. Pose estimation (3 min)

| # | Slide | Time |
|---|-------|------|
| 15 | FGPL refinement, now per-room — line filtering by room polygon prior | 1.5 min |
| 16 | Cross-room handling + qualitative pose viz | 1.5 min |

### 6. Colorization + meshing (2 min)

| # | Slide | Time |
|---|-------|------|
| 17 | Pose-aware projection → colored point cloud → Poisson recon + texrecon (single 3-panel slide) | 2 min |

### 7. Results (5 min)

| # | Slide | Time |
|---|-------|------|
| 18 | **Validation strategy** — no GT poses; colorization fidelity as pose-correctness proxy | 1.5 min |
| 19 | **Colorization quality (= pose quality), Ours vs Vanilla FGPL** — table on Subset 1 (multi-room: corridor+office) and Subset 2 (single-room control: office) | 2 min |
| 20 | Final outputs — textured GLB still + Unity virtual-tour screenshot with measurement | 1 min |
| 21 | Limitations — confirmation gates, single-floor only, dependence on SAM3, qualitative cross-room pose verification | 30 s |

### 8. Close (2 min)

| # | Slide | Time |
|---|-------|------|
| 22 | Conclusion + future work | 1.5 min |
| — | Thank you / Q&A | 30 s |

### Q&A backup slides (hidden, not in 30 min)

10 backup slides, kept all per user direction:

- B1: Matterport comparison framing (qualitative dimensions only)
- B2: Per-stage runtime chart (parsed from app logs)
- B3: FGPL math — line intersections, XDF on unit sphere
- B4: Jigsaw scoring function — polygon overlap + scale consistency
- B5: SAM3 failure modes + how confirmation gate handles them
- B6: RoomFormer → SAM3 transition (why dropped)
- B7: SAM3 parameter table (prompt, confidence, CLAHE settings)
- B8: Multi-floor extension (future work)
- B9: Manhattan-alignment assumption — robustness when violated
- B10: Internal pipeline matching distance (`avg_dist` from `local_filter_results.json`) — what it is and isn't

Navigation choice (hidden backup index slide vs. printed reference card) deferred to slide-build phase.

---

## Asset mapping

Per-slide asset state. **Ready** = use as-is. **Adapt** = exists, needs cropping/relabeling. **Create** = new artifact required this week.

| # | Slide | State | Source / action |
|---|-------|-------|-----------------|
| 1 | Title | Ready | KIT template |
| 2 | Practical problem | Create | Equipment photo (TLS scanner + 360° camera). ~15 min. |
| 3 | Academic framing | Ready | Text-only, copy phrasing from proposal abstract |
| 4 | What you'll see | Ready | Frame from edited video |
| 5 | Video | Adapt | Cut `2026-05-04 12-37-47.mkv` (14:19, 270 MB) → ~75–90 s with captions. Manual edit (user). |
| 6 | Pipeline at a glance | Create | 13-stage architecture diagram. Reused in thesis Ch 3. ~2 hours. |
| 7 | Pano pose lineage | Create | Comparison tree text + icons. ~30 min. |
| 8 | Foundation methods 2×2 | Adapt | Crops from `data/sam3_pano_processing/`, `manuscript/.../ch5-camera-pose-estimation/figures/`, `manuscript/.../ch6-colorization-meshing/figures/`. |
| 9 | The gap | Create | Cartoon: cross-room line pollution failure mode. ~45 min. |
| 10 | Density image | Ready | `manuscript/.../ch4-multi-room-assignment/figures/` (4-1a/b/c) |
| 11 | SAM3 segmentation | Ready | `ch4-multi-room-assignment/figures/` (4-2a/b/c) |
| 12 | Pano footprint | Ready | `data/sam3_pano_processing/footprint_comparison/comparison_summary.png` |
| 13 | Jigsaw match | Adapt | Endpoint: `data/sam3_room_segmentation/demo6_alignment.png` + PPT build animation. |
| 14 | Confirmation gate | Create | Screenshot of Electron confirmation modal. ~5 min. |
| 15 | FGPL per-room | Adapt | `ch5-camera-pose-estimation/figures/` (FGPL pipeline diagram) + callout box. |
| 16 | Pose viz | Ready | `ch5-camera-pose-estimation/figures/` (top-down + reprojection panels) |
| 17 | Colorization + meshing | Adapt | Cubemap from `ch6-colorization-meshing/figures/` + render of `data/textured_point_cloud/.../tmb_office_one_corridor_dense_noRGB_textured.ply` + screenshot of `data/mesh/.../tmb_office_one_corridor_bigger_noRGB_textured.glb`. ~1 hour. |
| 18 | Validation strategy | Create | Diagram: pose error → projection error → color error. ~30 min. |
| 19 | Ours vs vanilla FGPL table | Create (depends on P3) | Combine existing `data/validation/subset1.../evaluation_metrics.json` + `subset2.../evaluation_metrics.json` (Ours) with new ablation results (Vanilla FGPL). |
| 20 | Final outputs | Create | GLB turntable still + Unity tour screenshot with measurement. ~45 min. |
| 21 | Limitations | Ready | Text-only |
| 22 | Conclusion | Ready | Text + small recap figure |
| Q&A backups | 10 slides | Mostly Adapt | One Create: B2 runtime chart (parse app log timestamps). |

---

## Prerequisite tasks

| ID | Task | Critical path? | Estimate |
|----|------|----------------|----------|
| P1 | Edit `2026-05-04 12-37-47.mkv` from 14:19 → ~75–90 s with stage-name captions. Manual edit. | Yes | ~2 hours |
| P3 | **FGPL ablation** — disable polygon prior + room assignment in pose estimation; run vanilla FGPL on the 3 panos (TMB_corridor_south1, TMB_corridor_south2, TMB_office1) against `tmb_office_one_corridor_bigger_noRGB.ply`; colorize using those poses; evaluate against `tmb_office_one_corridor_bigger.ply` using existing `evaluate_colorization.py`; build comparison row. | Yes — slide 19 blocks on this | ~1 day |
| P4 | Render textured PLY still (slide 17) + GLB still (slide 20) + Unity tour screenshot with measurement (slide 20). | No | ~1 hour |
| P5 | Per-stage runtime chart for B2: parse `data/logs/app_*.log` timestamps, build bar chart. | No (Q&A only) | ~1 hour |

**Dropped:** rotation-error metric — no GT rotations available; replaced by colorization-as-pose-proxy framing.

**Reused without recomputation:** colorization metrics for Ours pipeline already exist in `data/validation/subset1 - corridor + office/evaluation_metrics.json` and `data/validation/subset2 - office/evaluation_metrics.json`. Subset 1 covers exactly the 3 panos in the ablation scope.

---

## Schedule

| Day | Date | Work |
|-----|------|------|
| 1 | Mon May 4 | Spec finalized; **edit video to 75 s** (P1); build pipeline diagram (slide 6) |
| 2 | Tue May 5 | **Run FGPL ablation** (P3): vanilla FGPL → colorize → evaluate |
| 3 | Wed May 6 | Build slides 1–9 (opener, demo, foundations); render PLY/GLB stills (P4) |
| 4 | Thu May 7 | Build slides 10–14 (multi-room core) |
| 5 | Fri May 8 | Build slides 15–17 (pose, colorization, meshing) |
| 6 | Sat May 9 | Build slides 18–22 (results + ablation table, conclusion) |
| 7 | Sun May 10 | Q&A backup slides; runtime chart (P5) |
| 8 | Mon May 11 | First full dry run; time the talk; pacing fixes |
| 9 | Tue May 12 | Buffer; second dry run; supervisor review |
| 10 | Wed May 13 | Defense |

Critical path: **P1 (Day 1) → P3 (Day 2) → slide 19 build (Day 6)**. P3 is the longest single task; if it slips, slide 19 falls back to qualitative-only comparison (cross-room error heatmap visualization without numeric ablation row), which is a defensible Plan B.

---

## Open decisions deferred to slide-build phase

These were intentionally not finalized in this spec because the user requested overall structure only:

1. Whether slide 13 uses a PowerPoint build animation or a static before/after pair.
2. Hidden backup index slide (slide 23) vs. printed reference card for Q&A navigation.
3. Whether to include 1–2 short clips from the full 14-min video at slides 13/20 for added context, or use only the slide-5 cut.
4. Final phrasing of the academic-framing bullet on slide 3 (lift directly from proposal abstract or reword for spoken delivery).
5. Caption style on the video (overlay text vs. lower-third).

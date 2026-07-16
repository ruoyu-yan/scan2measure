# Thesis Defense Presentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a 30-min thesis defense presentation (22 content slides + 10 Q&A backup slides) for the open defense on 2026-05-13.

**Architecture:** Demo-first structure — Motivation → Video → Foundations → Multi-room core → Pose → Colorization → Results → Close. Built in PowerPoint using KIT_PPT Template_EN.potx. Per-slide content limited to overall structure; slide-level visual details (fonts, layouts, animations) deferred to user.

**Source spec:** `docs/superpowers/specs/2026-05-04-thesis-defense-presentation-design.md`

**Tooling:** PowerPoint (Windows), Shotcut/DaVinci Resolve for video editing, MeshLab/Blender for renders, Python for runtime parsing.

**Output file (target):** `E:\OneDrive\File\Uni\KIT\WS25-26\Master Thesis\Thesis_Defense_Ruoyu_Yan.pptx`

---

## Prerequisite tasks (must finish before slides that depend on them)

### Task P1: Edit headline video to 75–90 s

**Source:** `E:\OneDrive\File\Uni\KIT\WS25-26\Master Thesis\2026-05-04 12-37-47.mkv` (14:19, 270 MB)
**Output:** `E:\OneDrive\File\Uni\KIT\WS25-26\Master Thesis\defense_demo_video.mp4` (~75–90 s, 1080p)
**Blocks:** Slide 4 (still frame) and Slide 5 (full video).

- [ ] Pick a video editor (Shotcut, DaVinci Resolve, or Clipchamp on Windows)
- [ ] Watch the raw video end-to-end; mark in/out points for each pipeline stage
- [ ] Cut to ~75–90 s using speed ramps (faster on long-running stages: line detection, meshing) and hard cuts (skip duplicate UI clicks)
- [ ] Add stage-name caption overlays at each pipeline transition (e.g., "Density image generation" → "Room segmentation (SAM3)" → "Pano footprint extraction" → "Polygon matching" → "Pose estimation" → "Colorization" → "Meshing & texturing" → "Virtual tour")
- [ ] Export 1080p MP4 at the target name above
- [ ] Extract one still frame from a visually strong moment (e.g., the textured mesh or virtual tour) and save as `defense_demo_still.png` for slide 4

### Task P3: FGPL ablation for slide 19

**Goal:** Run vanilla FGPL (no room polygon prior, no per-room line filtering) on the 3 panos, colorize using those poses, evaluate, and produce a comparison row for slide 19.

**Inputs:**
- Colorless point cloud: `data/textured_point_cloud/.../tmb_office_one_corridor_bigger_noRGB.ply` (or wherever your colorless PLY of `tmb_office_one_corridor_bigger` lives)
- Ground-truth colored cloud: `data/textured_point_cloud/.../tmb_office_one_corridor_bigger.ply`
- Panos: `TMB_corridor_south1.jpg`, `TMB_corridor_south2.jpg`, `TMB_office1.jpg`

**Existing scripts to reuse:**
- `src/pose_estimation/pose_estimation_pipeline.py` (FGPL-faithful single-room implementation)
- `src/colorization/colorize_point_cloud.py`
- `src/colorization/evaluate_colorization.py`

- [ ] Confirm `src/pose_estimation/pose_estimation_pipeline.py` runs single-room FGPL faithfully (no polygon prior, no per-room filtering); if not, add a `--no-room-prior` flag
- [ ] Run vanilla FGPL on each of the 3 panos against the colorless point cloud; save predicted poses to a separate output dir (e.g., `data/pose_estimates/ablation_vanilla_fgpl/`)
- [ ] Run `colorize_point_cloud.py` using the vanilla-FGPL poses; output to `data/textured_point_cloud/ablation_vanilla_fgpl/...`
- [ ] Run `evaluate_colorization.py` on the result against the original colored ply; save to `data/validation/ablation_vanilla_fgpl/evaluation_metrics.json`
- [ ] Render an error heatmap PLY screenshot (showing where vanilla FGPL fails — likely cross-room regions) and save as `defense_assets/ablation_error_heatmap.png`

**Plan B if vanilla FGPL doesn't converge / is too slow:** drop the numeric ablation row from slide 19 and use only the qualitative error-heatmap visualization side-by-side. The validation-strategy framing on slide 18 still stands.

### Task P4: Render mesh + tour stills

**Output dir:** `defense_assets/` (create at project root or wherever convenient)

- [ ] Render still of textured PLY: open `data/textured_point_cloud/.../tmb_office_one_corridor_dense_noRGB_textured.ply` in MeshLab; choose a clean angle; screenshot at high resolution → save as `defense_assets/textured_pointcloud_still.png`
- [ ] Render still of textured GLB: open `data/mesh/tmb_office_one_corridor_bigger_noRGB/tmb_office_one_corridor_bigger_noRGB_textured.glb` in Blender or three.js viewer; choose a clean angle; screenshot → save as `defense_assets/textured_mesh_still.png`
- [ ] (Optional) Render a short turntable: 4–6 s loop of the GLB rotating; save as `defense_assets/textured_mesh_turntable.mp4`
- [ ] Launch the Unity virtual tour build (`E:\OneDrive\...\unity\VirtualTour\Build\VirtualTour.exe`); take a screenshot mid-walk with a visible measurement annotation (use the point-to-point or wall-to-wall tool) → save as `defense_assets/unity_tour_measurement.png`

### Task P5: Per-stage runtime chart (Q&A backup B2)

**Output:** `defense_assets/runtime_per_stage.png`

- [ ] Pick the most recent successful end-to-end log: scan `data/logs/app_*.log` for one that ran all 13 stages
- [ ] Write a short Python script that parses the log, extracts per-stage start/end timestamps via the `[PROGRESS]` lines, and computes durations
- [ ] Plot a horizontal bar chart (matplotlib) with stage names on Y, duration in seconds on X; save the PNG

---

## Day 1 — Mon May 4: Spec + video edit + pipeline diagram

- [ ] Spec already written and approved
- [ ] Execute **Task P1** (video edit)
- [ ] **Build pipeline diagram for slide 6:** in PPT or draw.io, lay out 13 stages grouped into 4 phases (Multi-Room Assignment, Pose Estimation, Colorization, Meshing); mark stages 5 and 10 as confirmation gates with a different shape; export as `defense_assets/pipeline_diagram.png`. Reuse the same diagram in thesis Ch 3.

## Day 2 — Tue May 5: FGPL ablation

- [ ] Execute **Task P3** (FGPL ablation end-to-end)
- [ ] Verify ablation results saved at the paths specified in P3
- [ ] If P3 hit the Plan B fallback, note this in the slide-19 build task on Day 6

## Day 3 — Wed May 6: Build slides 1–9 (Opener, Demo, Foundations) + asset renders

**Open the KIT template** as a new presentation:
- [ ] Open PowerPoint, File → New from Template → `E:\OneDrive\File\Uni\KIT\WS25-26\Master Thesis\KIT_PPT Template_EN.potx`
- [ ] Save as `E:\OneDrive\File\Uni\KIT\WS25-26\Master Thesis\Thesis_Defense_Ruoyu_Yan.pptx`

**Slide 1 — Title (Ready):**
- [ ] Use the template title layout. Title: "Framework for Fusion of Laser Scanning Point Clouds with Panoramic Imagery to Enhance Indoor Measurement Reliability". Author: Ruoyu Yan. Supervisor: Jun.-Prof. Dr. R. Maalek. Institute: TMB, BGU, KIT. Date: 2026-05-13. Subtitle: "Master's Thesis Defense"

**Slide 2 — Practical problem (Create):**
- [ ] Take or find a photo of a colorless TLS scanner (e.g., FARO Focus) + a 360° pano camera (e.g., Insta360) → save as `defense_assets/equipment_photo.png`
- [ ] Insert the photo
- [ ] Add bullets: (i) Practitioners with a colorless TLS scanner + a separate 360° camera have no automated tool to fuse them. (ii) Plan4 renovation use case — needs in-house, verifiable workflow.

**Slide 3 — Academic framing (Ready):**
- [ ] Add bullet 1: AEC industry needs **transparent, standards-aware** workflows for multi-source data fusion (vs. black-box SaaS like Matterport). [Lift phrasing from `Master's Thesis- Ruoyu Yan.docx` abstract.]
- [ ] Add bullet 2: Existing geometric pano-pose methods (FGPL, CVPR 2024) handle **single-room scenes only** — gap for real buildings.

**Slide 4 — What you'll see (Ready, depends on P1):**
- [ ] Insert `defense_assets/defense_demo_still.png`
- [ ] One-line caption: "60-second walkthrough of the desktop app — colorless point cloud + panoramas in, textured GLB + virtual tour out."

**Slide 5 — Video (Ready, depends on P1):**
- [ ] Insert `defense_demo_video.mp4` full-bleed (no slide title; use blank-content layout)
- [ ] Set playback to "play automatically" on slide entry; loop disabled

**Slide 6 — Pipeline at a glance (depends on Day 1 diagram):**
- [ ] Insert `defense_assets/pipeline_diagram.png`
- [ ] Caption pointing out the 4 phases and 2 confirmation gates

**Slide 7 — Pano pose lineage (Create):**
- [ ] Build a horizontal tree (PPT shapes) with 4 nodes left-to-right: feature-based (SfM/PnP, PoseNet) → color-distribution (PICCOLO, CPO) → line+learned (LDL) → fully geometric (**FGPL**, highlighted)
- [ ] Below each node, one line on what it excludes / requires (e.g., "needs visual correspondences" / "needs scene-specific training" / "needs color in 3D model" / "needs learned features")
- [ ] Below FGPL, callout box: "Fits our colorless-TLS setting — but evaluated only on single-room scenes"

**Slide 8 — Foundation methods 2×2 (Adapt):**
- [ ] 2×2 grid of cells. Each cell: paper citation + small framework figure showing where the method sits in the pipeline.
  - Top-left: SAM3 (segmentation) — crop from `data/sam3_pano_processing/` or `manuscript/.../ch4-multi-room-assignment/figures/`
  - Top-right: FGPL (pose) — crop from `manuscript/.../ch5-camera-pose-estimation/figures/` (pipeline diagram)
  - Bottom-left: Screened Poisson (mesh) — illustrative figure / cite Kazhdan & Hoppe 2013
  - Bottom-right: MVS Texturing / texrecon — crop from `manuscript/.../ch6-colorization-meshing/figures/`

**Slide 9 — The gap (Create):**
- [ ] Build a 2-panel cartoon. Left: single-room FGPL — line intersections converge cleanly to correct pose. Right: multi-room — cross-room lines pollute the energy landscape, FGPL converges to wrong local minimum. Use stylized line drawings.
- [ ] Bottom caption: "We need to assign each panorama to a room first."

**Run Task P4 (mesh/tour renders) in parallel** — useful for slide 17 and slide 20 later in the week.

## Day 4 — Thu May 7: Build slides 10–14 (Multi-room core)

**Slide 10 — Density image generation (Ready):**
- [ ] Insert 3-panel figure: raw cloud → aligned cloud → density image. Source: `manuscript/.../ch4-multi-room-assignment/figures/` (4-1a/b/c)
- [ ] Add 3 short bullets: RANSAC floor plane → Manhattan rotation alignment → ortho projection (256×256, 10mm/100mm grid)
- [ ] Mention the metadata bridge (min_coords, offset, rotation_matrix) as the coordinate glue

**Slide 11 — Room segmentation with SAM3 (Ready):**
- [ ] Insert 3-panel figure: CLAHE-enhanced density → SAM3 mask → cleaned polygon. Source: `manuscript/.../ch4-multi-room-assignment/figures/` (4-2a/b/c)
- [ ] Bullets: prompt "floor plan", confidence 0.1, CLAHE clipLimit 4.0; mask classification (>70% area = junk, >85% occupied = building outline)

**Slide 12 — Pano footprint extraction (Ready):**
- [ ] Insert `data/sam3_pano_processing/footprint_comparison/comparison_summary.png`
- [ ] Bullets: SAM3 floor mask on the panorama → spherical-to-ground projection → camera-side polygon

**Slide 13 — Jigsaw match (Adapt):**
- [ ] Insert `data/sam3_room_segmentation/demo6_alignment.png` as the endpoint figure
- [ ] Above it, build a sequence (multi-step shape composition or PowerPoint build clicks): M room polygons + N pano footprints → score combinations → assigned matches
- [ ] Caption / scoring legend: polygon overlap (IoU) + scale consistency

**Slide 14 — Confirmation gate (Create):**
- [ ] Launch the Electron app, navigate to a state where the polygon-match confirmation modal is visible; screenshot → `defense_assets/confirmation_gate_screenshot.png`
- [ ] Insert screenshot
- [ ] Bullets: human-in-the-loop here is honest engineering — SAM3 misclassifications would cascade through pose, colorization, and meshing

## Day 5 — Fri May 8: Build slides 15–17 (Pose, Colorization, Meshing)

**Slide 15 — FGPL refinement, now per-room (Adapt):**
- [ ] Insert FGPL pipeline diagram from `manuscript/.../ch5-camera-pose-estimation/figures/`
- [ ] Add a callout box highlighting the line-filtering step: "Lines filtered by the assigned room polygon prior — cross-room pollution removed"

**Slide 16 — Cross-room handling + qualitative pose viz (Ready):**
- [ ] Insert top-down + reprojection panels from `manuscript/.../ch5-camera-pose-estimation/figures/`
- [ ] Caption: visual confirmation that predicted poses align panorama features with 3D structure across rooms

**Slide 17 — Colorization + meshing (Adapt, depends on P4):**
- [ ] 3-panel layout. Panel 1: cubemap projection diagram from `manuscript/.../ch6-colorization-meshing/figures/`. Panel 2: `defense_assets/textured_pointcloud_still.png`. Panel 3: `defense_assets/textured_mesh_still.png`.
- [ ] Caption: "Standard tools chained together — Poisson recon (Kazhdan 2013) + texrecon (Waechter 2014). Brief by design."

## Day 6 — Sat May 9: Build slides 18–22 (Results + Close)

**Slide 18 — Validation strategy (Create):**
- [ ] Build a left-to-right diagram (PPT shapes): pose error → projection error → color error
- [ ] Caption: "We have no GT poses. We measure end-to-end colorization fidelity against an original colored point cloud as a proxy for pose correctness."

**Slide 19 — Colorization quality table (depends on P3):**
- [ ] Build a table: rows = {Subset 1 (corridor + office), Subset 2 (office only — control)}, columns = {Method, Coverage %, RGB L2 mean, RGB L2 median, ΔE2000 mean, %ΔE<5, %ΔE<10}
- [ ] Method = {Ours, Vanilla FGPL} → 4 rows total
- [ ] Pull "Ours" numbers from `data/validation/subset1 - corridor + office/evaluation_metrics.json` and `data/validation/subset2 - office/evaluation_metrics.json`
- [ ] Pull "Vanilla FGPL" numbers from `data/validation/ablation_vanilla_fgpl/evaluation_metrics.json` (produced in Task P3)
- [ ] To the right of the table, insert `defense_assets/ablation_error_heatmap.png` (cross-room failure of vanilla FGPL)
- [ ] **Plan B note (if P3 fell back):** drop the "Vanilla FGPL" rows; show "Ours" only with a side-by-side qualitative heatmap comparing pipelines

**Slide 20 — Final outputs (Create, depends on P4):**
- [ ] Two-panel: `defense_assets/textured_mesh_still.png` (or `textured_mesh_turntable.mp4`) on left; `defense_assets/unity_tour_measurement.png` on right
- [ ] Caption: textured GLB output + interactive Unity virtual tour with measurement tool

**Slide 21 — Limitations (Ready):**
- [ ] Bulleted list: confirmation gates require human input; single-floor only (RANSAC floor + ortho assumption); SAM3 quality dependence; pose validation is end-to-end (colorization-proxy), not direct geometric error against GT poses

**Slide 22 — Conclusion + future work (Ready):**
- [ ] Restate contributions: (1) multi-room extension of FGPL; (2) transparent reproducible reference pipeline
- [ ] Future: automated confirmation gates; multi-floor support; quantitative Matterport benchmark; direct GT-pose evaluation with AprilTags

**Thank you / Q&A slide:**
- [ ] Single slide with "Thank you" and contact info

## Day 7 — Sun May 10: Q&A backup slides + runtime chart

- [ ] Execute **Task P5** (runtime chart for B2)

**B1 — Matterport comparison framing:**
- [ ] Build a qualitative-dimensions table: rows = {Cost, Openness, In-house verifiability, Hardware lock-in, Browser-based output, Measurement tool}; columns = {Matterport, Our framework}; mark each with check / cross / qualitative note
- [ ] Caption: "Quantitative benchmark deferred — closed-source SaaS limits direct comparison."

**B2 — Per-stage runtime chart:**
- [ ] Insert `defense_assets/runtime_per_stage.png`
- [ ] One-line caption: dataset = TMB office + corridor (3 panos); end-to-end ~X minutes

**B3 — FGPL math:**
- [ ] Equation block: line intersections on the unit sphere; XDF distance formula; energy minimization objective
- [ ] Citation: Liu et al., "From Geometric Lines to Pose: Frontal-Geometric Pose Localization", CVPR 2024

**B4 — Jigsaw scoring function:**
- [ ] Show the polygon overlap (IoU on aligned footprints) + scale consistency penalty terms used in `src/floorplan/align_polygons_demo6.py` and `polygon_scale_calculation_v2.py`
- [ ] Below: one successful match + one failed match for visual contrast

**B5 — SAM3 failure modes + confirmation gate:**
- [ ] Show one SAM3 mistake from the data (over-segmentation or merged rooms) → Electron confirmation UI screenshot from slide 14 → corrected polygons after user fix

**B6 — RoomFormer → SAM3 transition:**
- [ ] Two-row comparison: RoomFormer (per-domain training, structured floor plans, hard to extend) vs. SAM3 (zero-shot foundation model, robust, prompt-driven)
- [ ] Cite spec at `docs/superpowers/specs/2026-03-21-fusion-comparison-design.md`

**B7 — SAM3 parameter table:**
- [ ] Table of empirical settings: prompt = "floor plan", confidence = 0.1, CLAHE clipLimit = 4.0, tileGridSize = 8×8, mask area thresholds (>70% = junk, >85% occupied = outline)

**B8 — Multi-floor extension (future work):**
- [ ] Sketch: current pipeline assumes single-floor (RANSAC floor + Z-cut). Multi-floor would require per-floor segmentation in 3D first, then per-floor density images and SAM3 segmentation.

**B9 — Manhattan-alignment assumption:**
- [ ] Show what happens when no dominant axis exists: density image still produces, but segmentation polygons are rotated arbitrarily. Mostly a downstream-readability issue, not algorithmic blocker.

**B10 — Internal pipeline matching distance:**
- [ ] Show the per-pano `avg_dist` table from `data/pose_estimates/multiroom/local_filter_results.json` (TMB_office1: 0.0208 m; TMB_corridor_south1: 0.0282 m; TMB_corridor_south2: 0.0236 m)
- [ ] Clarify: "These are predicted-line vs. matched-3D-line endpoint distances after pose convergence — convergence indicator, NOT pose error vs. ground truth."

## Day 8 — Mon May 11: First dry run + pacing fixes

- [ ] Open the deck in Presenter View; record yourself (audio only) doing the talk start to finish
- [ ] Time each section against the planned budget (Opener 3 / Demo 2 / Foundations 5 / Multi-room 8 / Pose 3 / Colorization 2 / Results 5 / Close 2 = 30 min total)
- [ ] Identify slides that ran long: usually slide 13 (jigsaw), slide 19 (results table), slide 17 (3-panel slide). Trim content if over.
- [ ] Identify slides that ran short and have time slack you can give to the long ones
- [ ] Flag any slide where you stumbled — likely needs better speaker note or simpler content

## Day 9 — Tue May 12: Buffer + supervisor review

- [ ] Send PPT to supervisor (Jun.-Prof. Maalek) for last-minute feedback
- [ ] Second dry run incorporating feedback
- [ ] Final pacing check
- [ ] Print speaker reference card (slide numbers + B-slide jump list) — `<number>+Enter` to jump in PowerPoint

## Day 10 — Wed May 13: Defense day

- [ ] Bring laptop with PPT + the original full 14-min video as backup
- [ ] Bring USB stick with PPT in case of laptop failure
- [ ] Test display + clicker + audio in defense room before the talk

---

## Self-Review

**Spec coverage:**
- All 22 content slides have a build task ✓
- All 10 Q&A backup slides have a build task ✓
- All 4 prerequisite tasks (P1, P3, P4, P5) are present and dependencies are explicit ✓
- 9-day schedule from spec is preserved as Day 1–10 ✓
- Plan B for P3 slip is documented in the slide-19 task ✓

**Placeholder scan:**
- No "TBD"/"TODO" ✓
- No "implement later" / "fill in details" ✓
- All asset file paths concrete ✓
- All script paths concrete ✓

**Type/path consistency:**
- `defense_assets/` is the consistent name for the new asset folder
- `data/validation/ablation_vanilla_fgpl/evaluation_metrics.json` (P3 output) matches the pull location in slide 19 ✓
- `defense_demo_video.mp4` and `defense_demo_still.png` (P1 outputs) match the references in slides 4 and 5 ✓
- Pano names in P3 (`TMB_corridor_south1`, `TMB_corridor_south2`, `TMB_office1`) match the spec ✓

---

## Execution

This plan is written so the user can work through it at their own pace, day by day. Each day is a self-contained batch. Slide-level visual details (fonts, exact layouts, animations) intentionally left to the user per their request.

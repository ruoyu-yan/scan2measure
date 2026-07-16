# Upright rotation prior for multi-room pose estimation

**Date:** 2026-07-16
**Status:** approved, ready to implement
**Component:** `src/pose_estimation/pose_search.py`, `src/pose_estimation/multiroom_pose_estimation.py`

## 1. Problem

On a strictly-Manhattan 5-room Area_3 scene (22 panoramas, PanoPin-seeded), **12 of 22 panos came
back with a rotation error of 89-180°**. The existing 180°-ambiguity countermeasures
(`QUERY_SPHERE_LEVEL=3`, `TOP_K=10` rotation-diverse candidates, post-refinement selection by
`n_tight` then `avg_dist`) are all active and were not bypassed — they simply fail to discriminate.

The failure is decided in the coarse XDF search, not in refinement: for aliased panos the top-0
coarse candidate is already 1.64 m from ground truth (vs 0.39 m for good panos), and the final pose
is essentially the coarse pose (ICP never escapes the basin it was handed).

## 2. Root cause

`build_rotation_candidates` (`pose_search.py:72`) enumerates **24 candidates = 6 permutations × 4
det-preserving sign flips** — the full octahedral rotation group mapping the panorama's three
vanishing directions onto the map's three principal directions. Nothing constrains which way is
down, so **20 of those 24 tip or invert the camera**.

Measured on the 22-pano run (`(R @ up_world) · up_cam`, where `R` is the emitted world→camera
rotation):

| class | n | `(R @ up_world) · up_cam` | meaning |
|---|---|---|---|
| correct | 10 | **1.000** (all ten) | camera upright |
| non-upright | 8 | ≈ 0 | **camera lying on its side** |
| upside-down | 2 | ≈ −1 | **camera inverted** |
| true yaw flip | 2 | 1.000 | upright, facing backwards |

Ground-truth panos have a tilt of 0.1–1.0° (tripod capture), so **10 of the 12 failures are
physically impossible poses** that the estimator is free to select because it has no gravity prior.

## 3. The constraint

Two convention facts, neither fitted to data:

- **`up_cam = [0, 0, 1]`** — `sphere_geometry.equirect_to_sphere` sets `xyz[:,2] = cos(theta)` with
  `theta = pi * s_v`, so the top image row (`s_v = 0`) maps to `+z`. Image-top is up.
- **`up_world = [0, 0, 1]`** — gravity in a Z-up map frame. **Configurable**, because it only holds
  when the point cloud is gravity-aligned (true for raw S3DIS; not guaranteed for a production
  scan).

`R` maps world→camera (`pose_refine.refine_pose` computes `pts_3d_cam = (pts_3d_w - t) @ R.T`), so
an upright camera satisfies:

```
(R @ up_world) · up_cam  >=  cos(max_tilt_deg)
```

Validated on the emitted rotations: a `>= 0.98` threshold admits **10/10 correct** and only **2/12
aliased** poses — exactly the two true yaw flips.

## 4. Design

### 4.1 `pose_search.build_rotation_candidates`

```python
def build_rotation_candidates(principal_2d, principal_3d,
                              up_world=None, up_cam=(0, 0, 1), max_tilt_deg=10.0):
```

When `up_world is None` (default) the function behaves **exactly as today** — 24 candidates, no
filtering. The single-room pipeline (`pose_estimation_pipeline.py`) and existing TMB results are
therefore unaffected.

When `up_world` is provided, compute the 24 rotations as now, then keep only those satisfying the
constraint above. Returns the filtered `(rotations, perms_expanded)` pair.

**Fallback (fail-safe, not fail-silent):** if zero candidates survive, return all 24 unfiltered and
emit a loud warning naming the likely cause (a wrong `up_world` for a non-gravity-aligned cloud).
Returning an empty set would crash the search; silently returning all 24 without a warning would
hide a misconfiguration. The warning is the point.

### 4.2 `multiroom_pose_estimation`

Filter at exactly one place: immediately after `build_rotation_candidates`, **before** `[B5]`
(per-rotation intersection rearrange). `[B5]`, the XDF search and the top-K refinement all derive
from `perms_expanded`, so consistency downstream is automatic and no other call site changes.

New config keys:

| key | default | meaning |
|---|---|---|
| `upright_prior` | `false` | enable the constraint (opt-in; preserves current behaviour) |
| `up_world` | `[0, 0, 1]` | gravity direction in the map/point-cloud frame |
| `max_tilt_deg` | `10.0` | tolerance; capture is tripod-mounted so this is generous |

Log the surviving candidate count per panorama (expected: 24 → 4) so a bad `up_world` is visible
immediately rather than degrading results silently.

### 4.3 Secondary benefit

The XDF coarse search is the dominant cost and scales with the number of rotation candidates.
24 → 4 makes it roughly **6× cheaper**. The prior improves accuracy *and* runtime.

## 5. Scope — explicitly NOT in this change

- **The 2 true yaw flips** (`80e1f6ae`, `da0bb9ad`) are upright and correctly signed; no gravity
  prior can fix them. They respond to the geometry lever instead (a controlled re-run with 4 seeds
  instead of 22 recovered `80e1f6ae` to 0.3°). Out of scope here.
- **The rotation-margin confidence signal** (best minus second-best `n_tight` across distinct
  rotations; separates good from aliased 42/44 with zero false positives) is a separate, additive
  change. Out of scope here.

## 6. Testing

**Unit** (`tests/`, no GPU, synthetic principal directions):
1. `up_world=None` returns exactly 24 candidates, bit-identical to today (regression guard).
2. With `up_world=[0,0,1]`, every returned candidate satisfies the tilt constraint.
3. The filtered set is a strict subset of the unfiltered 24 (filtering, not re-deriving).
4. Degenerate `up_world` (e.g. `[1,0,0]` on a Z-up map, where nothing survives) triggers the
   fallback: 24 candidates returned plus a warning.

**End-to-end validation** — a falsifiable prediction, not a smoke test. Re-run the `manhattan_export`
arm (22 panos, ~8 min) with `upright_prior: true` and compare against the committed baseline:

| metric | baseline | predicted |
|---|---|---|
| rotation locked (≤45°) | 10/22 | **~20/22** |
| translation median | 0.960 m | **< 0.10 m** |
| still aliased | 12 | **exactly `80e1f6ae` + `da0bb9ad`** |

If a pano *other than* those two survives as aliased, the model in §2 is wrong and the result must
be re-examined rather than accepted.

---

## 7. Validation result (2026-07-16, measured)

Re-ran `manhattan_export` (22 panos, seed bit-identical) with `upright_prior: true`. The prior
kept **4/24** candidates per pano and the XDF search went 1.0s -> 0.1s.

| metric | baseline | predicted | **measured** |
|---|---|---|---|
| rotation locked (<=45°) | 10/22 | ~20/22 | **15/22** |
| translation median | 0.960 m | < 0.10 m | **0.084 m** |
| rotation median | 89.9° | — | **1.8°** |
| regressions | — | 0 | **0** |
| still aliased | 12 | exactly 2 | **7** |

**The prediction was NOT met, and the model in §2 was incomplete.** The reasoning error: 8 selected
poses were non-upright, and I assumed each would become *correct* once the impossible candidates
were removed. But a pano only selected an impossible pose because its discriminator was weak — and a
weak discriminator choosing among the 4 remaining upright candidates still fails. Non-upright poses
were a **symptom** of weak discrimination, not its cause.

The 4 upright candidates differ only by yaw (0/90/180/270°), so the residual failures are **pure yaw
aliasing** (89-179°). Of the 7 survivors, **3 are wrong-room panos** (`1a557181`, `da0bb9ad`,
`2b70fafb`, 14-27 m out) — PanoPin room errors, not FGPL rotation failures. Among right-room panos
the lock rate is **10/19 -> 15/19**.

**Verdict: keep the prior.** Strict improvement, zero regressions, 11x better translation median,
~10x faster search. But it does NOT solve the 180° flip alone — the residual yaw ambiguity responds
to the de-crowding lever instead (the 5-seed room-anchored arm locks 5/5 with the prior off), and
the rotation-margin signal (§5) detects what neither fixes. The three are complementary.

### Implementation note — a frame bug the first test could not catch

The first implementation filtered candidates against a raw **world**-frame `up_world`. The candidates
are in the **canonical** frame (`precompute_xdf_3d` rotates geometry by `canonical_rot =
principal_3d`; the search emits `R_world = R_cand @ principal_3d`). With the real
`principal_3d = [[0,0,-1],[0,-1,0],[-1,0,0]]`, world +Z is canonical -X, so it selected exactly the
wrong four candidates: rotation locked went 10/22 -> **0/22**.

The unit test passed because it used `principal_3d = eye(3)`, which makes canonical == world and
hides the bug completely. Tests now use the real non-identity `principal_3d` and assert in the
**world** frame (`R_cand @ principal_3d`), verifying that exactly the 4 world-upright candidates of
the 24 survive. The falsifiable prediction is what surfaced the failure; a vaguer criterion
("check whether rotation improves") would have let a 1.19 m median pass as noise.

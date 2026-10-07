"""Candidate bookkeeping for Point_360's colour arbitration (spec 2026-10-07 §5).

Two additive behaviours of multiroom_pose_estimation, both off by default:
  seed_candidates    one extra candidate per upright rotation at the panorama's seed position
                     (the position the local filter already reads from the alignment), refined
                     like the XDF poses but never chosen by FGPL itself;
  export_candidates  every refined candidate written to <pano>/candidates.json.
Why: on Area_2_manhattan4/office_8 the seed was within 1 cm of the station and FGPL's XDF
candidates were all 2 m away (2026-10-06); the arbiter can only pick what is on the list."""
import json
from pathlib import Path

import numpy as np


def seed_candidates(seed_xy, z, rotations, canonical_rot,
                    inter_2d_per_rot, inter_2d_mask_per_rot, inter_2d_idx_per_rot):
    """One unrefined candidate per rotation at the seed position, shaped exactly like the
    records pose_search.xdf_coarse_search_from_precomputed returns (R = rotations[ri] @
    canonical_rot, as there), so [B7] refines them with the same code."""
    t = rotations.new_tensor([float(seed_xy[0]), float(seed_xy[1]), float(z)])
    out = []
    for ri in range(rotations.shape[0]):
        out.append({
            'R': rotations[ri] @ canonical_rot,
            't': t,
            'rot_idx': ri,
            'cost': None,
            'inter_2d': inter_2d_per_rot[ri],
            'inter_2d_mask': inter_2d_mask_per_rot[ri],
            'inter_2d_idx': inter_2d_idx_per_rot[ri],
            'origin': 'seed',
        })
    return out


def index_of(record, records):
    """Position of `record` (by identity) in `records`; dict equality is unusable here because
    the records hold numpy arrays."""
    for i, r in enumerate(records):
        if r is record:
            return i
    raise ValueError("record is not in the list")


def _record(index, c):
    return {
        "index": index,
        "origin": c.get('origin', 'xdf'),
        "rot_idx": int(c['rot_idx']),
        "R": np.asarray(c['R'], dtype=float).tolist(),
        "t": np.asarray(c['t'], dtype=float).tolist(),
        "cost": None if c.get('cost') is None else float(c['cost']),
        "n_matched": int(c['n_matched']),
        "n_tight": int(c['n_tight']),
        "avg_dist": float(c['avg_dist']),
    }


def write_candidates(path, pano_name, refined, fgpl_choice):
    """Write every refined candidate, in refinement order, with the index FGPL itself chose."""
    doc = {"pano": pano_name, "fgpl_choice": int(fgpl_choice),
           "candidates": [_record(i, c) for i, c in enumerate(refined)]}
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=1))
    return doc

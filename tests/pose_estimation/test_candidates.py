import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "pose_estimation"))
import candidates  # noqa: E402


def _rot_z(deg):
    c, s = np.cos(np.radians(deg)), np.sin(np.radians(deg))
    return torch.tensor([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=torch.float32)


def test_seed_candidates_one_per_rotation_at_the_seed_with_the_canonical_rotation_folded_in():
    rotations = torch.stack([_rot_z(0), _rot_z(90), _rot_z(180), _rot_z(270)])
    canonical = _rot_z(17)
    per_rot = [torch.zeros((3, 3)) + r for r in range(4)]
    masks = [torch.ones((3, 3), dtype=torch.bool) for _ in range(4)]
    idx = [torch.zeros((3, 2), dtype=torch.long) + r for r in range(4)]
    out = candidates.seed_candidates([9.9, 16.5], 1.48, rotations, canonical, per_rot, masks, idx)
    assert [c['rot_idx'] for c in out] == [0, 1, 2, 3]
    assert all(c['origin'] == 'seed' and c['cost'] is None for c in out)
    assert torch.allclose(out[1]['R'], rotations[1] @ canonical)
    assert torch.allclose(out[2]['t'], torch.tensor([9.9, 16.5, 1.48]))
    assert out[3]['inter_2d'] is per_rot[3] and out[3]['inter_2d_idx'] is idx[3]


def test_write_candidates_records_every_field_and_fgpl_choice(tmp_path):
    refined = [
        {'R': np.eye(3), 't': np.array([1.0, 2.0, 1.5]), 'rot_idx': 2, 'cost': -1700.0,
         'n_matched': 40, 'n_tight': 12, 'avg_dist': 0.08},
        {'R': np.eye(3), 't': np.array([3.0, 2.0, 1.5]), 'rot_idx': 0, 'cost': None,
         'n_matched': 30, 'n_tight': 20, 'avg_dist': 0.05, 'origin': 'seed'},
    ]
    doc = candidates.write_candidates(tmp_path / "p" / "candidates.json", "p", refined, fgpl_choice=0)
    on_disk = json.loads((tmp_path / "p" / "candidates.json").read_text())
    assert on_disk == doc
    assert doc["pano"] == "p" and doc["fgpl_choice"] == 0
    assert [c["index"] for c in doc["candidates"]] == [0, 1]
    assert doc["candidates"][0]["origin"] == "xdf" and doc["candidates"][1]["origin"] == "seed"
    assert doc["candidates"][0]["cost"] == -1700.0 and doc["candidates"][1]["cost"] is None
    assert doc["candidates"][1]["t"] == [3.0, 2.0, 1.5] and doc["candidates"][1]["n_tight"] == 20
    assert np.allclose(doc["candidates"][0]["R"], np.eye(3))


def test_fgpl_choice_index_of_a_record_in_refinement_order():
    a = {'n_tight': 3}; b = {'n_tight': 9}; c = {'n_tight': 9}
    assert candidates.index_of(b, [a, b, c]) == 1
    assert candidates.index_of(c, [a, b, c]) == 2

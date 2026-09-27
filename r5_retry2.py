#!/usr/bin/env python3
"""r5_retry2 — last three missing points."""
import sys, json, os
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import OUT_DIR, run_set

JOBS = [('r5_et_sigma.json', {'r5_Et0.6_Nt21': 'r5_Et0.6_Nt21.def'}),
        ('r5_mobility.json', {'r5_mu1': 'r5_mu1.def'}),
        ('r5_csfinal.json', {'r5_csf_Nt22': 'r5_csf_Nt22.def'})]
for jf, variants in JOBS:
    fresh = run_set(variants, '_r5_tmp2.json')
    os.remove(os.path.join(OUT_DIR, '_r5_tmp2.json'))
    p = os.path.join(OUT_DIR, jf)
    d = json.load(open(p))
    d.update(fresh)
    json.dump(d, open(p, 'w'), indent=2)
    print(jf, fresh)

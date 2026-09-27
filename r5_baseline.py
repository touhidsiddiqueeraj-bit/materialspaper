#!/usr/bin/env python3
"""r5_baseline — fresh tight-mesh baseline rerun (freezes Round-5 headline).
Runs BASE def unchanged at 300 K / 1 sun with fine IV step; saves full J-V."""
import sys
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, DEF_DIR, write_def, run_set

write_def('r5_baseline.def', BASE)
print('wrote r5_baseline.def')

run_set({'r5_baseline': 'r5_baseline.def'}, 'r5_baseline.json',
        iv={'start': 0, 'stop': 1.5, 'step': 0.01},
        with_jv_keys=('r5_baseline',))

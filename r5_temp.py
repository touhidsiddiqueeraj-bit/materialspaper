#!/usr/bin/env python3
"""r5_temp — temperature sweep for Ea extraction (Voc vs T -> 0 K).
280..400 K in ~17 K steps (8 pts), fine IV step for clean Voc."""
import sys
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, write_def, run_set

write_def('r5_baseline.def', BASE)
temps = [280, 297, 314, 331, 348, 365, 382, 400]
variants = {f'r5_T{T}': 'r5_baseline.def' for T in temps}
tempmap = {f'r5_T{T}': T for T in temps}
print(f'{len(variants)} variants')
run_set(variants, 'r5_temp.json',
        iv={'start': 0, 'stop': 1.5, 'step': 0.01}, temps=tempmap)

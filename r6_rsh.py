#!/usr/bin/env python3
"""r6_rsh — shunt-resistance bound from archived baseline J-V (first-order,
flagged: Jn(V) = Jph(V) - V/Rsh on the R0 ideal curve; no new SCAPS runs)."""
import json
import numpy as np


def main():
    d = json.load(open('/home/touhid/Documents/materilaspaper/r5_results/r5_baseline.json'))['r5_baseline']
    V = np.array(d['V'])
    Jph = -np.array(d['J'])
    m = (V >= -1e-9) & (V <= float(d['summary']['Voc']))
    V, Jph = V[m], Jph[m]
    out = {}
    for Rsh in (100, 500, 1000, 10000):
        Jn = Jph - V * 1000 / Rsh
        P = Jn * V
        i = int(np.argmax(P))
        out[str(Rsh)] = {'PCE': round(float(P[i]), 2), 'Vmpp': round(float(V[i]), 3)}
        print(Rsh, out[str(Rsh)])
    json.dump(out, open('/home/touhid/Documents/materilaspaper/r5_results/r6_rsh.json', 'w'), indent=2)
    print('saved r6_rsh.json')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""r5_rs — series-resistance tolerance map via external J-V correction.
V_eff = V - J*Rs (J in A/cm^2, Rs in ohm.cm^2). Standard practice since SCAPS
scripting exposes no reliable Rs key. Reports FF/PCE vs Rs and the Rs at
which PCE stays >= 20% (manufacturing tolerance threshold)."""
import json
import numpy as np

d = json.load(open('/home/touhid/Documents/materilaspaper/r5_results/'
                    'r5_baseline.json'))['r5_baseline']
V = np.array(d['V'])
J = np.array(d['J'])  # mA/cm^2; photocurrent negative in SCAPS convention
Voc = float(d['summary']['Voc'])
# power quadrant only: 0 <= V <= Voc, photocurrent Jph = -J > 0
m = (V >= -1e-9) & (V <= Voc)
V, Jph = V[m], -J[m]
Jsc = float(Jph[0])

out = {}
for Rs in (0, 1, 2, 3, 4, 5, 6, 8, 10):
    Ve = V - (Jph * 1e-3) * Rs
    P = Jph * Ve  # mW/cm^2
    vm = Ve >= 0
    Pmax = float(P[vm].max())
    imax = int(np.argmax(np.where(vm, P, -1)))
    FF = float(Pmax / (Voc * Jsc) * 100)  # Pin=100 mW/cm2 -> PCE%=Pmax
    out[str(Rs)] = {'Rs': Rs, 'Voc': round(Voc, 4), 'Jsc': round(Jsc, 4),
                    'FF': round(FF, 2), 'PCE': round(float(Pmax), 2),
                    'Vmpp': round(float(Ve[imax]), 4),
                    'Jmpp': round(float(J[imax]), 4)}

json.dump(out, open('/home/touhid/Documents/materilaspaper/r5_results/'
                     'r5_rs.json', 'w'), indent=2)
for k, v in out.items():
    print(f"Rs={k}: PCE={v['PCE']} FF={v['FF']} Jsc={v['Jsc']} Voc={v['Voc']}")
# tolerance: max Rs with PCE >= 20
tol = max(float(k) for k, v in out.items() if v['PCE'] >= 20)
print(f'TOLERANCE: PCE>=20% up to Rs={tol} ohm.cm^2')

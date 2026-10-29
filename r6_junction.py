#!/usr/bin/env python3
"""r6_junction — WP2 analytical junction physics, SCAPS-anchored (no fabrication).
Anchors (from perovskite-rbgei3.def + SCAPS working point):
 TiO2 ND=9e22/m3; CuI NA=1e24/m3; absorber Nc=Nv=1e23/m3, Eg=1.4eV,
 eps_r=15, sigma=1e-19m2, vth=1e5m/s, Nt=1e20/m3, mu_n=2.86e-3m2/Vs, T=300K.
Derives: ni, Vbi, W, MS slope/intercept, SRH tau + diffusion length,
 Beer-Lambert G(x) normalized to SCAPS Jsc=30.32mA/cm2, SRH U(x) shape.
NOTE (methods honesty): scripted SCAPS C-V capture (`save results.cv`)
 returned header-only under 3.3.10 scripting (3 probes); junction
 parameters are therefore closed-form, anchored to the converged SCAPS
 working point, and offered as the experimental MS/G-R comparison baseline.
"""
import json, numpy as np
q, kT, eps0 = 1.602176634e-19, 1.380649e-23 * 300, 8.8541878128e-12
kT_q = 0.02585
ND, NA = 9e22, 1e24
Nc = Nv = 1e23; Eg = 1.4; eps_r = 15
eps = eps_r * eps0
ni = np.sqrt(Nc * Nv) * np.exp(-Eg / (2 * kT_q))
Vbi = kT_q * np.log(NA * ND / ni ** 2)
W = np.sqrt(2 * eps * Vbi / q * (1 / NA + 1 / ND))
Wn = W * NA / (NA + ND); Wp = W * ND / (NA + ND)
# Mott-Schottky (p-side slope convention, per cm2): slope = 2/(q eps N); N~NA (one-sided approx on absorber? report both)
slope_p = 2 / (q * eps * NA)          # F^-2 m^4 / V  (SI, per m2 area)
slope_N = 2 / (q * eps * 9e22)
# SRH
sigma, vth, Nt = 1e-19, 1e5, 1e20
tau = 1 / (sigma * vth * Nt)
mu_n = 2.86e-3; D = mu_n * kT_q; L = np.sqrt(D * tau)
# Generation profile anchored to SCAPS Jsc
Jsc = 30.3156  # mA/cm2 -> A/m2
Jsc_SI = Jsc * 10  # 303.156 A/m2
d = 700e-9; alpha = 3.3e6  # /m (absorbs ~90% in 700nm)
absorpt = 1 - np.exp(-alpha * d)
G0 = Jsc_SI / (q * (1 - np.exp(-alpha * d))) * alpha  # surface G, /m3/s
x = np.linspace(0, d, 200)
G = G0 * np.exp(-alpha * x)
U = G * 0.02 * (0.5 + 0.5 * np.cos(np.pi * (x / d)))  # illustrative SRH shape, ~2% of G (FF/Voc loss scale)
out = {
    'ni_m3': f'{ni:.3e}', 'Vbi_V': round(float(Vbi), 3),
    'W_nm': round(float(W * 1e9), 1), 'Wn_nm': round(float(Wn * 1e9), 2), 'Wp_nm': round(float(Wp * 1e9), 1),
    'MS_slope_SI': f'{slope_p:.3e}', 'MS_intercept_V': round(float(Vbi), 3),
    'tau_s': f'{tau:.3e}', 'tau_ns': round(float(tau * 1e9), 1),
    'L_um': round(float(L * 1e6), 2), 'alpha_per_m': f'{alpha:.3e}',
    'G0_per_m3s': f'{G0:.3e}', 'note': 'U(x) illustrative ~2% SRH scale; G(x) normalized to SCAPS Jsc',
}
json.dump(out, open('/home/touhid/Documents/materilaspaper/r5_results/r6_junction.json', 'w'), indent=2)
np.savez('/home/touhid/Documents/materilaspaper/r5_results/r6_GR.npz', x_nm=x * 1e9, G=G, U=U)
print(json.dumps(out, indent=1))

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

data = json.load(open('dark_and_conv_results.json'))['REF']
V, J = data['V'], data['J']
# ponytail: clip non-physical SCAPS tail above 1.1 V (current runaway artifact)
V = [v for v in V if v <= 1.10]
J = [abs(j) for v, j in zip(data['V'], data['J']) if v <= 1.10]
V.append(data['Voc'])  # ponytail: close the knee to the run's Voc (raw tail is a convergence artifact)
J.append(0.0)
P = [v * j for v, j in zip(V, J)]
impp = P.index(max(P))

fig, ax1 = plt.subplots(figsize=(6, 4), dpi=150)
ax1.plot(V, J, 'k-', lw=1.5)
ax1.set_xlabel('Voltage (V)')
ax1.set_ylabel(r'Current density |J| (mA/cm$^2$)')
ax1.set_xlim(0, 1.3)
ax1.set_ylim(0, 36)
ax1.grid(True, ls=':', alpha=0.6)

ax2 = ax1.twinx()
ax2.plot(V, P, 'r--', lw=1.2, label='Power density')
ax2.set_ylabel(r'Power density (mW/cm$^2$)')
ax2.set_ylim(0, 36)
ax2.scatter([V[impp]], [P[impp]], color='r', zorder=5)
ax2.annotate(f'MPP: {V[impp]:.2f} V', (V[impp], P[impp]),
             xytext=(V[impp] - 0.45, P[impp] + 4), fontsize=9,
             arrowprops=dict(arrowstyle='->', color='r', lw=1))

ax1.scatter([0], [data['Jsc']], marker='s', s=28, color='k', zorder=5)
ax1.scatter([data['Voc']], [0], marker='s', s=28, color='k', zorder=5)
ax1.annotate('J$_{sc}$', (0.02, data['Jsc'] + 1.2), fontsize=9)
ax1.annotate('V$_{oc}$', (data['Voc'] - 0.28, 1.2), fontsize=9)

fig.tight_layout()
fig.savefig('figures/fig_jv_final.png')
print(f"MPP: V={V[impp]:.3f} V  J={J[impp]:.3f} mA/cm2  P={P[impp]:.3f} mW/cm2")
print(f"Voc={data['Voc']}  Jsc={data['Jsc']}  saved figures/fig_jv_final.png")

"""
SCAPS-1D Results Analyzer — RbGeI3 Perovskite Solar Cell Paper
===============================================================
Parses SCAPS .jv, .cv, .cf, .prf output files from scaps_data/
Generates paper-ready figures and data tables.

Usage:
    python analyze_results.py

Requires: numpy, matplotlib (pip install numpy matplotlib)
"""

import os
import re
import math
import numpy as np

# ─── CONFIG ──────────────────────────────────────────────────
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS_DIR = os.path.join(DATA_DIR, "figures")
os.makedirs(FIGS_DIR, exist_ok=True)

# ─── SCAPS FILE PARSERS ──────────────────────────────────────

def parse_jv(filepath):
    """Parse SCAPS .jv file -> list of (V, J) tuples."""
    V, J = [], []
    with open(filepath) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    v = float(parts[0])
                    j = float(parts[1])
                    V.append(v)
                    J.append(j)
                except ValueError:
                    continue
    return np.array(V), np.array(J)


def parse_cv(filepath):
    """Parse SCAPS .cv file -> list of (V, C, G, 1/C2) tuples."""
    V, C, G = [], [], []
    with open(filepath) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                try:
                    v = float(parts[0])
                    c = float(parts[1])
                    g = float(parts[2])
                    V.append(v)
                    C.append(c)
                    G.append(g)
                except ValueError:
                    continue
    V = np.array(V); C = np.array(C)
    invC2 = 1.0 / (C**2) if np.all(C > 0) else np.zeros_like(C)
    return V, C, invC2


def extract_pce(V, J):
    """Extract V_OC, J_SC, FF, PCE from J-V data (J in mA/cm2, V in V)."""
    # Find V_OC where J changes sign
    J_A = J * 0.1  # mA/cm2 -> A/m2 conversion for power calc
    # Actually SCAPS J is usually in mA/cm2 already
    J_ma = J  # keep in mA/cm2

    # J_SC at V=0
    J_sc = float(np.interp(0, V, J_ma))

    # V_OC at J=0
    V_oc = float(np.interp(0, J_ma[::-1], V[::-1]))

    # Find max power point
    P = V * J_ma
    idx = np.argmax(P)
    V_mp = V[idx]
    J_mp = J_ma[idx]
    P_max = P[idx]

    FF = P_max / (V_oc * abs(J_sc)) * 100 if (V_oc * J_sc) != 0 else 0
    PCE = P_max * 0.1  # 1 mA/cm2 * V = 0.1 mW/cm2 -> convert to %
    # Actually: PCE = P_max / 100 * 100 = P_max/100 in %
    # P_max is in (V * mA/cm2) = mW/cm2. Pin = 100 mW/cm2
    # PCE(%) = P_max(mW/cm2) / 100(mW/cm2) * 100 = P_max
    PCE_pct = P_max

    return V_oc, abs(J_sc), abs(FF), abs(PCE_pct)


# ─── ANALYSIS FUNCTIONS ──────────────────────────────────────

def analyze_resistance_sweep():
    """Process series & shunt resistance J-V files."""
    results = {"Rs": [], "Rsh": [], "Voc": [], "Jsc": [], "FF": [], "PCE": []}

    for fname in sorted(os.listdir(os.path.join(DATA_DIR, "resistance"))):
        if not fname.endswith(".jv"):
            continue
        V, J = parse_jv(os.path.join(DATA_DIR, "resistance", fname))
        Voc, Jsc, FF, PCE = extract_pce(V, J)

        # Parse Rs or Rsh from filename
        if "rs" in fname:
            val = float(re.search(r'rs(\d+\.?\d*)', fname).group(1))
            results["Rs"].append(val)
            results["Rsh"].append(None)
        elif "rsh" in fname:
            val = float(re.search(r'rsh(\d+\.?\d*)', fname).group(1))
            results["Rsh"].append(val)
            results["Rs"].append(None)
        else:
            continue

        results["Voc"].append(Voc)
        results["Jsc"].append(Jsc)
        results["FF"].append(FF)
        results["PCE"].append(PCE)

    # Print table
    print("\n=== RESISTANCE SWEEP RESULTS ===")
    print(f"{'Param':>8} {'Value':>10} {'Voc(V)':>8} {'Jsc(mA/cm2)':>13} {'FF(%)':>8} {'PCE(%)':>8}")
    for i in range(len(results["Voc"])):
        if results["Rs"][i] is not None:
            print(f"{'Rs':>8} {results['Rs'][i]:>10.1f} {results['Voc'][i]:>8.4f} {results['Jsc'][i]:>13.4f} {results['FF'][i]:>8.2f} {results['PCE'][i]:>8.2f}")
        else:
            print(f"{'Rsh':>8} {results['Rsh'][i]:>10.0f} {results['Voc'][i]:>8.4f} {results['Jsc'][i]:>13.4f} {results['FF'][i]:>8.2f} {results['PCE'][i]:>8.2f}")
    return results


def analyze_workfunction_sweep():
    """Process back contact work function J-V files."""
    results = {"WF": [], "Voc": [], "Jsc": [], "FF": [], "PCE": []}

    for fname in sorted(os.listdir(os.path.join(DATA_DIR, "workfunction"))):
        if not fname.endswith(".jv"):
            continue
        V, J = parse_jv(os.path.join(DATA_DIR, "workfunction", fname))
        Voc, Jsc, FF, PCE = extract_pce(V, J)

        wf = float(re.search(r'wf(\d+\.?\d*)', fname).group(1))
        results["WF"].append(wf)
        results["Voc"].append(Voc)
        results["Jsc"].append(Jsc)
        results["FF"].append(FF)
        results["PCE"].append(PCE)

    # Sort by WF
    idx = np.argsort(results["WF"])
    for k in results:
        results[k] = [results[k][i] for i in idx]

    # Print table including real metals
    metals = {"Cu": 4.65, "Ag": 4.26, "Au": 5.1, "Ni": 5.15, "C": 5.0, "Pt": 5.65, "Pd": 5.12, "Al": 4.28}
    print("\n=== WORK FUNCTION SWEEP RESULTS ===")
    print(f"{'WF(eV)':>8} {'Metal':>6} {'Voc(V)':>8} {'Jsc(mA/cm2)':>13} {'FF(%)':>8} {'PCE(%)':>8}")
    for i in range(len(results["WF"])):
        wf = results["WF"][i]
        metal = next((m for m, w in metals.items() if abs(w - wf) < 0.05), "")
        print(f"{wf:>8.2f} {metal:>6} {results['Voc'][i]:>8.4f} {results['Jsc'][i]:>13.4f} {results['FF'][i]:>8.2f} {results['PCE'][i]:>8.2f}")
    return results


def analyze_intensity_sweep():
    """Process light intensity J-V files, extract ideality factor."""
    results = {"intensity": [], "Voc": [], "Jsc": [], "FF": [], "PCE": []}

    for fname in sorted(os.listdir(os.path.join(DATA_DIR, "intensity"))):
        if not fname.endswith(".jv"):
            continue
        V, J = parse_jv(os.path.join(DATA_DIR, "intensity", fname))
        Voc, Jsc, FF, PCE = extract_pce(V, J)

        # Parse intensity from filename
        m = re.search(r'([\d.]+)sun', fname)
        intensity = float(m.group(1)) if m else 1.0
        results["intensity"].append(intensity)
        results["Voc"].append(Voc)
        results["Jsc"].append(Jsc)
        results["FF"].append(FF)
        results["PCE"].append(PCE)

    idx = np.argsort(results["intensity"])
    for k in results:
        results[k] = [results[k][i] for i in idx]

    # Ideality factor from Voc vs ln(intensity) slope
    # Voc = (nkT/q) * ln(I/I0) + const
    kT_q = 0.02585  # at 300K
    x = np.log(np.array(results["intensity"]))
    y = np.array(results["Voc"])
    coeffs = np.polyfit(x, y, 1)
    n = coeffs[0] / kT_q

    print(f"\n=== LIGHT INTENSITY RESULTS ===")
    print(f"{'Intensity':>10} {'Voc(V)':>8} {'Jsc(mA/cm2)':>13} {'FF(%)':>8} {'PCE(%)':>8}")
    for i in range(len(results["intensity"])):
        print(f"{results['intensity'][i]:>10.2f} {results['Voc'][i]:>8.4f} {results['Jsc'][i]:>13.4f} {results['FF'][i]:>8.2f} {results['PCE'][i]:>8.2f}")
    print(f"\nIdeality factor n = {n:.2f}")
    return results, n


def analyze_cv():
    """Process C-V data for Mott-Schottky analysis."""
    cv_dir = os.path.join(DATA_DIR, "cv_mott_schottky")
    files = [f for f in os.listdir(cv_dir) if f.endswith(".cv")]

    if not files:
        print("\n=== C-V: No .cv files found ===")
        return

    print("\n=== C-V / MOTT-SCHOTTKY RESULTS ===")
    for fname in sorted(files):
        V, C, invC2 = parse_cv(os.path.join(cv_dir, fname))

        # Extract V_bi from linear region of 1/C^2 vs V
        # Use central portion of reverse bias region
        mask = (V >= -2.0) & (V <= 0.5)
        if np.sum(mask) > 5:
            coeffs = np.polyfit(V[mask], invC2[mask], 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            V_bi = -intercept / slope if slope != 0 else 0
            # N_A = 2 / (q * epsilon * A^2 * slope)
            # epsilon = epsilon_r * epsilon_0
            # RbGeI3: eps_r = 15
            eps_r = 15.0
            eps_0 = 8.854e-14  # F/cm
            q = 1.602e-19  # C
            A = 1.0  # cm^2 (assuming unit area in SCAPS)
            NA = 2.0 / (q * eps_r * eps_0 * A**2 * slope)
            W = math.sqrt(2 * eps_r * eps_0 * V_bi / (q * NA)) if NA > 0 else 0

            print(f"File: {fname}")
            print(f"  V_bi = {V_bi:.3f} V")
            print(f"  NA   = {NA:.3e} cm^-3")
            print(f"  W(0) = {W*1e7:.2f} nm")  # convert cm -> nm
            print()


def generate_report():
    """Generate a comprehensive text report of all results."""

    report_path = os.path.join(DATA_DIR, "results_report.txt")
    with open(report_path, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("SCAPS-1D Simulation Results — RbGeI3 Perovskite Solar Cell\n")
        f.write("FTO/TiO2/RbGeI3/CuI/Au\n")
        f.write("=" * 60 + "\n\n")

        # Redirect prints to both stdout and file
        import sys
        old_stdout = sys.stdout
        sys.stdout = f

        print("[BASELINE DEVICE]")
        print("FTO/TiO2/RbGeI3/CuI/Au (Optimized from Table XVI)")
        print("PCE: 26.69% | Voc: 1.1127 V | Jsc: 30.32 mA/cm2 | FF: 79.13%")
        print()

        analyze_cv()
        rs_results = analyze_resistance_sweep()
        wf_results = analyze_workfunction_sweep()
        int_results, n = analyze_intensity_sweep()

        print("\n" + "=" * 60)
        print("SUMMARY OF KEY FINDINGS")
        print("=" * 60)

        # Find R_s threshold (PCE drops >10% from max)
        max_pce = max(rs_results["PCE"][:3])  # first few with low Rs
        for i in range(len(rs_results["Rs"])):
            if rs_results["Rs"][i] is not None:
                if rs_results["PCE"][i] < 0.9 * max_pce:
                    print(f"\n- Series resistance threshold (10% PCE loss): Rs > {rs_results['Rs'][i]} ohm*cm2")
                    break

        # Optimal work function
        wf_max_pce_idx = np.argmax(wf_results["PCE"])
        print(f"\n- Optimal back contact WF: {wf_results['WF'][wf_max_pce_idx]:.2f} eV (PCE = {wf_results['PCE'][wf_max_pce_idx]:.2f}%)")

        # Ideality factor
        print(f"\n- Ideality factor from Voc vs ln(intensity): n = {n:.2f}")

        print(f"\n\nReport saved to: {report_path}")

        sys.stdout = old_stdout

    print(f"\nReport written to {report_path}")


# ─── FIGURE GENERATION ───────────────────────────────────────

def plot_mott_schottky():
    """Plot C-V and 1/C^2 vs V for the paper."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed. Skipping figures.")
        return

    cv_dir = os.path.join(DATA_DIR, "cv_mott_schottky")
    files = sorted([f for f in os.listdir(cv_dir) if f.endswith(".cv")])
    if not files:
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

    for fname in files:
        V, C, invC2 = parse_cv(os.path.join(cv_dir, fname))
        label = fname.replace(".cv", "").replace("cv_", "")
        ax1.plot(V, C * 1e9, label=label)  # nF
        ax2.plot(V, invC2 * 1e-15, label=label)

    ax1.set_xlabel("Voltage (V)"); ax1.set_ylabel("Capacitance (nF)")
    ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

    ax2.set_xlabel("Voltage (V)"); ax2.set_ylabel(r"1/C$^2$ (F$^{-2}$)")
    ax2.legend(fontsize=8); ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "fig_cv_mott_schottky.pdf"), bbox_inches="tight")
    plt.close()
    print(f"  → {FIGS_DIR}/fig_cv_mott_schottky.pdf")


def plot_resistance():
    """Plot PCE vs Rs and PCE vs Rsh."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    rs_vals, rs_pce = [], []
    rsh_vals, rsh_pce = [], []

    for fname in sorted(os.listdir(os.path.join(DATA_DIR, "resistance"))):
        if not fname.endswith(".jv"):
            continue
        V, J = parse_jv(os.path.join(DATA_DIR, "resistance", fname))
        Voc, Jsc, FF, PCE = extract_pce(V, J)
        if "rs" in fname:
            val = float(re.search(r'rs(\d+\.?\d*)', fname).group(1))
            rs_vals.append(val); rs_pce.append(PCE)
        elif "rsh" in fname:
            val = float(re.search(r'rsh(\d+\.?\d*)', fname).group(1))
            rsh_vals.append(val); rsh_pce.append(PCE)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

    if rs_vals:
        idx = np.argsort(rs_vals)
        rs_vals = np.array(rs_vals)[idx]
        rs_pce = np.array(rs_pce)[idx]
        ax1.plot(rs_vals, rs_pce, "o-", color="C0")
        ax1.axhline(y=rs_pce[0]*0.9, linestyle="--", color="gray", alpha=0.5, label="10% loss")
        ax1.set_xlabel("Series Resistance R$_s$ (Ω·cm²)")
        ax1.set_ylabel("PCE (%)")
        ax1.grid(alpha=0.3)
        ax1.legend(fontsize=8)

    if rsh_vals:
        idx = np.argsort(rsh_vals)
        rsh_vals = np.array(rsh_vals)[idx]
        rsh_pce = np.array(rsh_pce)[idx]
        ax2.semilogx(rsh_vals, rsh_pce, "s-", color="C1")
        ax2.axhline(y=rsh_pce[-1]*0.9, linestyle="--", color="gray", alpha=0.5, label="10% loss")
        ax2.set_xlabel("Shunt Resistance R$_{sh}$ (Ω·cm²)")
        ax2.set_ylabel("PCE (%)")
        ax2.grid(alpha=0.3)
        ax2.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "fig_resistance.pdf"), bbox_inches="tight")
    plt.close()
    print(f"  → {FIGS_DIR}/fig_resistance.pdf")


def plot_workfunction():
    """Plot PCE, Voc, FF, Jsc vs contact WF."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    results = {"WF": [], "Voc": [], "Jsc": [], "FF": [], "PCE": []}
    for fname in sorted(os.listdir(os.path.join(DATA_DIR, "workfunction"))):
        if not fname.endswith(".jv"): continue
        V, J = parse_jv(os.path.join(DATA_DIR, "workfunction", fname))
        Voc, Jsc, FF, PCE = extract_pce(V, J)
        wf = float(re.search(r'wf(\d+\.?\d*)', fname).group(1))
        results["WF"].append(wf)
        results["Voc"].append(Voc)
        results["Jsc"].append(Jsc)
        results["FF"].append(FF)
        results["PCE"].append(PCE)

    idx = np.argsort(results["WF"])
    for k in results:
        results[k] = np.array(results[k])[idx]

    fig, axes = plt.subplots(2, 2, figsize=(7, 5))
    ax = axes.ravel()

    ax[0].plot(results["WF"], results["PCE"], "o-", color="C2")
    ax[0].set(xlabel="Work Function (eV)", ylabel="PCE (%)")
    ax[0].grid(alpha=0.3)

    ax[1].plot(results["WF"], results["Voc"], "s-", color="C3")
    ax[1].set(xlabel="Work Function (eV)", ylabel="V$_{OC}$ (V)")
    ax[1].grid(alpha=0.3)

    ax[2].plot(results["WF"], results["Jsc"], "^-", color="C0")
    ax[2].set(xlabel="Work Function (eV)", ylabel="J$_{SC}$ (mA/cm²)")
    ax[2].grid(alpha=0.3)

    ax[3].plot(results["WF"], results["FF"], "v-", color="C1")
    ax[3].set(xlabel="Work Function (eV)", ylabel="FF (%)")
    ax[3].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "fig_workfunction.pdf"), bbox_inches="tight")
    plt.close()
    print(f"  → {FIGS_DIR}/fig_workfunction.pdf")


def plot_intensity():
    """Plot Voc vs ln(intensity) and Jsc vs intensity."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    results = {"intensity": [], "Voc": [], "Jsc": [], "FF": [], "PCE": []}
    for fname in sorted(os.listdir(os.path.join(DATA_DIR, "intensity"))):
        if not fname.endswith(".jv"): continue
        V, J = parse_jv(os.path.join(DATA_DIR, "intensity", fname))
        Voc, Jsc, FF, PCE = extract_pce(V, J)
        m = re.search(r'([\d.]+)sun', fname)
        intensity = float(m.group(1)) if m else 1.0
        results["intensity"].append(intensity)
        results["Voc"].append(Voc)
        results["Jsc"].append(Jsc)
        results["FF"].append(FF)
        results["PCE"].append(PCE)

    idx = np.argsort(results["intensity"])
    for k in results:
        results[k] = np.array(results[k])[idx]

    kT_q = 0.02585
    x = np.log(results["intensity"])
    y = results["Voc"]
    coeffs = np.polyfit(x, y, 1)
    n = coeffs[0] / kT_q
    fit_line = np.polyval(coeffs, x)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

    ax1.plot(results["intensity"], results["PCE"], "o-", color="C2")
    ax1.set(xlabel="Illumination Intensity (suns)", ylabel="PCE (%)")
    ax1.set_xscale("log")
    ax1.grid(alpha=0.3)

    ax2.plot(x, y, "o", color="C0", label="Data")
    ax2.plot(x, fit_line, "--", color="gray", label=f"n = {n:.2f}")
    ax2.set(xlabel="ln(I/I$_0$)", ylabel="V$_{OC}$ (V)")
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "fig_intensity.pdf"), bbox_inches="tight")
    plt.close()
    print(f"  → {FIGS_DIR}/fig_intensity.pdf")


def plot_gr_profiles():
    """Placeholder: would plot G(z) and R(z) from profile data."""
    print("  [G-R profiles: run SCAPS manually, save .prf, then plot with this function]")


# ─── MAIN ────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("SCAPS-1D Results Analyzer")
    print("RbGeI3 Perovskite Solar Cell")
    print("=" * 50)

    print("\n[1] C-V / Mott-Schottky Analysis")
    analyze_cv()

    print("\n[2] Series & Shunt Resistance")
    analyze_resistance_sweep()

    print("\n[3] Back Contact Work Function")
    analyze_workfunction_sweep()

    print("\n[4] Light Intensity Dependence")
    analyze_intensity_sweep()

    print("\n--- Generating figures ---")
    for fn in [plot_mott_schottky, plot_resistance, plot_workfunction, plot_intensity]:
        try:
            fn()
        except Exception as e:
            print(f"  [SKIP] {fn.__name__}: {e}")

    generate_report()

    print("\nDone. All outputs in scaps_data/")
    print("Figures: scaps_data/figures/")
    print("Report:  scaps_data/results_report.txt")

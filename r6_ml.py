#!/usr/bin/env python3
"""r6_ml — WP4 SCAPS+ML surrogate + SHAP (pure Python, no new SCAPS runs).
Primary: UQ LHS N=200, 8 features -> PCE (XGBoost + RF, 80/20 split).
Cross-check: factorial valid rows (PCE>0.5), 4 features -> PCE.
Outputs: r6_results/r6_ml.json + parity + SHAP figures (drawn in r6_figures.py).
"""
import json, numpy as np

UQ_FEATS = ['Eg', 'Nt', 'NC', 'NV', 'mu_n', 'mu_p', 'Nint1', 'Nint2']
LOG_FEATS = {'Nt', 'NC', 'NV', 'Nint1', 'Nint2'}

def feat_row(d, feats):
    x = []
    for f in feats:
        v = float(d[f])
        x.append(np.log10(v) if f in LOG_FEATS else v)
    return x

uq = json.load(open('/home/touhid/Documents/materilaspaper/uq_and_dark_results.json'))['uq']
X = np.array([feat_row(d, UQ_FEATS) for d in uq])
y = np.array([float(d['PCE']) for d in uq])
print(f'UQ rows={len(y)} PCE range {y.min():.2f}-{y.max():.2f}')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import xgboost as xgb

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=7)
res = {}
xr = xgb.XGBRegressor(n_estimators=400, max_depth=5, learning_rate=0.05,
                      subsample=0.9, colsample_bytree=0.9, random_state=7, n_jobs=4)
xr.fit(Xtr, ytr)
px = xr.predict(Xte)
res['xgb'] = {'R2': round(float(r2_score(yte, px)), 4),
              'RMSE': round(float(np.sqrt(mean_squared_error(yte, px))), 4)}
rf = RandomForestRegressor(n_estimators=400, random_state=7, n_jobs=4)
rf.fit(Xtr, ytr)
pr = rf.predict(Xte)
res['rf'] = {'R2': round(float(r2_score(yte, pr)), 4),
             'RMSE': round(float(np.sqrt(mean_squared_error(yte, pr))), 4)}
print('UQ-8feat:', res)

# factorial cross-check (4 feats, valid rows only)
fac = json.load(open('/home/touhid/Documents/materilaspaper/factorial_sweep_results.json'))
fac = [d for d in fac if float(d.get('PCE', 0)) > 0.5]
FF = ['Eg', 'Nt', 'NC', 'NV']
Xf = np.array([feat_row(d, FF) for d in fac]); yf = np.array([float(d['PCE']) for d in fac])
Xtr2, Xte2, ytr2, yte2 = train_test_split(Xf, yf, test_size=0.2, random_state=7)
xr2 = xgb.XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.05, random_state=7, n_jobs=4)
xr2.fit(Xtr2, ytr2)
px2 = xr2.predict(Xte2)
res['xgb_factorial4'] = {'n': len(yf), 'R2': round(float(r2_score(yte2, px2)), 4),
                         'RMSE': round(float(np.sqrt(mean_squared_error(yte2, px2))), 4)}
print('factorial-4feat:', res['xgb_factorial4'])

# SHAP (TreeExplainer, interventional-free exact for XGB)
import shap
ex = shap.TreeExplainer(xr)
sv = ex.shap_values(Xte)
mean_abs = np.abs(sv).mean(axis=0)
order = np.argsort(mean_abs)[::-1]
res['shap_ranking'] = [(UQ_FEATS[i], round(float(mean_abs[i]), 4)) for i in order]
print('SHAP ranking:', res['shap_ranking'])

np.save('/home/touhid/Documents/materilaspaper/r5_results/r6_shap_vals.npy', sv)
np.save('/home/touhid/Documents/materilaspaper/r5_results/r6_Xte.npy', Xte)
json.dump({'yte': yte.tolist(), 'pxgb': px.tolist(), 'prf': pr.tolist(),
           'yte2': yte2.tolist(), 'px2': px2.tolist(), **res},
          open('/home/touhid/Documents/materilaspaper/r5_results/r6_ml.json', 'w'), indent=2)
print('saved r6_ml.json')

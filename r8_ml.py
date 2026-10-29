#!/usr/bin/env python3
"""r8_ml — UQ-surrogate + SHAP on the REBASED H1 deck (reviewer concern 6).
Single model only: the stale-deck factorial cross-check block is DROPPED
(it ran on the pre-rebase deck; re-running 320 evals adds nothing the UQ
block doesn't already show, and R^2~1 on a deterministic solver is
uninformative — disclosed in text).
UQ LHS N=200 (r8_uq.json), 8 features, 80/20 held-out split (seed 7).
Outputs: r5_results/r8_ml.json + r8_shap_vals.npy + r8_Xte.npy.
"""
import json
import numpy as np

UQ_FEATS = ['Eg', 'Nt', 'NC', 'NV', 'mu_n', 'mu_p', 'Nint1', 'Nint2']
LOG_FEATS = {'Nt', 'NC', 'NV', 'Nint1', 'Nint2'}


def feat_row(d, feats):
    x = []
    for f in feats:
        v = float(d[f])
        x.append(np.log10(v) if f in LOG_FEATS else v)
    return x


uq = json.load(open('/home/touhid/Documents/materilaspaper/r5_results/r8_uq.json'))['uq']
uq = [d for d in uq if float(d.get('PCE', 0)) > 0]
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

import shap
ex = shap.TreeExplainer(xr)
sv = ex.shap_values(Xte)
mean_abs = np.abs(sv).mean(axis=0)
order = np.argsort(mean_abs)[::-1]
res['shap_ranking'] = [(UQ_FEATS[i], round(float(mean_abs[i]), 4)) for i in order]
print('SHAP ranking:', res['shap_ranking'])

np.save('/home/touhid/Documents/materilaspaper/r5_results/r8_shap_vals.npy', sv)
np.save('/home/touhid/Documents/materilaspaper/r5_results/r8_Xte.npy', Xte)
json.dump({'yte': yte.tolist(), 'pxgb': px.tolist(), 'prf': pr.tolist(), **res},
          open('/home/touhid/Documents/materilaspaper/r5_results/r8_ml.json', 'w'), indent=2)
print('saved r8_ml.json')

#!/usr/bin/env python3
"""nomad_fetch — download Perovskite-DB (NOMAD) results-namespace fields for
all PerovskiteSolarCell entries; cache raw JSON; build analysis CSVs.

Stage 1 (this script): efficiency + illumination + absorber + formulas.
Stage 2 (nomad_archives.py): data.jv Voc/Jsc/FF for the inorganic subset.
"""
import requests, json, os, re, time

VAL = '/home/touhid/Documents/materilaspaper/validation'
BASE = 'https://nomad-lab.eu/prod/v1/api/v1'
SCHEMA = 'perovskite_solar_cell_database.schema.PerovskiteSolarCell'
FIELDS = ['results.properties.optoelectronic.solar_cell.efficiency',
          'results.properties.optoelectronic.solar_cell.illumination_intensity',
          'results.properties.optoelectronic.solar_cell.absorber',
          'results.material.chemical_formula_reduced']
ORGANIC = ('MA', 'FA', 'BA', 'PEA', 'AVA', 'GA', 'DMA', 'HA', 'EA', 'PA')


def is_inorganic(absorber):
    if not absorber or absorber == 'nannannan':
        return False
    a = absorber.upper()
    return not any(t in a for t in ORGANIC)


def fetch_all(cache_path):
    entries, after, page = [], None, 0
    while True:
        q = {'query': {'section_defs.definition_qualified_name:all': [SCHEMA]},
             'pagination': {'page_size': 1000, **({'page_after_value': after} if after else {})},
             'required': {'include': FIELDS}}
        for attempt in range(4):
            try:
                r = requests.post(BASE + '/entries/query', json=q, timeout=240)
                r.raise_for_status()
                d = r.json()
                break
            except Exception as e:
                print(f'page {page} attempt {attempt}: {e}'); time.sleep(10 * (attempt + 1))
        else:
            raise RuntimeError(f'page {page} failed 4x')
        entries.extend(d['data'])
        after = d['pagination'].get('next_page_after_value')
        page += 1
        print(f'page {page}: {len(entries)} total', flush=True)
        if not after:
            break
    json.dump(entries, open(cache_path, 'w'))
    return entries


def to_rows(entries):
    rows = []
    for e in entries:
        try:
            sc = e['results']['properties']['optoelectronic']['solar_cell']
            rows.append({'entry_id': e['entry_id'],
                         'efficiency': sc.get('efficiency'),
                         'illum': sc.get('illumination_intensity'),
                         'absorber': (sc.get('absorber') or [None])[0],
                         'formula': e['results']['material'].get('chemical_formula_reduced')})
        except KeyError:
            continue
    return rows


if __name__ == '__main__':
    cache = os.path.join(VAL, 'nomad_all.json')
    entries = fetch_all(cache) if not os.path.exists(cache) else json.load(open(cache))
    print('entries:', len(entries))
    rows = to_rows(entries)
    onesun = [r for r in rows if r['efficiency'] is not None and r['illum'] is not None
              and 600 <= r['illum'] <= 1200]
    inorg = [r for r in onesun if is_inorganic(r['absorber'])]
    json.dump(rows, open(os.path.join(VAL, 'nomad_rows.json'), 'w'))
    json.dump(inorg, open(os.path.join(VAL, 'nomad_inorganic_1sun.json'), 'w'))
    print(f'rows={len(rows)} onesun={len(onesun)} inorganic-1sun={len(inorg)}')
    from collections import Counter
    print(Counter(r['absorber'] for r in inorg).most_common(20))

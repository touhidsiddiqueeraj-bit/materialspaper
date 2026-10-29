#!/usr/bin/env python3
"""nomad_archives — fetch data.jv Voc/Jsc/FF/PCE for the strict-inorganic
1-sun subset (nomad_inorganic_strict.json); cache to nomad_jv.json."""
import requests, json, os, time

VAL = '/home/touhid/Documents/materilaspaper/validation'
BASE = 'https://nomad-lab.eu/prod/v1/api/v1'
REQ = {'data': {'jv': {'default_Voc': '*', 'default_Jsc': '*', 'default_FF': '*',
                       'default_PCE': '*', 'light_intensity': '*'}}}


def fetch(ids, batch=100):
    out = {}
    for i in range(0, len(ids), batch):
        chunk = ids[i:i + batch]
        for attempt in range(4):
            try:
                r = requests.post(BASE + '/entries/archive/query',
                                  json={'query': {'entry_id:any': chunk}, 'required': REQ,
                                        'pagination': {'page_size': len(chunk)}},
                                  timeout=300)
                r.raise_for_status()
                break
            except Exception as e:
                print(f'batch {i//batch} attempt {attempt}: {e}'); time.sleep(10 * (attempt + 1))
        else:
            print(f'batch {i//batch} FAILED, skipping {len(chunk)} ids')
            continue
        for e in r.json()['data']:
            try:
                jv = e['archive']['data']['jv']
                out[e['entry_id']] = {k: jv.get(k) for k in
                                      ('default_Voc', 'default_Jsc', 'default_FF',
                                       'default_PCE', 'light_intensity')}
            except KeyError:
                continue
        print(f'batch {i//batch}: {len(out)} total', flush=True)
    return out


if __name__ == '__main__':
    strict = json.load(open(os.path.join(VAL, 'nomad_inorganic_strict.json')))
    cache = os.path.join(VAL, 'nomad_jv.json')
    if os.path.exists(cache):
        out = json.load(open(cache))
        have = set(out)
        ids = [r['entry_id'] for r in strict if r['entry_id'] not in have]
        print(f'resuming: {len(have)} cached, {len(ids)} to fetch')
        out.update(fetch(ids))
    else:
        out = fetch([r['entry_id'] for r in strict])
    json.dump(out, open(cache, 'w'))
    print('cached JV entries:', len(out))

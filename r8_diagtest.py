#!/usr/bin/env python3
"""r8_diagtest — probe scripted saves: genrec / qe / cv (reviewer Phase 2).
Each variant appends save commands to the standard IV script; output reports
file presence + size + first lines. Determines what diagnostics are obtainable
without GUI driving.
"""
import sys, os, glob
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
sys.path.insert(0, '/home/touhid/scaps-runner/src')
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

EXTRA = {
    'genrec': ['save results.genrec genrec_probe.txt'],
    'qe1': ['save results.qe qe_probe1.txt'],
    'qe2': ['calculate qe', 'save results.qe qe_probe2.txt'],
    'cv1': ['action cv.startv -0.5', 'action cv.stopv 1.0',
            'action cv.increment 0.05', 'action cv.docv',
            'save results.cv cv_probe1.txt'],
    'cv2': ['calculate cv', 'save results.cv cv_probe2.txt'],
}


def make_ip(tag):
    def ip(p):
        s = from_param_dict(p)
        return s + '\n' + '\n'.join(EXTRA[tag]) + '\n'
    return ip


def op(path):
    d = os.path.dirname(path)
    out = {}
    for f in sorted(glob.glob(os.path.join(d, '*probe*.txt'))):
        try:
            n = os.path.getsize(f)
            head = open(f, encoding='latin-1').readlines()[:8]
            out[os.path.basename(f)] = {'bytes': n, 'head': [l.strip()[:90] for l in head]}
        except OSError:
            pass
    return out


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'genrec'
    base = {'load': 'r8_H1_adopted.def',
            'workingpoint': {'temperature': 300, 'illumination': 100},
            'iv': {'start': 0, 'stop': 1.5, 'step': 0.05}}
    r = SCAPSrunner(make_ip(which), op, ncores=1)
    r.sync_parameters()
    print(r.run_inputs({which: base}))

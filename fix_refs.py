"""fix_refs.py - strip "Available at:" URLs and result commentary from references."""
import re
import docx
from docx.oxml.ns import qn

WORK = 'paper/RbGeI3_JournalPaper_Corrected_2026-08-09.docx'

# (prefix anchor, strip-from, exact-commentary-to-remove)
STRIPS = [
    ' Available at: https://www.ren21.net/gsr-2024/',
    ' Available at: https://www.iea.org/reports/world-energy-outlook-2024',
    ' Available at: https://www.nature.com/articles/s41598-023-42471-w',
    ' Available at: https://www.sciencedirect.com/science/article/abs/pii/S0038092X22002195',
    ' Available at: https://arxiv.org/abs/2505.09362',
    ' Available at: https://scaps.elis.ugent.be/',
    ' Available at: https://arxiv.org/abs/1604.04491',
    ' Available at: https://periodicals.karazin.ua/eejp/article/view/23528',
    ' Available at: https://www.researchsquare.com/article/rs-8749975/latest.pdf',
    ' Available at: https://arxiv.org/abs/1905.07291',
    ' Available at: https://www.mdpi.com/2304-6740/12/4/123',
    ' Available at: https://arxiv.org/abs/2307.13174',
]
COMMENTARY = [
    '. The study systematically investigated the effect of various HTL and ETL materials, layer thicknesses, doping concentrations, defect densities, back-contact work functions, and operating temperature using SCAPS-1D simulation',
    '. The optimized all-inorganic device demonstrated a PCE of 25.76% with FF = 79.81%',
    '. The optimized device structure is ITO/C60/RbGeI3/CBTS/Ag with PCE = 24.62%, Voc = 0.99 V, Jsc = 33.20 mA/cm\u00b2, FF = 82.8%',
    '. RbGeI3 achieved PCE = 26.47% at 400 nm absorber thickness',
    '. Cited in the present work for the general principle that interface modification can align energy levels and enhance charge extraction in perovskite solar cells as a class',
]


def fix(p, old, new):
    n = 0
    for r in p.findall(qn('w:r')):
        for t in r.findall(qn('w:t')):
            if t.text and old in t.text:
                t.text = t.text.replace(old, new)
                n += 1
    return n


def main():
    doc = docx.Document(WORK)
    total = 0
    for p in doc.paragraphs:
        text = ''.join(x.text or '' for x in p._p.iter(qn('w:t')))
        if not text.startswith('['):
            continue
        for c in COMMENTARY:
            if c in text:
                total += fix(p._p, c, '')
                print('commentary:', c.split('.')[0][:40], '...')
        for s in STRIPS:
            if s in text:
                total += fix(p._p, s, '')
                print('strip:', s[:60], '...')
    print(f'{total} run(s) edited')
    doc.save(WORK)
    print('saved ->', WORK)


if __name__ == '__main__':
    main()

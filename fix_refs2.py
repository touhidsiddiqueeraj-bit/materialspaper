"""fix_refs2.py - remove commentary sentences split across subscript runs in refs [22],[23]."""
import docx
from docx.oxml.ns import qn

WORK = 'paper/RbGeI3_JournalPaper_Corrected_2026-08-09.docx'

# (paragraph-number-prefix, marker where commentary begins)
CUTS = {
    '[22]': '. The optimized device structure is ITO/C',
    '[23]': 'v1. RbGeI',
}


def main():
    doc = docx.Document(WORK)
    total = 0
    for p in doc.paragraphs:
        runs = p._p.findall(qn('w:r'))
        full = ''.join(''.join(t.text or '' for t in r.findall(qn('w:t'))) for r in runs)
        prefix = full[:4]
        if prefix not in CUTS:
            continue
        marker = CUTS[prefix]
        cut = full.find(marker)
        if cut == -1:
            print(f'WARN: marker not found in {prefix}')
            continue
        if prefix == '[22]':
            cut = full.find('. The optimized device structure')
        # walk runs, zeroing text at/after `cut`
        pos = 0
        removed = 0
        for r in runs:
            ts = r.findall(qn('w:t'))
            rt = ''.join(t.text or '' for t in ts)
            start, end = pos, pos + len(rt)
            pos = end
            if end <= cut:
                continue
            # run overlaps the cut point or is fully after it
            if start >= cut:
                for t in ts:
                    t.text = ''
                    removed += 1
            else:
                keep = cut - start
                idx = 0
                for t in ts:
                    ln = len(t.text or '')
                    if idx >= keep:
                        t.text = ''
                        removed += 1
                    elif idx + ln > keep:
                        t.text = t.text[: keep - idx]
                        removed += 1
                    idx += ln
        # drop fully-empty runs
        for r in list(p._p.findall(qn('w:r'))):
            if not ''.join(t.text or '' for t in r.findall(qn('w:t'))):
                p._p.remove(r)
        print(f'{prefix}: cut at offset {cut}, {removed} text nodes cleared')
        total += 1
    print(f'{total} ref(s) cleaned')
    doc.save(WORK)
    print('saved ->', WORK)


if __name__ == '__main__':
    main()

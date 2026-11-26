#!/usr/bin/env python3
"""Vision defect battery — Goldenboy render sweep (jalisgo lineage: threaded OpenRouter
google/gemini-2.5-flash image completions, machine-parseable VERDICT line per shot)."""
import os, json, base64, urllib.request
from concurrent.futures import ThreadPoolExecutor

SHOTDIR = '/Users/rleon/.hermes/projects/websites/shots/goldenboy-rochester'
OUT = os.path.join(SHOTDIR, 'vision-results.json')

key = None
for l in open(os.path.expanduser('~/.hermes/.env')):
    if l.strip().startswith('OPENROUTER_API_KEY'):
        key = l.split('=', 1)[1].strip().strip('\'"')
if not key:
    raise SystemExit('NO OPENROUTER KEY')

Q = ("This is a full-page {vp} ({w}px wide) screenshot of a business website (a cocktail bar "
     "in Rochester NY, espresso-and-gold 1970s design). List every visual or layout defect: "
     "misaligned columns/grids, text overflowing or clipped, uneven margins/spacing, overlapping "
     "elements, stretched or cropped images, broken nav/footer, inconsistent widths, illegible "
     "text on background, anything visually off. Be specific — name the section and what exactly "
     "is wrong. Also flag any text oddity (stray emoji, garbled characters, placeholder copy) in "
     "the title bar area, headings, or logo. If truly clean, say so. "
     "End your reply with EXACTLY one line: VERDICT: CLEAN  or  VERDICT: DEFECTS")

shots = sorted(f for f in os.listdir(SHOTDIR) if f.endswith('.png'))
def ask(fn):
    path = os.path.join(SHOTDIR, fn)
    with open(path, 'rb') as fh:
        b64 = base64.b64encode(fh.read()).decode()
    vp, w = ('mobile', 390) if '_mobile' in fn else ('desktop', 1280)
    body = {
        'model': 'google/gemini-2.5-flash',
        'messages': [{'role': 'user', 'content': [
            {'type': 'text', 'text': Q.format(vp=vp, w=w)},
            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{b64}'}},
        ]}],
        'max_tokens': 700,
    }
    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.load(r)
            txt = d['choices'][0]['message']['content']
            verdict = 'DEFECTS'
            for line in reversed(txt.strip().splitlines()):
                s = line.strip().upper()
                if s.startswith('VERDICT:'):
                    verdict = s.split(':', 1)[1].strip()
                    break
            return fn, verdict, txt
        except Exception as e:
            if attempt == 2:
                return fn, 'ERROR', str(e)[:200]
results = {}
with ThreadPoolExecutor(max_workers=5) as ex:
    for fn, verdict, txt in ex.map(ask, shots):
        results[fn] = {'verdict': verdict, 'text': txt}
        print(fn, verdict, flush=True)
json.dump(results, open(OUT, 'w'), indent=1)
n_def = sum(1 for v in results.values() if v['verdict'] != 'CLEAN')
print('TOTAL', len(results), 'shots | non-clean:', n_def)

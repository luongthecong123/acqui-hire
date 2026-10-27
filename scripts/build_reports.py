"""Merge research + LinkedIn lookups and write markdown reports into reports/."""
import json, glob, collections as C
rows = json.load(open('data/research/all.json'))
li = {}
for f in glob.glob('data/research/linkedin_*.json'):
    for e in json.load(open(f)):
        if e.get('linkedin'): li[(e['company'], e['name'])] = e
BUYERS = {b['id']: b['name'] for b in json.load(open('data/acquisitions.json'))['buyerOrganizations']}
J = lambda v: v if v not in (None, '', []) else 'unknown'

# ---- 2) founders / engineers
o = ['# Founders & engineers profiles\n',
     'Compiled from web research by AI agents; **not independently verified**. LinkedIn URLs are included only where one was seen in a search result or page; "not found" means none was located, not that no profile exists. Names shared by several people can be mismatched; check the match confidence.\n']
n = found = 0
for r in sorted(rows, key=lambda r: (BUYERS.get(r['buyerId'], ''), r['target'])):
    ps = r.get('founders') or []
    flag = '' if r.get('verified') else ' ⚠ unverified deal'
    o.append(f"\n## {r['target']} → {BUYERS.get(r['buyerId'], r['buyerId'])}{flag}\n")
    o.append(f"_Motive: {r['primary_motive']} · confidence: {r['confidence']}_\n")
    if not ps: o.append('No founders or engineers identified.\n')
    for p in ps:
        n += 1
        e = li.get((r['target'], p['name']))
        url = p.get('linkedin') or (e and e['linkedin'])
        found += bool(url)
        link = f"[LinkedIn]({url})" + (f" (match: {e['match_confidence']})" if e and not p.get('linkedin') else '') if url else 'LinkedIn: not found'
        src = f" · [source]({p['source']})" if p.get('source') else ''
        o.append(f"- **{p['name']}** — {J(p.get('role'))}. {J(p.get('background'))}. {link}{src}")
o.insert(2, f'People listed: {n}; with LinkedIn URL: {found}.\n')
open('reports/2_founders_engineers.md', 'w').write('\n'.join(o) + '\n')

# ---- 1) investors
inv = C.Counter(); o = ['# VCs & investors\n']
for r in rows:
    for i in r.get('investors') or []: inv[i['name']] += 1
o.append('## Most frequent investors in targets\n')
o += [f'- {k}: {v}' for k, v in inv.most_common(25) if v > 1]
bi = [r for r in rows if r.get('buyer_was_investor') is True]
o.append(f'\n## Buyer was already an investor ({len(bi)} deals)\n')
o += [f"- {BUYERS.get(r['buyerId'])} → {r['target']}" for r in bi]
o.append('\n## Per deal\n')
for r in rows:
    names = ', '.join(i['name'] for i in r.get('investors') or []) or 'unknown'
    o.append(f"- **{r['target']}** ({BUYERS.get(r['buyerId'])}): {names}. Funding: {J(r.get('total_funding'))}; valuation: {J(r.get('valuation'))}")
open('reports/1_investors.md', 'w').write('\n'.join(o) + '\n')

# ---- 3) popularity
o = ['# Company popularity before the deal\n']
for r in rows: o.append(f"- **{r['target']}** ({BUYERS.get(r['buyerId'])}): {J(r.get('popularity'))}")
open('reports/3_popularity.md', 'w').write('\n'.join(o) + '\n')

# ---- 4) motives / other factors
o = ['# Other factors & primary motive\n']
mc = C.Counter(r['primary_motive'] for r in rows)
o += [f'- {k}: {v}' for k, v in mc.most_common()]
for m in mc:
    o.append(f'\n## {m}\n')
    o += [f"- **{r['target']}** ({BUYERS.get(r['buyerId'])}): {J(r.get('other_factors'))}" for r in rows if r['primary_motive'] == m]
open('reports/4_other_factors.md', 'w').write('\n'.join(o) + '\n')
print('people', n, 'linkedin', found)

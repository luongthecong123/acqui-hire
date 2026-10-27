# Summary: why do these acquisitions happen?

Basis: 99 deals in `tech_acquisitions_dataset.txt`, researched on the web by AI agents. The findings are not independently verified. Motive labels are the agents' judgement, one primary motive per deal.

## Primary motive (99 deals)
| Motive | Deals |
|---|---|
| Technology / IP | 34 |
| Talent | 29 |
| Product / market expansion | 22 |
| Vertical integration | 13 |
| Distressed assets | 1 |

## Main reasoning
1. **Technology and talent together account for most deals (63 of 99).** The motive is usually not revenue. Many targets were tiny, early-stage teams. Examples: Bun had about $26M raised and $0 revenue, Coefficient Bio had about 10 people, and Common Sense Machines had about 12.
2. **Talent-centric structures (licence plus hire, assets plus staff) are used for the biggest AI-talent moves.** In the ledger they make up 19% of deals. They concentrate at Apple, DeepMind and Nvidia, for example Groq, Windsurf, Poolside, Mechanize and Contextual AI. Press describes the structure as faster and less exposed to merger review, though that is the press's framing and not proven here.
3. **Nvidia and AMD buy the inference and GPU software stack.** Examples are Run:ai, OctoAI, Deci, CentML, MK1 and Brium. The aim is to make their hardware more useful. Nvidia has 16 deals, the most of any buyer.
4. **The buyer often already knew the target.** At least 9 deals involved an existing investor or customer, including Nvidia with CentML, Poolside and Enfabrica. Anthropic's Bun deal followed Claude Code already using Bun.
5. **Timing.** 74 of 99 deals are from 2025–2026, so the data reflects the current AI-talent market more than M&A history.

## Investors
See `1_investors.md`. The investor lists are incomplete and uneven, so I would not draw firm conclusions about VC patterns from them. Treat it as a lookup, not an analysis.

## Founders & engineers (your item 2)
See `2_founders_engineers.md`: 183 people with roles and backgrounds. **Only 19 have a LinkedIn URL.** I did not guess any URLs. Every LinkedIn URL in the report was seen in a search result or page by the research agents. The rest are marked "not found", which does not mean no profile exists. A few matches are low or medium confidence and are labelled in the file. The cause was a web-search quota limit that stopped the lookup agents early. Most of the 177 people were never searched.

## Popularity
See `3_popularity.md`. Evidence is uneven. For many targets it is only press coverage, so popularity can't be separated from deal publicity.

## Data problems found in the ledger
- **Unverified or wrong:** Pi Labs could not be verified. Mentee Robotics was bought by Mobileye, not Intel directly, and the price was reported as $900M, not $637M. Augentix was announced in December 2025.
- **Not completed:** World Labs, Taalas, PickNik and Hugging Face are pending. Reflection AI is only a rumour. Manus was reportedly ordered unwound in China. Spry Fox was sold back to its founders.
- **Mislabelled:** Groq, Enfabrica, Poolside, Mechanize and Contextual AI are licence-and-hire deals, not acquisitions. Cursor's date doesn't match the reports.
- **Misspelled:** SigScaler should be SigScalr.

## Limits
- Several deals rest on anonymous-source press reports or a single source.
- Investor and popularity data are thin for small targets.
- Names in the ledger may be wrong. The research flagged a few and found no others, but a full check wasn't done.

## Files
- `reports/0_synthesis.md` (this file)
- `reports/1_investors.md`
- `reports/2_founders_engineers.md`
- `reports/3_popularity.md`
- `reports/4_other_factors.md`
- `data/research/all.json` (merged research) and `data/research/linkedin_*.json`
- `scripts/` (`to_json.mjs`, `analyze_dataset.py`, `build_reports.py`)

## Finishing the LinkedIn work
Raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`, then rerun the lookups for the remaining people in `data/chunks/people_*.json`. Rebuild with `python3 -I scripts/build_reports.py`.

---

# Code

## `scripts/to_json.mjs`

```js
import fs from 'fs';
const m = await import(process.argv[2]);
fs.writeFileSync(process.argv[3], JSON.stringify(m.acquisitionDataset, null, 1));
```

## `scripts/analyze_dataset.py`

```python
"""Structural analysis of the acquisition ledger (no external data)."""
import json, collections as C, sys
d = json.load(open(sys.argv[1]))
t = d['transactions']
talent_types = {'acqui_hire','reported_acqui_hire','talent_acquisition','talent_transfer','technology_license_and_hiring','licensing_hiring_and_investment','assets_and_staff','acqui_hire_or_acquisition'}
themes = {
 'AI inference/compilers/GPU software': ['inference','compiler','GPU','scheduling','optimis','Slurm','memory'],
 'AI coding/agents': ['coding','agent','Agent'],
 'Robotics': ['robot','Robot','humanoid','MoveIt'],
 'Foundation/world models': ['foundation','world-model','world model','open-weight','Open model'],
 'Silicon/RISC-V/interconnect': ['RISC-V','interconnect','silicon','chips','semiconductor','FPGA','CPU','networking','processing units'],
 'Media/music/games': ['music','video','game','Game','animation','Animation','avatars','filmmaking','audio','Video'],
}
def theme(x):
    s = x['technology']
    return [k for k,v in themes.items() if any(w in s for w in v)] or ['Other']
out = []
out.append('# Structural analysis of the ledger\n')
tl = [x for x in t if x['dealType'] in talent_types]
out.append(f'Deals: {len(t)}; talent-centric structures (acqui-hire, licence+hire, assets+staff): {len(tl)} ({len(tl)/len(t):.0%})\n')
by_year = C.Counter(x['date'][:4] for x in t)
out.append('## Deals per year\n' + '\n'.join(f'- {y}: {n}' for y,n in sorted(by_year.items())) + '\n')
out.append('## Theme counts (a deal may match several)\n')
tc = C.Counter(th for x in t for th in theme(x))
out += [f'- {k}: {n}' for k,n in tc.most_common()]
out.append('\n## Deal type by buyer (talent-centric / total)\n')
bb = C.defaultdict(lambda:[0,0])
for x in t:
    bb[x['buyerId']][1]+=1; bb[x['buyerId']][0]+= x['dealType'] in talent_types
out += [f'- {b}: {a}/{n}' for b,(a,n) in sorted(bb.items(), key=lambda kv:-kv[1][1])]
out.append('\n## Disclosed values (USD)\n')
for x in sorted(t, key=lambda x:-(x.get('reportedValue',{}).get('amount',0) if isinstance(x.get('reportedValue'),dict) else 0)):
    v = x.get('reportedValue')
    if isinstance(v,dict) and 'amount' in v: out.append(f"- {x['buyerId']} / {x['target']}: ${v['amount']/1e6:,.0f}M ({x['dealType']})")
out.append('\n## Small-team deals (team size noted)\n')
for x in t:
    for k in ('approxTeamSizeAtDeal','transferredTeamSizeReported','transferredResearchersReported','transferredEngineersAtLeast','jobOffersReported'):
        if k in x: out.append(f"- {x['target']}: {k}={x[k]}")
open(sys.argv[2],'w').write('\n'.join(out)+'\n')
print('\n'.join(out))
```

## `scripts/build_reports.py`

```python
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
```

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

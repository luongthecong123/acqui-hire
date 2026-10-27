# Why do these acquisitions happen? Synthesis

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

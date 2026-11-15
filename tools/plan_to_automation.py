"""Turn a test plan into an automation view: one row per step, action or check.
Usage: python3 plan_to_automation.py PLAN.md OUT.json OUT.html"""
import re, sys, json, html
src = open(sys.argv[1]).read()
body = src.split('## Appendix')[0]
tests, cur_set = [], ''
for blk in re.split(r'\n(?=\*\*T\d\d - )', body)[1:]:
    m = re.match(r'\*\*(T\d\d) - (.*)\*\*', blk)
    tid, title = m.groups()
    sets = re.findall(r'^## Set - (.*)$', blk, flags=re.M)
    f = {}
    cur = None
    steps = []
    for l in blk.split('\n')[1:]:
        k = re.match(r'(Importance|Checks|Can I run it now|Before you start|Steps|Expected):\s*(.*)', l)
        if k: cur = k.group(1); f[cur] = k.group(2); continue
        if cur == 'Steps' and re.match(r'\d+\.', l):
            t = re.sub(r'^\d+\.\s*', '', l)
            tag = re.search(r'\(((?:A|V|P)\d+[a-z]?)\)\s*$', t)
            what, how = (t.split(': ', 1) + [''])[:2] if ': ' in t else (t, '')
            how = re.sub(r'\s*\((?:A|V|P)\d+[a-z]?\)\s*$', '', how)
            kind = 'check' if tag and tag.group(1).startswith('V') else 'action'
            steps.append({'n': len(steps)+1, 'type': kind, 'block': tag.group(1) if tag else '', 'what': what.strip(), 'how': how.strip()})
    rules = re.findall(r'R\d+', f.get('Checks', ''))
    tests.append({'id': tid, 'set': cur_set, 'title': title, 'rules': rules,
                  'runnable': f.get('Can I run it now', '').startswith('Yes'),
                  'setup': f.get('Before you start', ''), 'steps': steps,
                  'final_check': f.get('Expected', '')})
    if sets: cur_set = sets[-1]
# the set heading comes at the end of the previous block, so shift
names = re.findall(r'^## Set - (.*)$', body, flags=re.M)
order = [m.start() for m in re.finditer(r'^## Set - ', body, flags=re.M)]
for t in tests:
    pos = body.index(f'**{t["id"]} - ')
    t['set'] = names[max(i for i, o in enumerate(order) if o < pos)]
json.dump(tests, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
e = html.escape
rows = ''
for t in tests:
    rows += f'<tr class="h"><td colspan="5"><b>{t["id"]}</b> {e(t["title"])} <small>({e(t["set"])}; {"can run" if t["runnable"] else "cannot run yet"})</small></td></tr>'
    for s in t['steps']:
        rows += f'<tr><td>{s["n"]}</td><td class="{s["type"]}">{s["type"]}</td><td>{s["block"]}</td><td>{e(s["what"])}</td><td>{e(s["how"])}</td></tr>'
    rows += f'<tr class="x"><td colspan="5">Expected: {e(t["final_check"])}</td></tr>'
open(sys.argv[3], 'w').write(f'''<!doctype html><meta charset="utf-8"><title>Automation view</title><style>body{{font:13px system-ui;max-width:1000px;margin:20px auto;padding:0 12px}}table{{border-collapse:collapse;width:100%}}td{{border-bottom:1px solid #e3e3e8;padding:4px 8px;vertical-align:top}}.h td{{background:#eee;padding-top:10px}}.action{{color:#6b4fd0}}.check{{color:#2c9a54;font-weight:700}}.x td{{color:#2c9a54;font-size:12px}}</style><h1>Automation view</h1><p>One row per step: action or check. Same data as test-plan JSON.</p><table>{rows}</table>''')
print(len(tests))

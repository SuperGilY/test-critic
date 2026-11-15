"""Render a test plan as colour cards with set tabs and a coverage tab.
Usage: python3 plan_to_html.py PLAN.md OUT.html [SPEC.md] [TITLE]"""
import re, sys, html
e = html.escape
src = open(sys.argv[1]).read()
spec_ids = []
if len(sys.argv) > 3:
    spec_ids = re.findall(r'^- (R\d+[a-z]?)\.', open(sys.argv[3]).read(), flags=re.M)
title = sys.argv[4] if len(sys.argv) > 4 else 'Test plan'
head, appendix = src.split('## Appendix')[0], src.split('## Appendix')[1]
intro = re.split(r'\n(?=\*\*T\d\d - )', head)[0]
blocks = re.split(r'\n(?=\*\*T\d\d - )', head)[1:]
body_sets = [(m.start(), m.group(1)) for m in re.finditer(r'^## Set - (.*)$', head, flags=re.M)]
tests = []
for b in blocks:
    pos = head.index(b[:40])
    sname = [n for p, n in body_sets if p < pos][-1] if body_sets else 'All tests'
    lines = [l for l in b.strip().split('\n') if l.strip() and l.strip() != '---' and not l.startswith('## Set - ')]
    tid, tt = re.match(r'\*\*(T\d\d) - (.*)\*\*', lines[0]).groups()
    f, steps, cur = {}, [], None
    for l in lines[1:]:
        m = re.match(r'(Importance|Checks|Done via|Can I run it now|Before you start|Steps|Expected):\s*(.*)', l)
        if m: cur = m.group(1); f[cur] = m.group(2)
        elif cur == 'Steps' and re.match(r'\d+\.', l): steps.append(re.sub(r'^\d+\.\s*', '', l))
    tests.append(dict(id=tid, title=tt, set=sname, f=f, steps=steps,
                      rules=re.findall(r'R\d+[a-z]?', f['Checks']), run=f['Can I run it now'].startswith('Yes')))
sets = []
for t in tests:
    if t['set'] not in sets: sets.append(t['set'])
def card(t):
    f = t['f']; imp = f['Importance']; hi = imp.startswith('High')
    row = lambda c, l, x: f'<div class="row {c}"><span class="lab">{l}</span><span>{e(x)}</span></div>'
    st = ''.join('<li>' + (('<b>' + e(s.split(': ', 1)[0]) + '</b><br><span class="how">' + e(s.split(': ', 1)[1]) + '</span>') if ': ' in s else e(s)) + '</li>' for s in t['steps'])
    why = ('<div class="why">' + e(imp.split(' - ', 1)[1]) + '</div>') if hi and ' - ' in imp else ''
    cant = '' if t['run'] else '<div class="why">' + e(f['Can I run it now']) + '</div>'
    return (f'<section class="card" data-set="{e(t["set"])}"><header><span class="id">{t["id"]}</span><h2>{e(t["title"])}</h2>'
            f'<span class="pill {"hi" if hi else "lo"}">{e(imp.split(" - ")[0])}</span>'
            f'<span class="pill {"ok" if t["run"] else "no"}">{"Can run now" if t["run"] else "Cannot run yet"}</span></header>'
            + row('chk', 'What it checks', f['Checks']) + row('pre', 'Before you start', f['Before you start'])
            + f'<div class="row stp"><span class="lab">Steps</span><ol>{st}</ol></div>' + row('exp', 'Expected', f['Expected']) + why + cant + '</section>')
def cov(ts):
    ids = sorted({r for t in ts for r in t['rules']})
    ok = sorted({r for t in ts if t['run'] for r in t['rules']})
    blocked = [r for r in ids if r not in ok]
    return len(ts), sum(t['run'] for t in ts), ok, blocked
def bar(ok, tot):
    pct = int(100 * ok / tot) if tot else 0
    return f'<div class="meter"><i style="width:{pct}%"></i></div>'
allrules = spec_ids or sorted({r for t in tests for r in t['rules']})
n, nrun, ok, blocked = cov(tests)
none = [r for r in allrules if r not in ok and r not in blocked]
rows = ''
for s in sets:
    ts = [t for t in tests if t['set'] == s]
    a, b, o, bl = cov(ts)
    rows += f'<tr><td>{e(s)}</td><td>{b} of {a}</td><td>{len(o)}</td><td>{len(bl)}</td></tr>'
covhtml = (f'<section class="card" data-set="__cov"><h2>Coverage</h2>'
           f'<p><b>{len(ok)} of {len(allrules)}</b> rules have a test that can run now.</p>{bar(len(ok), len(allrules))}'
           f'<p>{len(blocked)} rules only have tests that cannot run yet: {e(", ".join(blocked)) or "none"}.<br>{len(none)} without any test: {e(", ".join(none)) or "none"}.</p>'
           f'<p>{nrun} of {n} tests can run now.</p>{bar(nrun, n)}'
           f'<table><tr><th>Set</th><th>Tests that can run</th><th>Rules covered</th><th>Rules blocked</th></tr>{rows}</table>'
           f'<p class="how">Covered = a test cites the rule and can be run. No test has been run yet.</p></section>')
tabs = '<button data-t="__ov" class="on">Overview</button><button data-t="__all">All tests</button>' + ''.join(
    f'<button data-t="{e(s)}">{e(s)} <small>{cov([t for t in tests if t["set"] == s])[1]}/{len([t for t in tests if t["set"] == s])}</small></button>' for s in sets) + '<button data-t="__cov">Coverage</button>'
how = ''.join('<li>' + re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', e(l[2:])) + '</li>' for l in intro.split('\n') if l.startswith('- '))
ovrows=''.join(f'<tr><td>{t["id"]}</td><td>{e(t["title"])}</td><td>{e(t["set"])}</td><td>{e(t["f"]["Importance"].split(" - ")[0])}</td><td>{"Yes" if t["run"] else "No"}</td></tr>' for t in tests)
ovhtml=f'<section class="card" data-set="__ov"><h2>Overview</h2><table><tr><th>ID</th><th>Test</th><th>Set</th><th>Importance</th><th>Can run</th></tr>{ovrows}</table></section>'
doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{e(title)}</title><style>
body{{font:15px/1.5 system-ui,sans-serif;max-width:780px;margin:0 auto;padding:0 16px 40px;color:#1c2330;background:#f5f6f8}}
nav{{position:sticky;top:0;background:#f5f6f8;padding:10px 0;display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid #dde1e8;z-index:2}}
nav button{{border:1px solid #cfd4dd;background:#fff;border-radius:99px;padding:5px 12px;font:inherit;font-size:13px;cursor:pointer}}
nav button.on{{background:#6b4fd0;color:#fff;border-color:#6b4fd0}} nav small{{opacity:.7}}
h1{{font-size:22px}} .card{{background:#fff;border:1px solid #dde1e8;border-radius:10px;padding:14px 16px;margin:14px 0}}
header{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px}} h2{{font-size:16px;margin:0;flex:1 1 300px}}
.id{{font-weight:700;color:#5b6577}} .pill{{font-size:12px;padding:2px 9px;border-radius:99px;font-weight:600}}
.hi{{background:#fde2e2;color:#a11}} .lo{{background:#eef0f4;color:#556}} .ok{{background:#dff3e4;color:#17692f}} .no{{background:#fff0d1;color:#8a5a00}}
.row{{display:flex;gap:10px;padding:7px 10px;margin:5px 0;border-radius:6px;border-left:4px solid}} .lab{{flex:0 0 120px;font-weight:700;font-size:13px}}
.chk{{background:#eef4ff;border-color:#3b6fd4}} .pre{{background:#fff7e6;border-color:#d9971a}} .stp{{background:#f3f0ff;border-color:#6b4fd0}} .exp{{background:#e9f7ee;border-color:#2c9a54}}
ol{{margin:0;padding-left:18px}} .how{{color:#667;font-size:13px}} .why{{font-size:13px;color:#8a5a00;margin-top:6px}}
.meter{{background:#e6e8ee;border-radius:99px;height:10px;margin:4px 0 10px}} .meter i{{display:block;height:100%;background:#2c9a54;border-radius:99px}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{border-bottom:1px solid #e3e3e8;padding:6px 8px;text-align:left}}
</style></head><body><h1>{e(title)}</h1><p class="how">{e(intro.split(chr(10))[0])}</p>
<div class="card"><b>How to read this</b><ul>{how}</ul></div>
<nav>{tabs}</nav>
{ovhtml}{covhtml}{''.join(card(t) for t in tests)}
<script>
var bs=document.querySelectorAll('nav button'),cs=document.querySelectorAll('.card[data-set]');
function show(t){{bs.forEach(function(b){{b.classList.toggle('on',b.dataset.t===t)}});cs.forEach(function(c){{var s=c.dataset.set;c.style.display=(t==='__all'?(s!=='__cov'&&s!=='__ov'):s===t)?'':'none'}});window.scrollTo(0,0)}}
bs.forEach(function(b){{b.onclick=function(){{show(b.dataset.t)}}}});show('__ov');
</script></body></html>'''
open(sys.argv[2], 'w').write(doc)
print(len(tests), 'tests,', len(sets), 'sets')

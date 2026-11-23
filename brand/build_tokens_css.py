#!/usr/bin/env python3
"""Regenerate brand/tokens.css from brand/tokens.json. Run: python3 brand/build_tokens_css.py"""
import json, pathlib

here = pathlib.Path(__file__).parent
t = json.loads((here / 'tokens.json').read_text())
theme = t['color']['themes'][0]['id']

def val(v):
    return v if isinstance(v, str) else v[theme]

lines = [f"/* {t['name']} — generated from tokens.json by build_tokens_css.py. Do not edit by hand. */", ':root {', '  color-scheme: dark;']
for fam in ('color', 'shadow', 'spacing', 'radius', 'layout'):
    lines.append(f'  /* {fam} */')
    lines += [f"  --{x['name']}: {val(x['value'])};" for x in t[fam]['tokens']]
lines.append('  /* type */')
lines += [f'  --font-{k}: {v};' for k, v in t['type']['families'].items()]
lines.append('}')
(here / 'tokens.css').write_text('\n'.join(lines) + '\n')

n = sum(len(t[f]['tokens']) for f in ('color', 'shadow', 'spacing', 'radius', 'layout'))
assert (here / 'tokens.css').read_text().count('\n  --') == n + len(t['type']['families'])
print(f'wrote tokens.css ({n} tokens)')

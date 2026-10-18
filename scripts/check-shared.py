#!/usr/bin/env python3
"""Drift guard: the nav, footer, enquiry widget (markup + JS) and their CSS are duplicated
across the static pages. Fail if the copies diverge.

Usage: python3 scripts/check-shared.py   (exit 1 on drift; run from the repo root)
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'about.html', 'pricing.html']


def between(text, start, end, include_end=False):
    i = text.index(start)
    j = text.index(end, i) + (len(end) if include_end else 0)
    return text[i:j]


def norm_links(h):
    """Sub-pages link back to index.html#...; make hrefs comparable with index.html."""
    h = h.replace('href="index.html#', 'href="#').replace('href="pricing.html"', 'href="#pricing"')
    h = re.sub(r'\s+aria-current="page"', '', h)
    h = re.sub(r'\s*<li class="nav-mobile-cta">.*?</li>', '', h, flags=re.S)   # index-only mobile CTA
    return h


def css_block(text, marker):
    style = between(text, '<style>', '</style>')
    parts = re.split(r'(?m)^(?=    /\* ── )', style)
    hit = [p for p in parts if p.startswith('    /* ── ' + marker)]
    return hit[0].strip() if hit else None


def pieces(path):
    t = (ROOT / path).read_text()
    out = {}
    out['nav markup'] = norm_links(between(t, '<header class="site-nav"', '</header>', True))
    out['footer markup'] = norm_links(between(t, '<footer>', '</footer>', True))
    out['widget markup'] = between(t, '<!-- ── ENQUIRY WIDGET', '<script>')
    out['widget js'] = between(t, '    // ── Enquiry widget ──', '  })();\n</script>')
    for name in ('NAV', 'FOOTER', 'ENQUIRY WIDGET', 'Decorative butterflies'):
        out['css ' + name] = css_block(t, name)
    return out


base = pieces(PAGES[0])
bad = 0
for page in PAGES[1:]:
    other = pieces(page)
    for key, val in base.items():
        if other[key] != val:
            bad += 1
            print(f'DRIFT: {page} differs from {PAGES[0]} in "{key}"')
print('shared blocks identical across', ', '.join(PAGES) if not bad else f'-- {bad} difference(s) found')
sys.exit(1 if bad else 0)

import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import outline as o
from build import svg, save, poly, rdiamond, subline, f, INK, AMBER
OUT = sys.argv[1]

# ---------- D: Ш as a podium / bar chart, winner's diamond on top ----------
def podium_sh(ox, base_y, sc, heights=(600, 750, 470)):
    """Custom Ш in font units (Unbounded 800 metrics): stems of podium heights, ink traps kept."""
    L, M, R = heights
    pts = [(1173.6, 205.8), (1068.8, 101), (1068.8, R), (1301.6, R), (1301.6, 0), (64.8, 0), (64.8, L),
           (297.6, L), (297.6, 101), (192.8, 205.8), (667, 205.8), (566.8, 101), (566.8, M), (799.6, M),
           (799.6, 101), (698.2, 205.8)]
    return poly([(ox + x * sc, base_y - y * sc) for x, y in pts])

def podium_diamond(ox, base_y, sc, top=750):
    R = 150
    return rdiamond(ox + 683.2 * sc, base_y - (top + 80 + R) * sc, R * sc, 18 * sc)

def concept_d(color):
    ink, amb = (INK, AMBER) if color else ('#000', '#000')
    S = 200; sc = S / 1000; cap = 150
    d, w, b = o.text('РЕШЕНО', size=S, skip=(2,))
    shx = b[2][0] - 64.8 * sc
    pad = 24; above = (80 + 300) * sc
    top = pad + above
    T = f'translate({f(pad - b[0][0])} {f(top + cap)})'
    body = (f'  <g id="wordmark" transform="{T}">\n    <path fill="{ink}" d="{d} {podium_sh(shx, 0, sc)}"/>\n'
            f'    <path fill="{amb}" d="{podium_diamond(shx, 0, sc)}"/>\n  </g>\n')
    W = b[-1][2] - b[0][0] + 2 * pad
    word = svg(W, top + cap + pad, body, 'РЕШЕНО wordmark')
    sp, hc = subline(b[-1][2] - b[0][0], pad, top + cap + 0.22 * cap, 0, ink)
    lock = svg(W, top + cap + 0.22 * cap + hc + pad, body + sp, 'РЕШЕНО Business Live logo')
    # symbol: the podium Ш alone, centred on 256
    k = 0.15; gw = (1301.6 - 64.8) * k; gh = (750 + 80 + 300) * k
    ox = 128 - gw / 2 - 64.8 * k; by = 128 + gh / 2
    sym = svg(256, 256, f'  <path fill="{ink}" d="{podium_sh(ox, by, k)}"/>\n  <path fill="{amb}" d="{podium_diamond(ox, by, k)}"/>\n',
              'РЕШЕНО symbol')
    return word, lock, sym

# ---------- E: tic-tac-toe grid, three diamonds = three businesses, three solutions ----------
def symbol_e(color):
    ink, amb = (INK, AMBER) if color else ('#000', '#000')
    c, g = 64, 18; o0 = (256 - (3 * c + 2 * g)) / 2
    a1, a2 = o0 + c, o0 + 2 * c + g
    e0, e1 = o0, 256 - o0
    bars = ' '.join(poly([(x, e0), (x + g, e0), (x + g, e1), (x, e1)]) + ' ' + poly([(e0, x), (e1, x), (e1, x + g), (e0, x + g)])
                    for x in (a1, a2))
    centres = [o0 + c / 2 + i * (c + g) for i in range(3)]
    dias = ' '.join(rdiamond(centres[i], centres[2 - i], 30, 4) for i in range(3))
    return f'  <path fill="{ink}" d="{bars}"/>\n  <path fill="{amb}" d="{dias}"/>\n'

# ---------- F: a knot that resolves into a straight line ending in the diamond ----------
def symbol_f(color):
    ink, amb = (INK, AMBER) if color else ('#000', '#000')
    w = 26
    line = ('M 18 172 C 76 172 124 146 124 104 C 124 74 102 56 78 56 C 54 56 36 74 36 98 '
            'C 36 146 90 172 150 172 L 184 172')
    return (f'  <path fill="none" stroke="{ink}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" d="{line}"/>\n'
            f'  <path fill="{amb}" d="{rdiamond(214, 172, 28, 4)}"/>\n')

def lockup(symbody, color, title):
    ink = INK if color else '#000'
    S = 112; cap = o.cap_height(size=S)
    d, w, b = o.text('РЕШЕНО', size=S)
    x0 = 256 + 56 - b[0][0]
    from build import sub_cap
    gap = 0.22 * cap; scap = sub_cap(b[-1][2] - b[0][0])
    base = 128 - (cap + gap + scap) / 2 + cap
    body = symbody + f'  <path fill="{ink}" d="{o.text("РЕШЕНО", size=S, x=x0, y=base)[0]}"/>\n'
    body += subline(b[-1][2] - b[0][0], x0 + b[0][0], base + gap, 0, ink)[0]
    return svg(x0 + b[-1][2] + 8, 256, body, title)

for color, suf in ((False, ''), (True, '-color')):
    wd, ld, sd = concept_d(color)
    save(f'd-wordmark{suf}.svg', wd); save(f'd-lockup{suf}.svg', ld); save(f'd-symbol{suf}.svg', sd)
    save(f'e-symbol{suf}.svg', svg(256, 256, symbol_e(color), 'РЕШЕНО symbol'))
    save(f'e-lockup{suf}.svg', lockup(symbol_e(color), color, 'РЕШЕНО Business Live logo'))
    save(f'f-symbol{suf}.svg', svg(256, 256, symbol_f(color), 'РЕШЕНО symbol'))
    save(f'f-lockup{suf}.svg', lockup(symbol_f(color), color, 'РЕШЕНО Business Live logo'))
print('ok')

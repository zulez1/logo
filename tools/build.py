import sys, math, os
sys.path.insert(0, os.path.dirname(__file__))
import outline as o

OUT = sys.argv[1]
INK, AMBER = '#0D0F13', '#F0B90B'
f = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {f(h)}" width="{f(w)}" height="{f(h)}" '
            f'role="img" aria-labelledby="title">\n  <title id="title">{title}</title>\n{body}</svg>\n')

def save(name, s):
    open(os.path.join(OUT, name), 'w').write(s)

def poly(pts):
    return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ' Z'

def rdiamond(cx, cy, R, r):
    """Diamond (square rotated 45°) with half-diagonal R and corner radius r."""
    vs = [(cx, cy - R), (cx + R, cy), (cx, cy + R), (cx - R, cy)]
    t = r  # tangent length for 90° corner
    d = ''
    for i, (x, y) in enumerate(vs):
        px, py = vs[i - 1]; nx, ny = vs[(i + 1) % 4]
        L = math.hypot(x - px, y - py)
        a = (x + (px - x) * t / L, y + (py - y) * t / L)
        b = (x + (nx - x) * t / L, y + (ny - y) * t / L)
        d += ('M' if i == 0 else 'L') + f'{f(a[0])} {f(a[1])} A{f(r)} {f(r)} 0 0 1 {f(b[0])} {f(b[1])} '
    return d + 'Z'

def check(P1, P2, P3, w):
    h = w / 2; s = h / math.sqrt(2)
    u1 = (s, -s); u2 = (-s, -s)
    return poly([(P1[0] + u1[0], P1[1] + u1[1]), (P2[0], P2[1] - h * math.sqrt(2)), (P3[0] + u2[0], P3[1] + u2[1]),
                 (P3[0] - u2[0], P3[1] - u2[1]), (P2[0], P2[1] + h * math.sqrt(2)), (P1[0] - u1[0], P1[1] - u1[1])])

def subline(width, x, top, size, color, tr=0.34):
    """'BUSINESS LIVE' with fixed tracking, scaled to span width (size arg ignored)."""
    _, w0, b = o.text('BUSINESS LIVE', 'Montserrat', 700, 100, 0, 0, tr)
    ink = b[-1][2] - b[0][0]
    sz = 100 * width / ink
    d, _, b = o.text('BUSINESS LIVE', 'Montserrat', 700, sz, 0, 0, tr)
    capm = o.cap_height('Montserrat', 700, sz)
    d, _, _ = o.text('BUSINESS LIVE', 'Montserrat', 700, sz, x - b[0][0], top + capm, tr)
    return f'  <path fill="{color}" d="{d}"/>\n', capm

def sub_cap(width, tr=0.34):
    _, _, b = o.text('BUSINESS LIVE', 'Montserrat', 700, 100, 0, 0, tr)
    return o.cap_height('Montserrat', 700, 100 * width / (b[-1][2] - b[0][0]))

# ---------- A: wordmark, final О becomes the amber diamond ----------
def concept_a(color):
    S = 200; cap = o.cap_height(size=S)
    d, w, boxes = o.text('РЕШЕНО', size=S, x=0, y=0)
    stem = 0.2 * S * 0.9          # approx Unbounded 800 stem
    R = stem * 1.1               # diamond half-diagonal: a heavy full stop
    cx = boxes[-1][2] + 14 + R
    dia = rdiamond(cx, -R + 2, R, 4)   # sits on the baseline (slight overshoot)
    pad = 24; x0 = boxes[0][0]
    right = cx + R
    W = right - x0 + 2 * pad
    ink, amb = (INK, AMBER) if color else ('#000', '#000')
    body = f'  <g id="wordmark" transform="translate({f(pad - x0)} {f(pad + cap)})">\n'
    body += f'    <path fill="{ink}" d="{d}"/>\n    <path fill="{amb}" d="{dia}"/>\n  </g>\n'
    word_only = svg(W, cap + 2 * pad + 4, body, 'РЕШЕНО wordmark')
    top2 = pad + cap + 0.22 * cap
    sp, hc = subline(boxes[-1][2] - x0, pad, top2, 0, ink)
    return word_only, svg(W, top2 + hc + pad, body + sp, 'РЕШЕНО Business Live logo')

# ---------- B: diamond with negative-space check ----------
def symbol_b(color, ox=0, oy=0, k=1.0):
    cx, cy = 128, 128
    dia = rdiamond(cx, cy, 120, 22)
    chk = check((82, 130), (114, 162), (176, 100), 30)
    T = f' transform="translate({f(ox)} {f(oy)}) scale({f(k)})"' if (ox or oy or k != 1) else ''
    return f'  <path id="symbol"{T} fill="{AMBER if color else "#000"}" fill-rule="evenodd" d="{dia} {chk}"/>\n'

# ---------- C: Р with a play-triangle counter ----------
def symbol_c(color, ox=0, oy=0, k=1.0):
    outer = poly([(52, 20), (128, 20), (204, 96), (128, 172), (100, 172), (100, 236), (52, 236)])
    counter = poly([(100, 60), (100, 132), (136, 96)])
    T = f' transform="translate({f(ox)} {f(oy)}) scale({f(k)})"' if (ox or oy or k != 1) else ''
    s = f'  <g id="symbol"{T}>\n    <path fill="{INK if color else "#000"}" fill-rule="evenodd" d="{outer} {counter}"/>\n'
    if color:
        s += f'    <path fill="{AMBER}" d="{counter}"/>\n'
    return s + '  </g>\n'

def lockup(symfn, color, title):
    # symbol 256 tall, text block to the right
    S = 112; cap = o.cap_height(size=S)
    d, w, boxes = o.text('РЕШЕНО', size=S)
    x0 = 256 + 56 - boxes[0][0]
    gap = 0.22 * cap; sc = sub_cap(boxes[-1][2] - boxes[0][0])
    block = cap + gap + sc
    base = 128 - block / 2 + cap
    body = symfn(color)
    body += f'  <path id="wordmark" fill="{INK if color else "#000"}" d="{o.text("РЕШЕНО", size=S, x=x0, y=base)[0]}"/>\n'
    body += subline(boxes[-1][2] - boxes[0][0], x0 + boxes[0][0], base + gap, 0, INK if color else '#000')[0]
    W = x0 + boxes[-1][2] + 8
    return svg(W, 256, body, title)

for color, suf in ((False, ''), (True, '-color')):
    wa, la = concept_a(color)
    save(f'a-wordmark{suf}.svg', wa); save(f'a-lockup{suf}.svg', la)
    save(f'b-symbol{suf}.svg', svg(256, 256, symbol_b(color), 'РЕШЕНО symbol'))
    save(f'b-lockup{suf}.svg', lockup(symbol_b, color, 'РЕШЕНО Business Live logo'))
    save(f'c-symbol{suf}.svg', svg(256, 256, symbol_c(color), 'РЕШЕНО symbol'))
    save(f'c-lockup{suf}.svg', lockup(symbol_c, color, 'РЕШЕНО Business Live logo'))
print('ok')

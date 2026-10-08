"""Outline text to SVG path data using a variable font at a chosen weight."""
import functools
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTS = '/tmp/claude-0/-home-user-logo/8f584cd3-6d50-55cc-9a77-77d1bee1a941/scratchpad/fonts/'

@functools.lru_cache(None)
def font(name, wght):
    f = TTFont(FONTS + name + '.ttf')
    return instantiateVariableFont(f, {'wght': wght})

def text(s, name='Unbounded', wght=800, size=100, x=0, y=0, track=0.0, skip=()):
    """Return (path_d, width, glyph_boxes). y is baseline. track in em. skip: indices to leave out (still advance)."""
    f = font(name, wght)
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    sc = size / upm
    pen = SVGPathPen(gs, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.'))
    cx = x; boxes = []
    for i, ch in enumerate(s):
        g = cmap[ord(ch)]
        adv = f['hmtx'][g][0] * sc
        bp = BoundsPen(gs); gs[g].draw(bp)
        b = bp.bounds
        boxes.append((cx + b[0]*sc, y - b[3]*sc, cx + b[2]*sc, y - b[1]*sc) if b else None)
        if i not in skip:
            gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        cx += adv + (track * size if i < len(s)-1 else 0)
    return pen.getCommands(), cx - x, boxes

def cap_height(name='Unbounded', wght=800, size=100):
    f = font(name, wght)
    return f['OS/2'].sCapHeight * size / f['head'].unitsPerEm

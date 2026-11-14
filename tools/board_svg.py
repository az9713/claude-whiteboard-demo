"""Render a static map of the whiteboard (from its element layout) as SVG."""
import html, sys

FILL = {"blue": "#e4edf8", "green": "#e3f1e6", "yellow": "#fbf1d2", "white": "#f3f1ec"}
ACC = "#c4552d"

sections = [
    (0, 240, 520, 480, "1 · The claim"), (560, 240, 520, 480, "2 · The shift"),
    (1120, 240, 520, 480, "3 · What is NOT solved"), (0, 800, 1640, 340, "4 · The method: loop until good"),
    (0, 1220, 800, 810, "4a · Build the harness, explained"), (840, 1220, 800, 810, "4b · The #1 skill, explained"),
    (0, 2110, 1080, 424, "5 · Proof it already works"), (1120, 2110, 520, 424, "6 · Ben's bets"),
    (0, 2614, 1640, 800, "7 · Behavior changes: stop → start → try this"),
]
# x, y, w, h, colour, label, outlined
blocks = [
    (24, 264, 472, 76, "blue", "Agents out-code humans on A→B tasks", 0),
    (24, 364, 472, 76, "blue", "Hand-coding? \"Flat wrong.\"", 0),
    (584, 264, 472, 88, "blue", "Start of 2026: one thread", 0),
    (584, 416, 472, 88, "blue", "Now: ~20 agents, 5 machines", 0),
    (584, 528, 472, 76, "blue", "The barrier is psychological", 0),
    (584, 628, 472, 68, "blue", "CRUD only → bleak", 0),
    (1144, 264, 472, 88, "white", "Non-verifiable decisions", 0),
    (1144, 376, 472, 88, "white", "Product judgment", 0),
    (1144, 488, 472, 76, "white", "Taste + direction", 0),
    (1144, 588, 472, 88, "white", "Hands-off = bad time", 0),
    (32, 840, 264, 140, "green", "1. Pick an ocean", 0),
    (360, 840, 264, 140, "green", "2. Build the harness", 1),
    (688, 840, 264, 140, "green", "3. Loop the builder", 0),
    (1016, 840, 264, 140, "green", "4. Cross-model review", 0),
    (1344, 840, 264, 140, "green", "5. Phone check", 0),
    (24, 1394, 200, 180, "white", "The spec", 0),
    (300, 1394, 200, 180, "yellow", "The fake API", 0),
    (576, 1394, 200, 180, "white", "The real app", 0),
    (24, 1760, 170, 170, "yellow", "Stripe test", 0), (218, 1760, 170, 170, "yellow", "Flight sim", 0),
    (412, 1760, 170, 170, "yellow", "Crash dummy", 0), (606, 1760, 170, 170, "yellow", "Staging", 0),
    (864, 1394, 208, 180, "green", "1. Notice", 0), (1136, 1394, 208, 180, "green", "2. Reject", 0),
    (1408, 1394, 208, 180, "green", "3. Engineer it out", 1),
    (864, 1694, 364, 120, "white", "Weak correction", 0), (1252, 1694, 364, 120, "white", "Strong correction", 1),
    (24, 2134, 328, 128, "yellow", "TS Go → Rust", 0), (376, 2134, 328, 128, "yellow", "T3 Code", 0),
    (728, 2134, 328, 128, "yellow", "Cat-patrol robot", 0), (24, 2286, 328, 128, "yellow", "3D-printer bot", 0),
    (376, 2286, 328, 128, "yellow", "Dictation app", 0), (728, 2286, 328, 128, "yellow", "FPS game", 0),
    (1144, 2134, 472, 76, "white", "Google products displaced", 0),
    (1144, 2234, 472, 76, "white", "Tiny team, better mobile OS", 0),
    (1144, 2334, 472, 76, "white", "Solo dev beats AAA studio", 0),
    (1144, 2434, 472, 76, "white", "Horizon: ~1 year", 0),
]
lines = [  # free text as grey bars (x, y, width)
    (24, 1250, 700), (24, 1290, 520), (24, 1606, 740), (24, 1634, 600), (24, 1700, 560), (24, 1962, 700),
    (864, 1250, 720), (864, 1290, 420), (864, 1606, 740), (864, 1634, 640), (864, 1846, 680), (32, 1084, 900),
]
arrows = [((584 + 236, 352), (584 + 236, 416))]
arrows += [((296 + i * 328, 910), (360 + i * 328, 910)) for i in range(4)]
arrows += [((224, 1484), (300, 1484)), ((500, 1484), (576, 1484))]
arrows += [((1072, 1484), (1136, 1484)), ((1344, 1484), (1408, 1484))]

W, H = 1700, 3640
o = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='-30 -30 {W} {H}' font-family='-apple-system,Segoe UI,Helvetica,Arial,sans-serif' role='img' aria-label='Map of the whiteboard used to build this summary'>",
     "<defs><marker id='ah' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='#555'/></marker>",
     f"<marker id='ahr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='{ACC}'/></marker></defs>",
     f"<rect x='-30' y='-30' width='{W}' height='{H}' fill='#fbfaf7'/>",
     "<text x='0' y='52' font-size='52' font-weight='700' fill='#1d1d1b'>Software is solved. Now be more ambitious.</text>",
     "<text x='0' y='112' font-size='28' fill='#6b6a65'>Writing code is solved. Ambition, taste, verification are not.</text>"]
for x, y, w, h, t in sections:
    o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='14' fill='none' stroke='#d6d2c8' stroke-width='2'/>")
    o.append(f"<text x='{x + 4}' y='{y - 12}' font-size='24' font-weight='700' fill='#3a3a36'>{html.escape(t)}</text>")
for x, y, w, h, c, label, key in blocks:
    st = f"stroke='{ACC}' stroke-width='4'" if key else "stroke='none'"
    o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='12' fill='{FILL[c]}' {st}/>")
    fs = 22 if w > 180 else 19
    o.append(f"<text x='{x + w / 2}' y='{y + h / 2 + fs * 0.35}' text-anchor='middle' font-size='{fs}' font-weight='600' fill='#2b2b28'>{html.escape(label)}</text>")
for x, y, w in lines:
    o.append(f"<rect x='{x}' y='{y}' width='{w}' height='12' rx='6' fill='#e2ded5'/>")
# capability chart
o.append("<polyline points='48,490 48,660 488,660' fill='none' stroke='#555' stroke-width='3'/>")
o.append(f"<polyline points='48,650 348,600 388,575 428,545 468,510 488,490' fill='none' stroke='{ACC}' stroke-width='6' stroke-linejoin='round'/>")
for (x1, y1), (x2, y2) in arrows:
    o.append(f"<line x1='{x1}' y1='{y1}' x2='{x2 - 2}' y2='{y2}' stroke='#555' stroke-width='3' marker-end='url(%23ah)'/>".replace("%23", "#"))
# return loop arrow
o.append(f"<polyline points='1476,980 1476,1030 164,1030 164,984' fill='none' stroke='{ACC}' stroke-width='4' stroke-dasharray='12 8' marker-end='url(#ahr)'/>")
o.append(f"<text x='820' y='1060' text-anchor='middle' font-size='20' fill='{ACC}' font-weight='600'>Broke? Stop, name it, engineer it out</text>")
# table
tx, ty, cw = 24, 2638, [300, 480, 812]
rows, rh = 12, 60
o.append(f"<rect x='{tx}' y='{ty}' width='{sum(cw)}' height='{rows * rh}' rx='10' fill='#ffffff' stroke='#d6d2c8' stroke-width='2'/>")
o.append(f"<rect x='{tx}' y='{ty}' width='{sum(cw)}' height='{rh}' rx='10' fill='#efede8'/>")
for i in range(1, rows):
    o.append(f"<line x1='{tx}' y1='{ty + i * rh}' x2='{tx + sum(cw)}' y2='{ty + i * rh}' stroke='#e3dfd6' stroke-width='2'/>")
cx = tx
for j, wd in enumerate(cw):
    if j:
        o.append(f"<line x1='{cx}' y1='{ty}' x2='{cx}' y2='{ty + rows * rh}' stroke='#e3dfd6' stroke-width='2'/>")
    o.append(f"<text x='{cx + 18}' y='{ty + 38}' font-size='22' font-weight='700' fill='#3a3a36'>{['Stop', 'Start: what it means', 'Try this'][j]}</text>")
    for i in range(1, rows):
        o.append(f"<rect x='{cx + 18}' y='{ty + i * rh + 24}' width='{wd * (0.55 + 0.3 * ((i * 7 + j * 3) % 5) / 4):.0f}' height='12' rx='6' fill='#e2ded5'/>")
    cx += wd
o.append(f"<rect x='320' y='3480' width='1000' height='96' rx='48' fill='#f3f1ec' stroke='{ACC}' stroke-width='4'/>")
o.append("<text x='820' y='3538' text-anchor='middle' font-size='30' font-weight='600' fill='#1d1d1b'>Effort + caring: the edge, for now. Go bigger.</text>")
o.append("</svg>")
open(sys.argv[1], "w").write("\n".join(o))

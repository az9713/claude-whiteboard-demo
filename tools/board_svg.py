"""Render a static map of the whiteboard (from its element layout) as SVG."""
import html, sys

FILL = {"blue": "#e4edf8", "green": "#e3f1e6", "yellow": "#fbf1d2", "white": "#f3f1ec"}
ACC = "#c4552d"

sections = [
    (0, 240, 520, 480, "1 · The claim"), (560, 240, 520, 480, "2 · The shift"),
    (1120, 240, 520, 480, "3 · What is NOT solved"), (0, 800, 1640, 340, "4 · The method: loop until good"),
    (0, 1220, 800, 810, "4a · Build the harness, explained"), (840, 1220, 800, 810, "4b · The #1 skill, explained"),
    (0, 2110, 1080, 424, "5 · Proof it already works"), (1120, 2110, 520, 424, "6 · Ben's bets"),
    (0, 2614, 1640, None, "7 · Behavior changes: stop → start → try this"),
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
texts = [  # (x, y, wrap width, font size, bold, text)
    (32, 1076, 1560, 18, 0, "#1 skill in 2026: spot bad agent output, say \"no, not like this\", then engineer the cause out (see 4b)."),
    (24, 1244, 752, 23, 0, "A harness is a safe practice copy of the real thing. The agent can test its own work against it, thousands of times, with no human watching."),
    (24, 1598, 752, 17, 0, "Why not just use the real YouTube? Real APIs have quotas, keys and rate limits, change under you, and can't be reset. A fake is free, instant, and always in the same known state, so the agent can loop for hours alone."),
    (24, 1694, 752, 21, 1, "Things you already know that work the same way"),
    (24, 1954, 752, 17, 0, "The FPS game is the same idea: a CLI plus screenshots lets the agent 'see' and play its own game, so it can tell whether a change worked."),
    (864, 1244, 752, 23, 0, "Judge what the agent made, reject what's wrong, then fix the cause so it never comes back."),
    (864, 1598, 752, 17, 0, "Why it's #1: agents now write the code, but they still can't tell good from good-enough. The person who keeps saying no, and turns each no into a permanent guardrail, gets quality that compounds."),
    (864, 1838, 752, 15, 0, "Source: Mario (creator of the Pi coding agent), quoted by Ben. It is the dashed loop arrow in section 4."),
]

def wrap(text, width, fs):
    n = max(8, int(width / (fs * 0.52)))
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out

table = [
    ("Hand-coding; reading every line", "Agents write the code. Your job is checking the change stays inside what you asked for.", "Ask for one feature, then read only the list of changed files. Anything outside the ask? Reject it."),
    ("Asking for what feels safe", "Pick the project you shelved as too big. Agents make it feasible now.", "List the three projects you've postponed for years. Start the biggest as a weekend spike."),
    ("Babysitting one thread in the IDE", "Hand off whole tasks; let several agents run in the background at once.", "Queue three independent tasks before dinner (a bug fix, a test suite, a doc). Review all three in the morning."),
    ("Letting agents test by clicking around", "Give agents a fast, scriptable way to check their own work.", "Before building on an outside API, have an agent build a fake of it from the docs. Add a CLI command that prints the app's state."),
    ("Letting one model grade its own work", "A different model reviews; the loop continues until it approves.", "Builder: a GPT model. Reviewer: Fable 5.2 with your checklist. Nothing merges until the reviewer says pass."),
    ("Patching a bad output and moving on", "Every failure becomes a permanent guardrail.", "Agent broke login twice? Add a login test that runs on every change, plus one line in the agent's instructions file."),
    ("Putting up with tools you hate", "If a tool annoys you daily, have agents build your own version.", "Ben did this with his dictation app. Name your three most annoying tools and rebuild one."),
    ("Accepting the model's UI and product calls", "Models still lack taste. You define what good looks like, up front.", "Before any design work, give the agent two or three screenshots you like and one paragraph on the feel you want."),
    ("Judging AI by one-shot demos", "A one-prompt demo is the floor. Quality comes from many rounds of expert correction on one product.", "Plan for 300 prompts, not one. Each round fixes one specific thing: \"spacing too tight,\" \"error message unclear.\""),
    ("Checking work only at your desk", "Make every result reviewable in two minutes, from your phone.", "Have each agent task end with a preview link, before/after screenshots and a short diff summary sent to your phone."),
    ("Betting on long-range forecasts", "Guessing the future is a fool's game; act on what works today.", "Plan on a 12-month horizon. Re-test your assumptions every time a new model ships."),
]
TFS, LH = 17, 23
cw = [300, 480, 812]
row_lines = [[wrap(c, cw[j] - 36, TFS) for j, c in enumerate(r)] for r in table]
row_h = [max(len(l) for l in r) * LH + 26 for r in row_lines]
head_h = 56
table_h = head_h + sum(row_h)
sec7_h = table_h + 48
pill_y = 2614 + sec7_h + 60
arrows = [((584 + 236, 352), (584 + 236, 416))]
arrows += [((296 + i * 328, 910), (360 + i * 328, 910)) for i in range(4)]
arrows += [((224, 1484), (300, 1484)), ((500, 1484), (576, 1484))]
arrows += [((1072, 1484), (1136, 1484)), ((1344, 1484), (1408, 1484))]

W = 1700
H = pill_y + 96 + 60 + 30
o = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='-30 -30 {W} {H}' font-family='-apple-system,Segoe UI,Helvetica,Arial,sans-serif' role='img' aria-label='Map of the whiteboard used to build this summary'>",
     "<defs><marker id='ah' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='#555'/></marker>",
     f"<marker id='ahr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='{ACC}'/></marker></defs>",
     f"<rect x='-30' y='-30' width='{W}' height='{H}' fill='#fbfaf7'/>",
     "<text x='0' y='52' font-size='52' font-weight='700' fill='#1d1d1b'>Software is solved. Now be more ambitious.</text>",
     "<text x='0' y='112' font-size='28' fill='#6b6a65'>Writing code is solved. Ambition, taste, verification are not.</text>"]
for x, y, w, h, t in sections:
    h = h or sec7_h
    o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='14' fill='none' stroke='#d6d2c8' stroke-width='2'/>")
    o.append(f"<text x='{x + 4}' y='{y - 12}' font-size='24' font-weight='700' fill='#3a3a36'>{html.escape(t)}</text>")
for x, y, w, h, c, label, key in blocks:
    st = f"stroke='{ACC}' stroke-width='4'" if key else "stroke='none'"
    o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='12' fill='{FILL[c]}' {st}/>")
    fs = 22 if w > 180 else 19
    o.append(f"<text x='{x + w / 2}' y='{y + h / 2 + fs * 0.35}' text-anchor='middle' font-size='{fs}' font-weight='600' fill='#2b2b28'>{html.escape(label)}</text>")
for x, y, w, fs, b, t in texts:
    for k, ln in enumerate(wrap(t, w, fs)):
        o.append(f"<text x='{x}' y='{y + fs + k * fs * 1.35:.0f}' font-size='{fs}' font-weight='{700 if b else 400}' fill='#3a3a36'>{html.escape(ln)}</text>")
# capability chart
o.append("<polyline points='48,490 48,660 488,660' fill='none' stroke='#555' stroke-width='3'/>")
o.append(f"<polyline points='48,650 348,600 388,575 428,545 468,510 488,490' fill='none' stroke='{ACC}' stroke-width='6' stroke-linejoin='round'/>")
for (x1, y1), (x2, y2) in arrows:
    o.append(f"<line x1='{x1}' y1='{y1}' x2='{x2 - 2}' y2='{y2}' stroke='#555' stroke-width='3' marker-end='url(%23ah)'/>".replace("%23", "#"))
# return loop arrow
o.append(f"<polyline points='1476,980 1476,1030 164,1030 164,984' fill='none' stroke='{ACC}' stroke-width='4' stroke-dasharray='12 8' marker-end='url(#ahr)'/>")
o.append(f"<text x='820' y='1060' text-anchor='middle' font-size='20' fill='{ACC}' font-weight='600'>Broke? Stop, name it, engineer it out</text>")
# table
tx, ty = 24, 2638
o.append(f"<rect x='{tx}' y='{ty}' width='{sum(cw)}' height='{table_h}' rx='10' fill='#ffffff' stroke='#d6d2c8' stroke-width='2'/>")
o.append(f"<rect x='{tx + 1}' y='{ty + 1}' width='{sum(cw) - 2}' height='{head_h}' rx='10' fill='#efede8'/>")
cx = tx
for j, wd in enumerate(cw):
    if j:
        o.append(f"<line x1='{cx}' y1='{ty}' x2='{cx}' y2='{ty + table_h}' stroke='#e3dfd6' stroke-width='2'/>")
    o.append(f"<text x='{cx + 18}' y='{ty + 36}' font-size='20' font-weight='700' fill='#3a3a36'>{['Stop', 'Start: what it means', 'Try this'][j]}</text>")
    cx += wd
ry = ty + head_h
for r, lines_ in enumerate(row_lines):
    o.append(f"<line x1='{tx}' y1='{ry}' x2='{tx + sum(cw)}' y2='{ry}' stroke='#e3dfd6' stroke-width='2'/>")
    cx = tx
    for j, wd in enumerate(cw):
        col = ['#8a877f', '#1d1d1b', '#2b2b28'][j]
        wt = ['400', '600', '400'][j]
        for k, ln in enumerate(lines_[j]):
            deco = " text-decoration='line-through'" if j == 0 else ""
            o.append(f"<text x='{cx + 18}' y='{ry + 30 + k * LH}' font-size='{TFS}' font-weight='{wt}' fill='{col}'{deco}>{html.escape(ln)}</text>")
        cx += wd
    ry += row_h[r]
o.append(f"<rect x='320' y='{pill_y}' width='1000' height='96' rx='48' fill='#f3f1ec' stroke='{ACC}' stroke-width='4'/>")
o.append(f"<text x='820' y='{pill_y + 58}' text-anchor='middle' font-size='30' font-weight='600' fill='#1d1d1b'>Effort + caring: the edge, for now. Go bigger.</text>")
o.append("</svg>")
open(sys.argv[1], "w").write("\n".join(o))

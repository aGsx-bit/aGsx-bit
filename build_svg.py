"""
Builds light_mode.svg and dark_mode.svg for the GitHub profile card.
Style: neofetch terminal card (inspired by github.com/Andrew6rant).

Usage:  edit INFO below, then run  python build_svg.py
The dynamic stats (Uptime, Repos, Stars, Commits, Followers, LOC) are
filled in by today.py via GitHub Actions and must NOT be hand-edited here.
"""
import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))

# ======================= EDIT YOUR INFO HERE =======================
INFO = {
    'name': 'mahamad',                    # shown as  mahamad@aGsx-bit
    'username': 'aGsx-bit',
    'os': 'Windows 11, Android, Linux',
    'birthday': '2001-11-27',             # YYYY-MM-DD  (used for Uptime)
    'host': 'Custom Rig / Acer Nitro',
    'kernel': 'Software Engineering & Security Research',
    'prog': 'C, C++, C#, Java, Go, PHP, Python, JavaScript',
    'computer': 'SQL, PS, Bash, x86 Assembly, Regex, LaTeX, HTML, CSS',
    'real': 'Kurdish, English, Arabic, Russian',
    'sysnet': 'Cisco Routing & Switching, Network Architecture, Cabling',
    'secaud': 'Network Safety, Vulnerability Assessment, App Recon',
    'elechw': 'Circuitry, Power Distribution, Storage & Hardware Repair',
    'github': 'aGsx-bit',
    'discord': 'mahamad_xoshnaw',
    'telegram': 'Mahamad_122',
    'email': 'mahamad.agsx@gmail.com',
}
# ====================================================================

THEMES = {
    'light': dict(bg='#f6f8fa', text='#24292f', key='#953800', value='#0a3069',
                  cc='#57606a', sep='#57606a', art_bg='#0a0e0f'),
    'dark':  dict(bg='#0a0e0f', text='#e8f4f8', key='#f0883e', value='#79c0ff',
                  cc='#7d8590', sep='#30363d', art_bg='#0a0e0f'),
}

ART_SCALE = 0.5        # their art is 792x1050 at 8px font; scale to ~396x525
ART_X, ART_Y = 15, 25  # position of the art group on the card
INFO_X = 440           # x position of the info panel
LINE_H = 20            # line height of the info panel
LINE_CHARS = 86        # right-alignment column for static values (in chars)
CARD_W, CARD_H = 1300, 590


def load_art():
    """Load the photo grid: rows of [char, [r, g, b]]."""
    with open(os.path.join(HERE, 'art_grid.json'), encoding='utf-8') as f:
        return json.load(f)


def art_svg(grid):
    """Emit the photo as tspans, merging same-color runs per row."""
    parts = []
    for y, row in enumerate(grid):
        x = 0
        while x < len(row):
            ch, col = row[x]
            if ch == ' ' or ch == '\x00':   # background cells are skipped
                x += 1
                continue
            run, j = [ch], x + 1
            while j < len(row) and row[j][0] != ' ' and row[j][1] == col:
                run.append(row[j][0])
                j += 1
            color = f"rgb({col[0]},{col[1]},{col[2]})"
            parts.append(
                f'<tspan x="{20 + x * 8}" y="{20 + y * 10}" fill="{color}">'
                f'{escape("".join(run))}</tspan>')
            x = j
            
    return ('<g transform="translate({0},{1}) scale({2})" opacity="0.55">\n'
            '<rect x="0" y="0" width="792" height="1050" fill="{3}" rx="16"/>\n'
            '<text font-family="\'JetBrains Mono\',Consolas,monospace" font-size="8px">{4}</text>\n</g>').format(
                ART_X, ART_Y, ART_SCALE, '#0a0e0f', '\n'.join(parts))


def line(y, parts, theme):
    """One info-panel line."""
    spans = []
    first = True
    for p in parts:
        txt, cls = p[0], p[1]
        pid = f' id="{p[2]}"' if len(p) > 2 and p[2] else ''

        if first:
            spans.append(f'<tspan x="{INFO_X}" class="{cls}"{pid}>{escape(txt)}</tspan>')
            first = False
        else:
            spans.append(f'<tspan class="{cls}"{pid}>{escape(txt)}</tspan>')

    return f'<text y="{y}" font-family="ConsolasFallback,Consolas,monospace" font-size="16px">{"".join(spans)}</text>'


def dots(n):
    return f' {"." * n} ' if n else ''


def fdots(key, value):
    """Dots to right-align a static value at the LINE_CHARS column."""
    return dots(max(LINE_CHARS - len(key) - len(': ') - len(value), 1))


def card_svg(mode):
    """Build the full card SVG for the given mode."""
    t = THEMES[mode]
    grid = load_art()
    y = 30
    L = []

    def add(parts):
        nonlocal y
        L.append(line(y, parts, t))
        y += LINE_H

    head = f"{INFO['name']}@{INFO['username']}"
    dash_w = max(10, int((CARD_W - INFO_X - 30) / 9.6) - len(head) - 2)
    sep = '─' * dash_w

    # header
    add([(head, 'text')])
    add([(sep, 'sep')])
    # system
    add([('. ', 'cc'), ('OS', 'key'), (':', 'cc'), (fdots('OS', INFO['os']), 'cc'), (INFO['os'], 'value')])
    add([('. ', 'cc'), ('Uptime', 'key'), (':', 'cc'),
         (dots(61), 'cc', 'age_data_dots'), ('X years, X months', 'value', 'age_data')])
    add([('. ', 'cc'), ('Host', 'key'), (':', 'cc'), (fdots('Host', INFO['host']), 'cc'), (INFO['host'], 'value')])
    add([('. ', 'cc'), ('Kernel', 'key'), (':', 'cc'), (fdots('Kernel', INFO['kernel']), 'cc'), (INFO['kernel'], 'value')])
    add([('. ', 'cc')])
    # languages
    add([('. ', 'cc'), ('Languages.Programming', 'key'), (':', 'cc'), (fdots('Languages.Programming', INFO['prog']), 'cc'), (INFO['prog'], 'value')])
    add([('. ', 'cc'), ('Languages.Computer', 'key'), (':', 'cc'), (fdots('Languages.Computer', INFO['computer']), 'cc'), (INFO['computer'], 'value')])
    add([('. ', 'cc'), ('Languages.Real', 'key'), (':', 'cc'), (fdots('Languages.Real', INFO['real']), 'cc'), (INFO['real'], 'value')])
    add([('. ', 'cc')])
    # infrastructure & hardware
    add([('. ', 'cc'), ('Systems & Network', 'key'), (':', 'cc'), (fdots('Systems & Network', INFO['sysnet']), 'cc'), (INFO['sysnet'], 'value')])
    add([('. ', 'cc'), ('Security & Auditing', 'key'), (':', 'cc'), (fdots('Security & Auditing', INFO['secaud']), 'cc'), (INFO['secaud'], 'value')])
    add([('. ', 'cc'), ('Electrical & Hardware', 'key'), (':', 'cc'), (fdots('Electrical & Hardware', INFO['elechw']), 'cc'), (INFO['elechw'], 'value')])
    add([('. ', 'cc')])
    # contact
    add([('- Contact ', 'sep'), ('─' * max(0, dash_w - 10), 'sep')])
    add([('. ', 'cc'), ('GitHub', 'key'), (':', 'cc'), (fdots('GitHub', INFO['github']), 'cc'), (INFO['github'], 'value')])
    add([('. ', 'cc'), ('Discord', 'key'), (':', 'cc'), (fdots('Discord', INFO['discord']), 'cc'), (INFO['discord'], 'value')])
    add([('. ', 'cc'), ('Telegram', 'key'), (':', 'cc'), (fdots('Telegram', INFO['telegram']), 'cc'), (INFO['telegram'], 'value')])
    add([('. ', 'cc'), ('Email', 'key'), (':', 'cc'), (fdots('Email', INFO['email']), 'cc'), (INFO['email'], 'value')])
    # github stats (dynamic)
    add([('- GitHub Stats ', 'sep'), ('─' * max(0, dash_w - 15), 'sep')])
    add([('. ', 'cc'), ('Repos', 'key'), (':', 'cc'), (dots(6), 'cc', 'repo_data_dots'),
         ('0', 'value', 'repo_data'),
         (' {Contributed: ', 'cc'), (dots(0), 'cc', 'contrib_data_dots'),
         ('0', 'value', 'contrib_data'), ('} | Stars: ', 'cc'),
         (dots(14), 'cc', 'star_data_dots'), ('0', 'value', 'star_data')])
    add([('. ', 'cc'), ('Commits', 'key'), (':', 'cc'), (dots(22), 'cc', 'commit_data_dots'),
         ('0', 'value', 'commit_data'), (' | Followers: ', 'cc'),
         (dots(10), 'cc', 'follower_data_dots'), ('0', 'value', 'follower_data')])
    add([('. ', 'cc'), ('Lines of Code', 'key'), (':', 'cc'),
         (dots(17), 'cc', 'loc_data_dots'), ('0', 'value', 'loc_data'),
         (' (', 'cc'), (dots(0), 'cc', 'loc_add_dots'), ('0', 'value', 'loc_add'),
         ('++,', 'cc'), (dots(7), 'cc', 'loc_del_dots'), ('0', 'value', 'loc_del'), ('--)', 'cc')])

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{CARD_W}px" height="{CARD_H}px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {t['key']};}}
.value {{fill: {t['value']};}}
.sep {{fill: {t['sep']};}}
.cc {{fill: {t['cc']};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{CARD_W}px" height="{CARD_H}px" fill="{t['bg']}" rx="15"/>
{art_svg(grid)}
<g fill="{t['text']}">
{''.join(L)}
</g>
</svg>'''

    return svg


if __name__ == '__main__':
    for mode in THEMES:
        out = os.path.join(HERE, f'{mode}_mode.svg')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(card_svg(mode))
        print('wrote', out)
# -*- coding: utf-8 -*-
"""
index.html — fix requirement #1 (full-card clickability) and a structural bug
(a second, nested <main> wrapping the "Academic" tiles, invalid inside the
page's real <main id="main">). Rebuilds the block using the site's normal
.section/.wrap convention and turns each tile into a single <a> that covers
the whole card, following the same pattern already used by .card.program-card
elsewhere on the site (whole card is the link; a trailing cue replaces the
nested button/link).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "index.html"

OLD_OPEN = (
    '  <main class="flex min-h-screen items-center justify-center px-5 py-12 sm:px-8 lg:px-10">\n'
    '    \n\n'
    '      <section class="w-full max-w-[1440px]" aria-label="Academic programmes">\n\n'
    '        <div class="academic-head reveal">\n'
    '          <h2 id="academic-h" class="academic-title">Academic</h2>\n'
    '          <p class="th-body">ค้นหาเส้นทางการศึกษาที่เหมาะกับคุณ ที่คณะบริหารธุรกิจเพื่อสังคม มศว</p>\n'
    '        </div>\n'
    '        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">\n'
    '          \n'
)
NEW_OPEN = (
    '  <section class="section academic-section" aria-labelledby="academic-h">\n'
    '    <div class="wrap">\n'
    '      <div class="academic-head reveal">\n'
    '        <h2 id="academic-h" class="academic-title">Academic</h2>\n'
    '        <p class="th-body">ค้นหาเส้นทางการศึกษาที่เหมาะกับคุณ ที่คณะบริหารธุรกิจเพื่อสังคม มศว</p>\n'
    '      </div>\n'
    '      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">\n'
)

OLD_CLOSE = (
    '        </div>\n'
    '      </section>\n'
    '    </main>\n'
)
NEW_CLOSE = (
    '      </div>\n'
    '    </div>\n'
    '  </section>\n'
)

CARD_RE = re.compile(
    r'<!-- (?P<label>[^>]+?) -->\s*'
    r'<article class="programme-card group (?P<bg>bg-\[[^\]]+\])">\s*'
    r'<div class="programme-decoration"></div>\s*'
    r'<div class="programme-icon">\s*'
    r'<i class="(?P<icon>[^"]+)" aria-hidden="true"></i>\s*'
    r'</div>\s*'
    r'<div class="programme-content">\s*'
    r'<h2>(?P<th>[^<]+)</h2>\s*'
    r'<p class="programme-en">(?P<en>[^<]+)</p>\s*'
    r'<p class="programme-description">\s*(?P<desc>[^<]+?)\s*</p>\s*'
    r'<a class="programme-button" href="[^"]*">\s*'
    r'<span>รายละเอียด</span>\s*'
    r'<i class="fa-solid fa-arrow-right" aria-hidden="true"></i>\s*'
    r'</a>\s*'
    r'</div>\s*'
    r'<span class="programme-accent"></span>\s*'
    r'</article>',
    re.S,
)

REAL_HREF = {
    "Admission": "admissions.html",
    "Undergraduate": "programs.html?level=undergraduate",
    "Graduate": "programs.html#graduate-entry",
    "International": "international.html",
}


def card_repl(m):
    label = m.group("label").strip()
    href = REAL_HREF[label]
    return (
        '<!-- %s -->\n'
        '          <a class="programme-card group %s" href="%s">\n'
        '            <div class="programme-decoration"></div>\n\n'
        '            <div class="programme-icon">\n'
        '              <i class="%s" aria-hidden="true"></i>\n'
        '            </div>\n\n'
        '            <div class="programme-content">\n'
        '              <h2>%s</h2>\n'
        '              <p class="programme-en">%s</p>\n'
        '              <p class="programme-description">\n'
        '                %s\n'
        '              </p>\n\n'
        '              <span class="programme-button" aria-hidden="true">\n'
        '                <span>รายละเอียด</span>\n'
        '                <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>\n'
        '              </span>\n'
        '            </div>\n\n'
        '            <span class="programme-accent"></span>\n'
        '          </a>'
        % (label, m.group("bg"), href, m.group("icon"), m.group("th"), m.group("en"), m.group("desc"))
    )


def main():
    s = IDX.read_text(encoding="utf-8")
    assert OLD_OPEN in s, "academic tiles opening block not found (already patched?)"
    assert OLD_CLOSE in s, "academic tiles closing block not found (already patched?)"

    s, n_cards = CARD_RE.subn(card_repl, s)
    assert n_cards == 4, "expected 4 programme-card tiles, patched %d" % n_cards

    s = s.replace(OLD_OPEN, NEW_OPEN, 1)
    s = s.replace(OLD_CLOSE, NEW_CLOSE, 1)

    IDX.write_text(s, encoding="utf-8")
    print("index.html : academic tiles -- fixed nested <main>, made %d cards fully clickable" % n_cards)


if __name__ == "__main__":
    main()

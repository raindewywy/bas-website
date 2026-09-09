# -*- coding: utf-8 -*-
"""
faculty.html -- requirements #7/#8: each person's Thai/English name must
appear exactly once. The page currently renders BOTH the "variant A" and
"variant B" name markup for every card at once (a leftover A/B comparison
toggle), so every name is duplicated in the DOM regardless of which one is
visually hidden. Fix at the source: keep a single name block per card
(Thai name primary / English name secondary -- the same hierarchy already
used on leadership.html), and drop the toggle UI that this template was
scaffolded for.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAC = ROOT / "faculty.html"

TOGGLE_RE = re.compile(
    r'\s*<div class="staff-toggle mt-5">.*?</div>\n?',
    re.S,
)

CARD_NAME_RE = re.compile(
    r'<div class="staff-name-a"><div class="en-name th-body">(?P<th1>[^<]+)</div>'
    r'<div class="th-name" style="color:var\(--muted\);font-size:\.85rem;margin-top:\.15rem;">(?P<en1>[^<]+)</div></div>'
    r'<div class="staff-name-b"><div class="th-name th-body">(?P<th2>[^<]+)</div>'
    r'<div class="en-name">(?P<en2>[^<]+)</div></div>'
)

CARD_CLASS_RE = re.compile(r'class="staff-card staff-name-a reveal"')


def name_repl(m):
    th, en = m.group("th1"), m.group("en1")
    assert th == m.group("th2") and en == m.group("en2"), (th, en, m.group("th2"), m.group("en2"))
    return (
        '<div class="th-name th-body" style="font-weight:700;font-size:1.02rem;">%s</div>'
        '<div class="en-name" style="color:var(--muted);font-size:.85rem;">%s</div>' % (th, en)
    )


def main():
    s = FAC.read_text(encoding="utf-8")

    s, n_toggle = TOGGLE_RE.subn("", s)

    s, n_names = CARD_NAME_RE.subn(name_repl, s)

    # the toggle-driven modifier class no longer means anything -- plain staff-card
    s, n_class = CARD_CLASS_RE.subn('class="staff-card reveal"', s)

    FAC.write_text(s, encoding="utf-8")
    print("faculty.html : toggle removed=%d, cards de-duplicated=%d, classes normalised=%d"
          % (n_toggle, n_names, n_class))


if __name__ == "__main__":
    main()

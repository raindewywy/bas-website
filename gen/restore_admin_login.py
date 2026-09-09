# -*- coding: utf-8 -*-
"""
Restore the admin login affordance (shield button in the header + login modal
+ admin bar) exactly as it was before remove_admin_demo.py ran.

Each page is restored from its OWN pristine copy so the markup goes back
byte-identical — nothing else on the page is touched. The JS (initAdmin) and
the CSS (.admin-modal / .admin-bar / .admin-toggle) were never removed, so the
feature works again as soon as the markup is back.
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIG = Path("/mnt/user-data/uploads/bas-website")

HEADER = '<header class="site-header">'
SEARCH_BTN_RE = re.compile(
    r'<button class="icon-btn search-toggle search-only"[^>]*>.*?</button>', re.S)
TOGGLE_RE = re.compile(
    r'\s*<button class="icon-btn admin-toggle" id="admin-open"[^>]*>.*?</button>', re.S)


def main():
    restored = skipped = 0
    for path in sorted(glob.glob(str(ROOT / "*.html"))):
        p = Path(path)
        orig_p = ORIG / p.name
        if not orig_p.exists():
            print("  ! no pristine copy:", p.name)
            continue

        cur = p.read_text(encoding="utf-8")
        if 'id="admin-modal"' in cur and 'id="admin-open"' in cur:
            skipped += 1
            continue

        orig = orig_p.read_text(encoding="utf-8")

        # --- 1. modal + admin bar block (sits right before <header>) --------
        a = orig.index('<div class="admin-modal"')
        b = orig.index(HEADER)
        block = orig[a:b]

        if 'id="admin-modal"' not in cur:
            i = cur.index(HEADER)
            cur = cur[:i] + block + cur[i:]

        # --- 2. shield button, back in its original slot -------------------
        if 'id="admin-open"' not in cur:
            m = TOGGLE_RE.search(orig)
            assert m, "toggle not found in pristine %s" % p.name
            sm = SEARCH_BTN_RE.search(cur)
            assert sm, "search toggle not found in %s" % p.name
            cur = cur[:sm.end()] + m.group(0) + cur[sm.end():]

        p.write_text(cur, encoding="utf-8")
        restored += 1

    print("restored: %d pages | already present: %d" % (restored, skipped))


if __name__ == "__main__":
    main()

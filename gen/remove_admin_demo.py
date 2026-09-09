# -*- coding: utf-8 -*-
"""
Remove the site-wide fake "admin login" demo scaffold (requirement #12):
a shield-icon header button that opens a login modal explicitly labelled
"* ต้นแบบนี้จำลองหน้าจอเข้าสู่ระบบเพื่อสาธิตเท่านั้น ไม่ได้เชื่อมต่อฐานข้อมูลผู้ใช้จริง"
("this prototype simulates a login screen for demo purposes only -- not
wired to a real user database"), plus the "admin bar" it turns on. This is
development/demo scaffolding, not a real feature, and is present verbatim
on every page (part of the shared header shell) -- fixed at the source
across all pages in one pass.
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BLOCK_RE = re.compile(
    r'<div class="admin-modal" id="admin-modal" aria-hidden="true">.*?'
    r'id="admin-logout"[^>]*>ออกจากระบบ</button>\s*</div>\s*</div>\s*',
    re.S,
)
TOGGLE_RE = re.compile(
    r'\s*<button class="icon-btn admin-toggle" id="admin-open"[^>]*>.*?</button>',
    re.S,
)


def main():
    total = 0
    for path in sorted(glob.glob(str(ROOT / "*.html"))):
        p = Path(path)
        s = orig = p.read_text(encoding="utf-8")
        s, n1 = BLOCK_RE.subn("", s)
        s, n2 = TOGGLE_RE.subn("", s)
        if s != orig:
            p.write_text(s, encoding="utf-8")
            total += n1 + n2
            print("cleaned admin demo scaffold:", p.name, n1, n2)
    print("total removals:", total)


if __name__ == "__main__":
    main()

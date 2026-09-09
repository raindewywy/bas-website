# -*- coding: utf-8 -*-
"""
Palette brightening — approved by the faculty:

  --brand-ink  #006775 -> #06D0EB   (text, links, icon fills — everywhere)
  dark bands   #04262C -> #00505C   (page hero, CTA band) + footer
  any surface filled with #06D0EB gets white text

Kept deliberately:
  --brand-deep #00505C — still used for hover/active states so buttons and the
  dean-direct pill still darken on hover (as chosen earlier).
  --ink #0F1719 — body-text colour, untouched.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"

EDITS = [
    # ---- tokens ---------------------------------------------------------
    ("  --brand-ink:#006775;     /* readable brand ink on light surfaces — passes AA for text/links */",
     "  --brand-ink:#06D0EB;     /* brand ink — brightened per faculty request (was #006775) */"),

    ("  --deep-900:#04262C;   /* พื้นเข้มสายเดียวกับ #00B3C9 — ตัวอักษรขาวได้ 15.6:1 */",
     "  --deep-900:#00505C;   /* แถบเข้ม (hero / CTA) — สว่างขึ้น ตัวอักษรขาวยังผ่าน AA */"),

    ("  --focus:#006775;",
     "  --focus:#00505C;"),

    # ---- surfaces that used the pale tint + ink text -> solid brand + white
    (".stat-tile-v2 .stat-ico{\n"
     "  width:52px; height:52px; border-radius:50%; flex:none;\n"
     "  background:var(--brand-tint); color:var(--brand-ink);",
     ".stat-tile-v2 .stat-ico{\n"
     "  width:52px; height:52px; border-radius:50%; flex:none;\n"
     "  background:#06D0EB; color:#fff;"),

    ('.mega a:hover, .mega a:focus-visible{background:var(--brand-tint); color:var(--brand-ink); border-left-color:var(--brand);}',
     '.mega a:hover, .mega a:focus-visible{background:#06D0EB; color:#fff; border-left-color:#06D0EB;}'),

    ('.drawer-sub a:hover, .drawer-sub a:focus-visible{background:var(--brand-tint); color:var(--brand-ink);}',
     '.drawer-sub a:hover, .drawer-sub a:focus-visible{background:#06D0EB; color:#fff;}'),

    ('.card-tag{background:var(--brand-tint); color:var(--brand-ink); border-radius:2px;}',
     '.card-tag{background:#06D0EB; color:#fff; border-radius:2px;}'),

    # ---- footer band ----------------------------------------------------
    ('.site-footer{background:var(--ink); color:rgba(255,255,255,.82); margin-top:var(--space-8);}',
     '.site-footer{background:#00505C; color:rgba(255,255,255,.86); margin-top:var(--space-8);}'),

    # ---- keep the approved "darken on hold" behaviour --------------------
    ('.dean-direct:hover, .dean-direct:focus-visible, .dean-direct:active{\n'
     '  background:var(--brand-ink); color:#fff; transform:translateY(-2px);',
     '.dean-direct:hover, .dean-direct:focus-visible, .dean-direct:active{\n'
     '  background:var(--brand-deep); color:#fff; transform:translateY(-2px);'),

    ('.dean-mail-btn:hover, .dean-mail-btn:focus-visible, .dean-mail-btn:active{\n'
     '  background:var(--brand-ink); border-color:var(--brand-ink); color:#fff;',
     '.dean-mail-btn:hover, .dean-mail-btn:focus-visible, .dean-mail-btn:active{\n'
     '  background:var(--brand-deep); border-color:var(--brand-deep); color:#fff;'),

    # B·A·S badge: bright fill, white letter (hover keeps the deep tone)
    ('.id-card:hover, .id-card:focus-within{\n'
     '  transform:translateY(-4px); box-shadow:var(--shadow-m); border-color:var(--brand-ink);\n'
     '}',
     '.id-card:hover, .id-card:focus-within{\n'
     '  transform:translateY(-4px); box-shadow:var(--shadow-m); border-color:#06D0EB;\n'
     '}'),
]


def main():
    css = CSS.read_text(encoding="utf-8")
    done = 0
    for old, new in EDITS:
        if old in css:
            css = css.replace(old, new, 1)
            done += 1
        else:
            print("  ! not found:", old.splitlines()[0][:70])
    CSS.write_text(css, encoding="utf-8")
    print("palette edits applied: %d/%d" % (done, len(EDITS)))


if __name__ == "__main__":
    main()

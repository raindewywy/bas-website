# -*- coding: utf-8 -*-
"""
Requirement #3 — อัตลักษณ์คณะ must follow the กรอบแนวคิด pattern.

Reference: swu.ac.th "กรอบแนวคิด การพัฒนา LOVES" — an intro line followed by a
row of equal-weight cards, ALL visible at once, each card = big letter +
English heading + Thai description. No tabs, no accordion, no hidden panels.

The BAS section was a tablist (one panel visible at a time), which is a
different component pattern. This converts it to the same card-grid
composition, reusing the existing .id-* classes and the site's own grid /
card / hover conventions.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "index.html"
CSS = ROOT / "assets" / "styles.css"

BAS = [
    ("B", "Business", "ธุรกิจที่เข้าใจจริง",
     "องค์ความรู้ด้านบัญชี การเงิน การตลาด การจัดการ และธุรกิจระหว่างประเทศ "
     "ที่สอนผ่านโจทย์จริงของภาคธุรกิจ ไม่ใช่กรณีศึกษาสำเร็จรูป"),
    ("A", "Administration", "บริหารอย่างมืออาชีพ",
     "ทักษะการตัดสินใจ การวางแผน และการนำองค์กร ที่นิสิตได้ฝึกจริงผ่านโครงงาน "
     "การแข่งขันเคส และการฝึกงานกับองค์กรพันธมิตร"),
    ("S", "Society", "เพื่อสังคมที่ดีกว่า",
     "คำว่า “เพื่อสังคม” อยู่ในชื่อคณะ ไม่ใช่กิจกรรมเสริม — ทุกหลักสูตรวัดความสำเร็จ "
     "ทั้งผลประกอบการและผลกระทบที่เกิดกับผู้คนและชุมชน"),
]


def cards():
    out = []
    for letter, en, th, desc in BAS:
        out.append(
            '<article class="id-card reveal">'
            '<span class="id-letter" aria-hidden="true">%s</span>'
            '<h3 class="id-en">%s</h3>'
            '<p class="id-th th-body">%s</p>'
            '<p class="id-desc th-body">%s</p>'
            "</article>" % (letter, en, th, desc)
        )
    return "".join(out)


NEW_SECTION = (
    '  <section class="section-tight identity-section" aria-labelledby="identity-h">\n'
    '    <div class="wrap">\n'
    '      <div class="section-head reveal"><div>\n'
    '        <p class="eyebrow">อัตลักษณ์คณะ</p>\n'
    '        <h2 id="identity-h" class="bi-heading"><span class="bi-th th-body">B · A · S</span>'
    '<span class="bi-en">Business Administration for Society</span></h2>\n'
    '        <p class="lede th-body">กรอบแนวคิดสามด้านที่กำหนดวิธีการเรียนการสอน '
    'การทำงาน และการวัดความสำเร็จของคณะ</p>\n'
    '      </div></div>\n'
    '      <div class="id-grid">' + cards() + '</div>\n'
    '    </div>\n'
    '  </section>'
)

OLD_CSS_START = "/* ---- 2. B · A · S strip ----------------------------------------------- */"
OLD_CSS_END = "/* ---- 3. Activity rail (carousel) -------------------------------------- */"

NEW_CSS = """/* ---- 2. B · A · S framework cards (กรอบแนวคิด pattern) ----------------- */
.identity-section{background:linear-gradient(180deg,var(--paper) 0%,var(--paper-dim) 100%);}
.id-grid{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:var(--space-4);}
.id-card{
  display:flex; flex-direction:column; align-items:center; text-align:center;
  gap:.45rem; padding:var(--space-6) var(--space-4) var(--space-5);
  background:var(--surface); border:1.5px solid var(--line); border-radius:var(--radius-l);
  transition:border-color var(--dur), box-shadow var(--dur), transform var(--dur);
}
.id-card:hover, .id-card:focus-within{
  border-color:var(--teal-600); transform:translateY(-3px); box-shadow:var(--shadow-m);
}
.id-letter{
  width:68px; height:68px; flex:none; border-radius:50%;
  background:var(--brand-ink); color:#fff;
  display:grid; place-items:center; margin-bottom:.35rem;
  font-family:var(--font-display); font-size:2rem; font-weight:700; line-height:1;
  transition:background var(--dur), transform var(--dur);
}
.id-card:hover .id-letter{background:var(--teal-700); transform:scale(1.06);}
.id-en{font-family:var(--font-display); font-weight:600; font-size:1.15rem; color:var(--ink);}
.id-th{font-size:.9rem; font-weight:600; color:var(--brand-ink);}
.id-desc{font-size:.9rem; color:var(--muted); max-width:34ch;}
@media (max-width:900px){
  .id-grid{grid-template-columns:repeat(2,minmax(0,1fr));}
}
@media (max-width:640px){
  .id-grid{grid-template-columns:1fr;}
  .id-card{padding:var(--space-5) var(--space-4); gap:.35rem;}
  .id-letter{width:56px; height:56px; font-size:1.6rem;}
  .id-desc{max-width:none;}
}
@media (prefers-reduced-motion: reduce){
  .id-card:hover, .id-card:focus-within{transform:none;}
  .id-card:hover .id-letter{transform:none;}
}

"""


def main():
    # ---- HTML -----------------------------------------------------------
    s = IDX.read_text(encoding="utf-8")
    m = re.search(
        r'  <section class="section-tight identity-section" aria-labelledby="identity-h">.*?\n  </section>',
        s, re.S,
    )
    assert m, "identity section not found"
    assert "id-grid" not in m.group(0), "already converted"
    s = s[:m.start()] + NEW_SECTION + s[m.end():]
    IDX.write_text(s, encoding="utf-8")
    print("index.html : อัตลักษณ์คณะ tablist -> กรอบแนวคิด card grid (3 cards, all visible)")

    # ---- CSS ------------------------------------------------------------
    css = CSS.read_text(encoding="utf-8")
    a = css.index(OLD_CSS_START)
    b = css.index(OLD_CSS_END)
    css = css[:a] + NEW_CSS + css[b:]
    CSS.write_text(css, encoding="utf-8")
    print("styles.css : .id-tabs/.id-panel tab CSS -> .id-grid card CSS")


if __name__ == "__main__":
    main()

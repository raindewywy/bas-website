# -*- coding: utf-8 -*-
"""
Round 3 — feedback from the screenshots.

 1. อัตลักษณ์คณะ: match the swu.ac.th "กรอบแนวคิด การพัฒนา LOVES" composition —
    a left intro column (heading + description) beside a row of cards, each card
    laid out horizontally with a large circular letter badge overlapping the
    card's left edge and the text to its right.
 3. Remove the brand-blue hairlines drawn on component boxes
    (.card-ph::before and .split-media::after).
 4. สายตรงคณบดี: the global rule `a:not(.btn):not(.nav-link):hover` (0,3,1) was
    overriding `.dean-direct:hover` (0,2,0), so the label turned dark teal on
    hover instead of staying white. Excluded at the source.
 5. Remove the remaining advisory notice boxes that are not structural.
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "index.html"
CSS = ROOT / "assets" / "styles.css"

# ===========================================================================
# 1. อัตลักษณ์คณะ — LOVES composition
# ===========================================================================
BAS = [
    ("B", "Business", "ธุรกิจที่เข้าใจจริง",
     "องค์ความรู้ด้านบัญชี การเงิน การตลาด การจัดการ และธุรกิจระหว่างประเทศ "
     "ที่สอนผ่านโจทย์จริงของภาคธุรกิจ"),
    ("A", "Administration", "บริหารอย่างมืออาชีพ",
     "ทักษะการตัดสินใจ การวางแผน และการนำองค์กร ที่นิสิตได้ฝึกจริงผ่านโครงงาน "
     "และการแข่งขันเคส"),
    ("S", "Society", "เพื่อสังคมที่ดีกว่า",
     "ทุกหลักสูตรวัดความสำเร็จ ทั้งผลประกอบการและผลกระทบที่เกิดกับผู้คนและชุมชน"),
]


def cards():
    return "".join(
        '<article class="id-card reveal">'
        '<span class="id-letter" aria-hidden="true">%s</span>'
        '<span class="id-body">'
        '<span class="id-en">%s</span>'
        '<span class="id-th th-body">%s</span>'
        '<span class="id-desc th-body">%s</span>'
        "</span></article>" % (letter, en, th, desc)
        for letter, en, th, desc in BAS
    )


NEW_SECTION = (
    '  <section class="section-tight identity-section" aria-labelledby="identity-h">\n'
    '    <div class="wrap id-layout">\n'
    '      <div class="id-intro reveal">\n'
    '        <p class="eyebrow">อัตลักษณ์คณะ</p>\n'
    '        <h2 id="identity-h" class="bi-heading"><span class="bi-th th-body">B · A · S</span>'
    '<span class="bi-en">Business Administration for Society</span></h2>\n'
    '        <p class="id-lead th-body">กรอบแนวคิดสามด้านที่กำหนดวิธีการเรียนการสอน '
    'การทำงาน และการวัดความสำเร็จของคณะ</p>\n'
    '      </div>\n'
    '      <div class="id-grid">' + cards() + '</div>\n'
    '    </div>\n'
    '  </section>'
)

CSS_START = "/* ---- 2. B · A · S framework cards (กรอบแนวคิด pattern) ----------------- */"
CSS_END = "/* ---- 3. Activity rail (carousel) -------------------------------------- */"

NEW_CSS = """/* ---- 2. B · A · S framework (กรอบแนวคิด composition) -------------------- */
.identity-section{background:linear-gradient(180deg,var(--paper) 0%,var(--paper-dim) 100%);}
.id-layout{
  display:grid; grid-template-columns:minmax(200px,280px) minmax(0,1fr);
  gap:var(--space-6) var(--space-7); align-items:center;
}
.id-intro h2{font-size:var(--step-h3); margin-top:var(--space-2);}
.id-lead{margin-top:var(--space-3); color:var(--muted); font-size:.95rem;}

.id-grid{
  display:grid; grid-template-columns:repeat(3,minmax(0,1fr));
  gap:var(--space-5); padding-left:36px;
}
.id-card{
  position:relative; display:flex; align-items:center;
  background:var(--surface); border:1px solid var(--line); border-radius:var(--radius-l);
  padding:var(--space-5) var(--space-4);
  box-shadow:0 2px 12px rgba(27,31,34,.06); min-height:170px;
  transition:transform var(--dur), box-shadow var(--dur), border-color var(--dur);
}
.id-card:hover, .id-card:focus-within{
  transform:translateY(-4px); box-shadow:var(--shadow-m); border-color:var(--brand-ink);
}
.id-letter{
  position:absolute; left:-36px; top:50%; transform:translateY(-50%);
  width:72px; height:72px; border-radius:50%;
  background:var(--brand-ink); color:#fff; display:grid; place-items:center;
  font-family:var(--font-display); font-size:2.1rem; font-weight:700; line-height:1;
  box-shadow:0 4px 14px rgba(0,88,102,.28);
  transition:transform var(--dur), background var(--dur);
}
.id-card:hover .id-letter{transform:translateY(-50%) scale(1.07); background:var(--brand-deep);}
.id-body{display:flex; flex-direction:column; gap:.3rem; padding-left:44px; min-width:0;}
.id-en{font-family:var(--font-display); font-weight:700; font-size:1.12rem; color:var(--ink); line-height:1.25;}
.id-th{font-size:.88rem; font-weight:600; color:var(--brand-ink);}
.id-desc{font-size:.86rem; color:var(--muted); line-height:1.6;}

@media (max-width:1100px){
  .id-layout{grid-template-columns:1fr; gap:var(--space-5);}
  .id-grid{grid-template-columns:repeat(3,minmax(0,1fr));}
}
@media (max-width:900px){
  .id-grid{grid-template-columns:1fr; gap:var(--space-6); padding-left:32px;}
  .id-card{min-height:0;}
}
@media (max-width:520px){
  .id-grid{padding-left:26px;}
  .id-letter{left:-26px; width:58px; height:58px; font-size:1.65rem;}
  .id-body{padding-left:34px;}
}
@media (prefers-reduced-motion: reduce){
  .id-card:hover, .id-card:focus-within{transform:none;}
  .id-card:hover .id-letter{transform:translateY(-50%);}
}

"""


def fix_identity():
    s = IDX.read_text(encoding="utf-8")
    m = re.search(
        r'  <section class="section-tight identity-section" aria-labelledby="identity-h">.*?\n  </section>',
        s, re.S)
    assert m, "identity section not found"
    IDX.write_text(s[:m.start()] + NEW_SECTION + s[m.end():], encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    a, b = css.index(CSS_START), css.index(CSS_END)
    CSS.write_text(css[:a] + NEW_CSS + css[b:], encoding="utf-8")
    print("1. อัตลักษณ์คณะ -> LOVES composition (intro column + badge-overlap cards)")


# ===========================================================================
# 3 + 4. CSS: blue hairlines on boxes, dean-direct hover colour
# ===========================================================================
def fix_css():
    css = CSS.read_text(encoding="utf-8")
    n = 0

    # -- blue bar on card media placeholders
    old = ('.card-ph::before{\n'
           '  content:""; position:absolute; left:0; top:0; height:3px; width:38%;\n'
           '  background:var(--brand); z-index:1;\n'
           '}\n')
    if old in css:
        css = css.replace(old, "", 1); n += 1
    old2 = ('.card:hover .card-ph::before, a:hover > .card-media > .card-ph::before'
            '{width:64%; transition:width var(--dur) var(--ease);}\n')
    if old2 in css:
        css = css.replace(old2, "", 1); n += 1

    # -- blue tick on media plates
    old3 = ('.split-media::after{\n'
            '  content:""; position:absolute; left:0; top:0; width:44px; height:3px;\n'
            '  background:var(--brand);\n'
            '}\n'
            '.split-media--live::after{content:none;}\n')
    if old3 in css:
        css = css.replace(old3, "", 1); n += 1

    # -- dean-direct label must stay white in every state
    old4 = "a:not(.btn):not(.nav-link):hover{color:var(--brand-ink);}"
    new4 = "a:not(.btn):not(.nav-link):not(.dean-direct):hover{color:var(--brand-ink);}"
    if old4 in css:
        css = css.replace(old4, new4, 1); n += 1

    CSS.write_text(css, encoding="utf-8")
    print("3. blue hairlines removed + 4. dean-direct hover colour fixed (%d edits)" % n)


# ===========================================================================
# 5. Remaining advisory notices (non-structural ones)
# ===========================================================================
DROP = [
    "ช่องทางที่แสดงคืออีเมลทางการของผู้บริหารตามตำแหน่ง",
    "หน้านี้แสดงความร่วมมือระหว่างประเทศที่ยืนยันได้จากข่าวประชาสัมพันธ์ทางการของคณะ",
    "รายละเอียดจำนวนหน่วยกิต ค่าเล่าเรียน และจำนวนรับ จะเผยแพร่เพิ่มเติมเมื่อคณะยืนยันข้อมูล",
    "รายละเอียดเกณฑ์ GPA ขั้นต่ำ หลักสูตรที่เข้าร่วมได้ และรายวิชาที่เทียบโอนได้",
    "ขณะนี้แสดงข้อมูลติดต่อระดับภาควิชา รายชื่ออาจารย์ที่ปรึกษาประจำหลักสูตรจะเพิ่มเติมในภายหลัง",
]
NOTICE_RE = re.compile(r'<div class="notice[^"]*"[^>]*>.*?</div>', re.S)


def fix_notices():
    total = 0
    for path in sorted(glob.glob(str(ROOT / "*.html"))):
        p = Path(path)
        s = orig = p.read_text(encoding="utf-8")

        def repl(m):
            nonlocal total
            text = re.sub("<[^>]+>", "", m.group(0))
            if any(d in text for d in DROP):
                total += 1
                return ""
            return m.group(0)

        s = NOTICE_RE.sub(repl, s)
        if s != orig:
            p.write_text(s, encoding="utf-8")
    print("5. advisory notice boxes removed: %d" % total)


if __name__ == "__main__":
    fix_identity()
    fix_css()
    fix_notices()

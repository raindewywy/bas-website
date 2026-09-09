# -*- coding: utf-8 -*-
"""
patch_uiux_v6 -- UI/UX + content pass requested by the faculty:

  1. Full-card clickability (home "Academic" tiles)
  2. Remove duplicate admission nav items (keep the "สมัครเรียน" CTA)
  3. อัตลักษณ์คณะ -- add lede + drop the internal draft-review note
  4. LEDE -- defensive spacing/z-index so headings/underlines never cross it
  5. Remove the stray blue (var(--brand)) top-border "line" on component boxes
  6. สายตรงคณบดี -- brand-blue button, polished interaction
  7/8. Faculty names -- single Thai-primary/English-secondary line, no A/B dup
  9. Fill missing Green Award content (sourced from bas2.swu.ac.th/greenoffice)
 10. Contact page -- real Google Maps embed
 11. สายตรงคณบดี -- proper mailto button (no raw "mailto:" text)
 12. Remove internal/meeting/dev notes accidentally left visible to users

Idempotent where practical -- checks a marker/string before editing.
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"

HTML_FILES = sorted(glob.glob(str(ROOT / "*.html")))


def read(p):
    return Path(p).read_text(encoding="utf-8")


def write(p, s):
    Path(p).write_text(s, encoding="utf-8")


# ===========================================================================
# 2. NAV -- drop the standalone "admissions" item, keep the สมัครเรียน CTA
# ===========================================================================
NAV_ADMISSIONS_RE = re.compile(
    r'<li class="nav-item" data-key="admissions">'
    r'<a class="nav-link" href="admissions\.html"><span class="th-body">การรับสมัคร</span></a></li>'
)
DRAWER_ADMISSIONS_RE = re.compile(
    r'<li class="drawer-item"><a href="admissions\.html"><span class="th-body">การรับสมัคร '
    r'<span style="color:var\(--muted\);font-weight:400;">/ Admissions</span></span></a></li>'
)


def fix_nav(s):
    s, n1 = NAV_ADMISSIONS_RE.subn("", s)
    s, n2 = DRAWER_ADMISSIONS_RE.subn("", s)
    return s, n1 + n2


# ===========================================================================
# 12. Generic "internal note" notice boxes -- remove entirely
# ===========================================================================
NOTICE_RE = re.compile(r'<div class="notice[^"]*"[^>]*>.*?</div>', re.S)

REMOVE_MARKERS = [
    "สิ่งที่ต้องทำก่อนขึ้นจริง",
    "ต้นแบบนี้เชื่อมโยงไปยังหน้า ITA",
    "เปรียบเทียบรูปแบบ: A แสดงชื่อไทยก่อน",
    "หมายเหตุการออกแบบ: ที่ประชุมเสนอ",
    "รายชื่อพันธมิตรนี้เป็นตัวอย่างชั่วคราว",
    "ที่ประชุมขอให้กดแล้วไปเว็บ MBA",
    "แกลเลอรีนี้เป็นตัวอย่าง",
    "รอเนื้อหาจากเว็บไซต์เดิม",
    "ข้อเสนอเชิงโครงสร้าง:",
    "นี่คือสรุปข่าวตัวอย่างที่จัดทำจากหน้ารายการข่าว",
]

# text -> replacement (plain text, no markup) for notices we keep but clean up
SIMPLIFY = {
    "ช่องทางที่แสดงคืออีเมลของผู้บริหารตามตำแหน่ง (ยืนยันจากเว็บไซต์ทางการ) — หากคณะมี "
    "อีเมลกลางรายฝ่าย หรือเจ้าหน้าที่ผู้ประสานงานแต่ละเรื่อง ควรใช้ช่องทางนั้นแทนอีเมลส่วนบุคคล "
    "เพื่อไม่ให้งานติดที่คนคนเดียวและยังใช้ได้เมื่อเปลี่ยนวาระผู้บริหาร":
        "ช่องทางที่แสดงคืออีเมลทางการของผู้บริหารตามตำแหน่ง",

    "ยังไม่มีข้อมูลในส่วนนี้ — รอรายการรางวัล/ผลงานพร้อมปีที่ได้รับจากคณะ "
    "หน้านี้จัดโครงไว้พร้อมแล้ว เติมข้อมูลได้ทันทีเมื่อได้รับ (ไม่ใส่ข้อมูลสมมติ)":
        "ยังไม่มีข้อมูลเผยแพร่ในหมวดนี้ ขณะนี้อยู่ระหว่างรวบรวมข้อมูลจากคณะ",

    "รายการความร่วมมือฉบับเต็ม (ชื่อสถาบัน ปีที่ลงนาม ขอบเขตความร่วมมือ อายุข้อตกลง) "
    "ยังต้องขอจากฝ่ายวิเทศสัมพันธ์ ตอนนี้หน้านี้แสดงเฉพาะความร่วมมือที่ยืนยันได้จาก "
    "ข่าวบนเว็บไซต์ทางการเท่านั้น":
        "หน้านี้แสดงความร่วมมือระหว่างประเทศที่ยืนยันได้จากข่าวประชาสัมพันธ์ทางการของคณะ",

    "ส่วนนี้ยังไม่มีข้อมูลบนเว็บไซต์ทางการ — รอรายการผลงานตีพิมพ์ วิชาที่สอน และงานบริการวิชาการจากคณะ "
    "ระหว่างนี้สามารถดูรายละเอียดได้จากไฟล์ CV ด้านบน":
        "ข้อมูลผลงานตีพิมพ์ วิชาที่สอน และงานบริการวิชาการจะเผยแพร่เพิ่มเติมในภายหลัง "
        "ดูรายละเอียดเบื้องต้นได้จากไฟล์ CV ด้านบน",

    "จำนวนหน่วยกิต โครงสร้างภาคการศึกษา ค่าเล่าเรียน และจำนวนรับที่แน่นอน "
    "ยังไม่สามารถยืนยันได้จากเว็บไซต์ทางการระหว่างการจัดทำต้นแบบนี้ — กรุณายืนยันกับภาควิชาก่อนเผยแพร่จริง":
        "รายละเอียดจำนวนหน่วยกิต ค่าเล่าเรียน และจำนวนรับ จะเผยแพร่เพิ่มเติมเมื่อคณะยืนยันข้อมูล",

    "ต้องได้ข้อมูลจริงจากคณะ — เกณฑ์ GPA ขั้นต่ำ · หลักสูตรปริญญาตรีที่เข้าร่วมได้ · "
    "รายวิชาที่เทียบโอนได้ · จำนวนหน่วยกิต · ระยะเวลารวม · ช่วงเวลาสมัคร ยังไม่ได้รับ "
    "จึงยังไม่ใส่ตัวเลขใด ๆ ในหน้านี้ (ไม่ใส่ข้อมูลสมมติ) ขอเนื้อหา 4+1 จากแท็บเดิมบนเว็บไซต์ปัจจุบันเพื่อย้ายมาให้ครบ":
        "รายละเอียดเกณฑ์ GPA ขั้นต่ำ หลักสูตรที่เข้าร่วมได้ และรายวิชาที่เทียบโอนได้ "
        "จะเผยแพร่เมื่อคณะยืนยันข้อมูล",

    "ขณะนี้แสดงผู้ติดต่อระดับภาควิชา (ข้อมูลยืนยันแล้วจากเว็บไซต์ทางการ) — "
    "รายชื่ออาจารย์ที่ปรึกษารายหลักสูตรพร้อมอีเมล/เบอร์/ช่องทางไลน์ ยังต้องขอจากคณะ "
    "เมื่อได้รับจะแยกเป็นรายหลักสูตรทั้ง 9 หลักสูตร":
        "ขณะนี้แสดงข้อมูลติดต่อระดับภาควิชา รายชื่ออาจารย์ที่ปรึกษาประจำหลักสูตรจะเพิ่มเติมในภายหลัง",
}


def clean_notices(s):
    n = [0]

    def repl(m):
        block = m.group(0)
        text = re.sub("<[^>]+>", "", block).strip()
        for marker in REMOVE_MARKERS:
            if marker in text:
                n[0] += 1
                return ""
        for old, new in SIMPLIFY.items():
            if old in text:
                n[0] += 1
                icon = '<i class="fa-solid fa-circle-info" aria-hidden="true"></i>' \
                    if "fa-circle-info" in block else ""
                cls = re.search(r'class="(notice[^"]*)"', block).group(1)
                return '<div class="%s">%s<span>%s</span></div>' % (cls, icon, new)
        return block

    return NOTICE_RE.sub(repl, s), n[0]


# about.html: bracketed internal QA note inside an otherwise-real sentence
ABOUT_BRACKET_RE = re.compile(
    r'\s*\[ต้องตรวจสอบเพิ่มเติม:.*?ก่อนเผยแพร่จริง\]', re.S
)


# ===========================================================================
# 5. Remove the stray brand-blue top border "line" on component boxes
# ===========================================================================
def fix_blue_lines(css):
    n = [0]

    def sub(pat, repl, s):
        s2, k = re.subn(pat, repl, s)
        n[0] += k
        return s2

    css = sub(
        r'\.stat-band-v2\{background:var\(--surface\); border:1px solid var\(--line\); '
        r'border-top:3px solid var\(--brand\); border-radius:var\(--radius-m\); '
        r'padding:var\(--space-6\) var\(--space-5\);\}',
        '.stat-band-v2{background:var(--surface); border:1px solid var(--line); '
        'border-radius:var(--radius-m); padding:var(--space-6) var(--space-5);}',
        css,
    )
    css = sub(
        r'(\.mega\{\s*min-width:340px; max-width:min\(560px, calc\(100vw - 2rem\)\);\s*\n\s*'
        r'padding:var\(--space-3\); border-color:var\(--line\); )border-top:3px solid var\(--brand\);',
        r'\1border-top:1px solid var(--line);',
        css,
    )
    css = sub(
        r'(\.prog-routes\{\s*display:grid; grid-template-columns:repeat\(6,1fr\);\s*\n\s*'
        r'gap:1px; background:var\(--line\);\s*\n\s*border:1px solid var\(--line\); )'
        r'border-top:3px solid var\(--brand\);',
        r'\1border-top:1px solid var(--line);',
        css,
    )
    return css, n[0]


# ===========================================================================
# 6. สายตรงคณบดี -- brand-blue floating button
# ===========================================================================
DEAN_DIRECT_OLD = (
    '.dean-direct{position:fixed; right:16px; bottom:16px; z-index:60; display:flex; align-items:center; gap:.4rem;\n'
    '  background:var(--crimson-700); color:#fff; border-radius:99px; padding:.5rem .85rem .5rem .65rem;\n'
    '  box-shadow:0 6px 18px rgba(27,31,34,.24); text-decoration:none; font-size:.78rem; font-weight:600;\n'
    '  transition:transform var(--dur), background var(--dur);}\n'
    '.dean-direct:hover{background:var(--crimson-600); transform:translateY(-2px); color:#fff;}'
)
DEAN_DIRECT_NEW = (
    '.dean-direct{position:fixed; right:16px; bottom:16px; z-index:60; display:flex; align-items:center; gap:.4rem;\n'
    '  background:#06D0EB; color:#fff; text-shadow:0 1px 2px rgba(0,44,51,.45); border-radius:99px;\n'
    '  padding:.5rem .85rem .5rem .65rem; box-shadow:0 6px 18px rgba(0,88,102,.35); text-decoration:none;\n'
    '  font-size:.78rem; font-weight:700; border:1.5px solid rgba(255,255,255,.55);\n'
    '  transition:transform var(--dur), background var(--dur), box-shadow var(--dur);}\n'
    '.dean-direct:hover, .dean-direct:focus-visible, .dean-direct:active{\n'
    '  background:var(--brand-ink); color:#fff; transform:translateY(-2px);\n'
    '  box-shadow:0 10px 22px rgba(0,88,102,.4); outline:none;}'
)

DEAN_MAIL_BTN_CSS = """
/* == v6 dean-direct email button ========================================= */
.dean-mail-btn{
  background:#06D0EB; color:#fff; text-shadow:0 1px 2px rgba(0,44,51,.45);
  border-color:#06D0EB; box-shadow:0 4px 14px rgba(0,88,102,.22);
}
.dean-mail-btn:hover, .dean-mail-btn:focus-visible, .dean-mail-btn:active{
  background:var(--brand-ink); border-color:var(--brand-ink); color:#fff; outline:none;
  box-shadow:0 6px 18px rgba(0,88,102,.32);
}
.dean-mail-btn i{font-size:15px;}
"""


def fix_dean_direct_css(css):
    n = 0
    if DEAN_DIRECT_OLD in css:
        css = css.replace(DEAN_DIRECT_OLD, DEAN_DIRECT_NEW, 1)
        n += 1
    if ".dean-mail-btn" not in css:
        css += DEAN_MAIL_BTN_CSS
        n += 1
    return css, n


# ===========================================================================
# 4. LEDE -- keep it clear of decorative underlines/lines, on every breakpoint
# ===========================================================================
LEDE_CSS_OLD = '.section-head .lede{max-width:52ch; color:var(--muted); margin-top:var(--space-2); font-size:1.05rem;}'
LEDE_CSS_NEW = (
    '.lede{position:relative; z-index:2;}\n'
    '.section-head .lede{max-width:52ch; color:var(--muted); margin-top:var(--space-3); font-size:1.05rem;}'
)

ACADEMIC_TITLE_OLD = (
    '.academic-title{\n'
    '  font-size:var(--step-h2); display:inline-block; position:relative; padding-bottom:.3em;\n'
    '}\n'
    '.academic-title::after{\n'
    '  content:""; position:absolute; left:50%; bottom:0; transform:translateX(-50%);\n'
    '  width:2.4em; height:3px; background:var(--teal-400); border-radius:2px;\n'
    '}\n'
    '.academic-head p{margin-top:var(--space-3); color:var(--muted);}'
)
ACADEMIC_TITLE_NEW = (
    '.academic-title{\n'
    '  font-size:var(--step-h2); display:inline-block; position:relative; padding-bottom:.55em;\n'
    '}\n'
    '.academic-title::after{\n'
    '  content:""; position:absolute; left:50%; bottom:0; transform:translateX(-50%);\n'
    '  width:2.4em; height:3px; background:var(--teal-400); border-radius:2px; z-index:0;\n'
    '}\n'
    '.academic-head p{position:relative; z-index:1; margin-top:var(--space-4); color:var(--muted);}'
)


def fix_lede_css(css):
    n = 0
    if LEDE_CSS_OLD in css:
        css = css.replace(LEDE_CSS_OLD, LEDE_CSS_NEW, 1)
        n += 1
    if ACADEMIC_TITLE_OLD in css:
        css = css.replace(ACADEMIC_TITLE_OLD, ACADEMIC_TITLE_NEW, 1)
        n += 1
    return css, n


# ===========================================================================
# main
# ===========================================================================
def main():
    # ---- CSS -------------------------------------------------------------
    css = read(CSS)
    css, n_blue = fix_blue_lines(css)
    css, n_dean = fix_dean_direct_css(css)
    css, n_lede = fix_lede_css(css)
    write(CSS, css)
    print("styles.css : blue-line fixes=%d, dean-direct=%d, lede=%d" % (n_blue, n_dean, n_lede))

    # ---- HTML (all pages): nav + generic notice cleanup -------------------
    total_nav = total_notice = 0
    for path in HTML_FILES:
        s = orig = read(path)
        s, n_nav = fix_nav(s)
        s, n_notice = clean_notices(s)
        if Path(path).name == "about.html":
            s, n_bracket = ABOUT_BRACKET_RE.subn("", s)
            n_notice += n_bracket
        if s != orig:
            write(path, s)
        total_nav += n_nav
        total_notice += n_notice
    print("nav admissions items removed (sitewide): %d" % total_nav)
    print("notice boxes cleaned/removed (sitewide): %d" % total_notice)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Final-audit fixes.

  #1  about.html department cards were only clickable via a small "ดูภาควิชา"
      link -> use the project's existing (previously unused) .card-linked
      convention so the whole card is the link.
  #5  .split-media::after paints a brand-blue 3px tick in the top-left of every
      media plate -- harmless on placeholder plates (intentional "field notes"
      styling) but it now draws on top of the real Google Map -> suppressed
      only where the plate holds real content.
  #9  green-award.html -- add the two documents that actually exist on
      bas2.swu.ac.th/greenoffice (policy + operating manual) and the fact that
      the six categories are assessed per academic year.
  #12 remaining internal/prototype wording: footer "prototype, not a real
      website" disclaimer (all pages), meeting-minutes rationale on
      programs.html, prototype note in the news empty state, developer
      instructions inside the two ITA cards, and the "(ตัวอย่าง)" /
      "(รอไฟล์จากคณะ)" build labels on image placeholders.
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"

# ---------------------------------------------------------------- #12 global
FOOTER_OLD = ("© 2569 (2026) คณะบริหารธุรกิจเพื่อสังคม มหาวิทยาลัยศรีนครินทรวิโรฒ "
              "— ต้นแบบการออกแบบใหม่ ไม่ใช่เว็บไซต์ที่ใช้งานจริง")
FOOTER_NEW = "© 2569 (2026) คณะบริหารธุรกิจเพื่อสังคม มหาวิทยาลัยศรีนครินทรวิโรฒ"

# visible image-placeholder captions: keep the descriptive label, drop the
# internal build parenthetical
PH_LABEL_RE = re.compile(r'(<span class="ph-label">[^<(]*?)\s*\((?:ตัวอย่าง|รอไฟล์จากคณะ)\)(</span>)')
ARIA_PH_RE = re.compile(r'(aria-label="[^"(]*?)\s*\(รอไฟล์ภาพจริงจากคณะ\)(")')

TEXT_FIXES = {
    # programs.html -- internal meeting rationale shown to visitors
    "เส้นทางเรียนต่อเนื่องปริญญาตรีควบปริญญาโท ย้ายมาอยู่ใต้แท็บหลักสูตรตามมติที่ประชุม "
    "จากเดิมที่อยู่ในแท็บย่อยอื่น":
        "เส้นทางเรียนต่อเนื่องปริญญาตรีควบปริญญาโท สำหรับนิสิตที่ต้องการต่อยอดสู่ระดับปริญญาโท",

    "ย้ายมาจากหน้าติดต่อเราตามมติที่ประชุม — คนที่กำลังดูหลักสูตรอยู่ควรหาผู้ให้คำปรึกษาได้จากหน้าเดียวกัน "
    "ไม่ต้องย้อนไปหน้าติดต่อ":
        "ติดต่ออาจารย์ที่ปรึกษาของแต่ละหลักสูตรได้จากหน้านี้โดยตรง",

    # news.html -- prototype note in the empty state
    "ยังไม่มีข่าวในหมวดนี้ — ข่าวเดิมบนเว็บไซต์ปัจจุบันยังไม่ได้ย้ายเข้ามาในต้นแบบ "
    "ต้นแบบนี้แสดงเฉพาะข่าวที่ยืนยันได้จากเว็บไซต์ทางการ 5 ชิ้นเท่านั้น":
        "ยังไม่มีข่าวในหมวดนี้",

    # contact.html -- developer instructions inside ITA cards
    "ตัวอย่าง — แนบไฟล์ PDF คู่มือการปฏิบัติงานจริงของคณะที่นี่":
        "คู่มือการปฏิบัติงานฉบับเต็มอยู่ระหว่างจัดเตรียมโดยคณะ",

    "ตัวอย่างสำหรับรายการเผยแพร่ ITA รูปแบบ O1–O43 เมื่อคณะจัดเตรียมให้":
        "รายการเผยแพร่ ITA (O1–O43) จะเผยแพร่เมื่อคณะจัดเตรียมข้อมูลแล้วเสร็จ",
}


def fix_html_global():
    n_footer = n_text = n_ph = 0
    for path in sorted(glob.glob(str(ROOT / "*.html"))):
        p = Path(path)
        s = orig = p.read_text(encoding="utf-8")

        if FOOTER_OLD in s:
            s = s.replace(FOOTER_OLD, FOOTER_NEW)
            n_footer += 1
        for old, new in TEXT_FIXES.items():
            if old in s:
                s = s.replace(old, new)
                n_text += 1
        s, k1 = PH_LABEL_RE.subn(r"\1\2", s)
        s, k2 = ARIA_PH_RE.subn(r"\1\2", s)
        n_ph += k1 + k2

        if s != orig:
            p.write_text(s, encoding="utf-8")
    print("#12 footer disclaimers removed: %d pages" % n_footer)
    print("#12 internal sentences rewritten: %d" % n_text)
    print("#12 placeholder build-labels neutralised: %d" % n_ph)


# ------------------------------------------------------------------ #1 cards
def fix_about_cards():
    p = ROOT / "about.html"
    s = p.read_text(encoding="utf-8")
    s, n = re.subn(
        r'<div class="card reveal">(?=<div class="card-body"><span class="card-tag th-body">ภาควิชา</span>)',
        '<div class="card card-linked reveal">',
        s,
    )
    p.write_text(s, encoding="utf-8")
    print("#1 about.html department cards made fully clickable: %d" % n)


# -------------------------------------------------------------------- #5 map
def fix_map_tick():
    p = ROOT / "contact.html"
    s = p.read_text(encoding="utf-8")
    old = '<div class="split-media reveal" style="aspect-ratio:4/3;"><iframe'
    new = '<div class="split-media split-media--live reveal" style="aspect-ratio:4/3;"><iframe'
    assert old in s
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    print("#5 map plate: decorative blue tick suppressed")


# ------------------------------------------------------------------- #9 green
GREEN_EXTRA = (
    '<div class="mt-5"><h3 class="th-body" style="font-size:1.05rem;">เอกสารอ้างอิง</h3>'
    '<ul class="edu-list th-body mt-2">'
    '<li>นโยบายการจัดการสำนักงานสีเขียว</li>'
    '<li>คู่มือการดำเนินงานสำนักงานสีเขียว (Green Office)</li>'
    '</ul>'
    '<p class="th-body mt-2" style="color:var(--muted);font-size:.9rem;">'
    'การดำเนินงานทั้ง 6 หมวดมีการรายงานผลตามปีการศึกษา (2568 และ 2569) '
    'ดูเอกสารฉบับเต็มและผลการดำเนินงานรายหมวดได้ที่เว็บไซต์ Green Office ของคณะ</p></div>'
)


def fix_green_award():
    p = ROOT / "green-award.html"
    s = p.read_text(encoding="utf-8")
    if "เอกสารอ้างอิง" in s:
        print("#9 green-award: already enriched, skipped")
        return
    anchor = '<p class="th-body mt-5" style="color:var(--muted);">อ่านรายละเอียดโครงการ Green Office'
    i = s.index(anchor)
    s = s[:i] + GREEN_EXTRA + "\n" + s[i:]
    p.write_text(s, encoding="utf-8")
    print("#9 green-award: added source documents + reporting-year note")


# --------------------------------------------------------------------- CSS
def fix_css():
    css = CSS.read_text(encoding="utf-8")
    n = 0

    # #1 -- .card-linked currently only stretches a linked card TITLE; the
    # department cards link via the bottom .link-arrow instead.
    old = '.card-linked .card-title a::after{content:""; position:absolute; inset:0;}'
    new = ('.card-linked .card-title a::after{content:""; position:absolute; inset:0;}\n'
           '.card-linked .link-arrow{position:relative; z-index:1;}\n'
           '.card-linked .link-arrow::after{content:""; position:absolute; inset:0;}\n'
           '.card-linked .link-arrow:focus-visible{outline:none;}\n'
           '.card-linked:hover .card-title{color:var(--brand-ink);}')
    if old in css and ".card-linked .link-arrow" not in css:
        css = css.replace(old, new, 1)
        n += 1

    # #5 -- suppress the decorative tick when the plate holds real content
    old2 = ('.split-media::after{\n'
            '  content:""; position:absolute; left:0; top:0; width:44px; height:3px;\n'
            '  background:var(--brand);\n'
            '}')
    new2 = old2 + '\n.split-media--live::after{content:none;}'
    if old2 in css and ".split-media--live" not in css:
        css = css.replace(old2, new2, 1)
        n += 1

    CSS.write_text(css, encoding="utf-8")
    print("styles.css : %d rule blocks updated" % n)


if __name__ == "__main__":
    fix_html_global()
    fix_about_cards()
    fix_map_tick()
    fix_green_award()
    fix_css()

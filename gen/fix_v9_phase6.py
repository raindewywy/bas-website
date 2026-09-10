#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_phase6.py — REQUIREMENTS v9 · เฟส 6 (กล่องทั้งใบคลิกได้)
  REQ-A2      : index.html — คลิกที่ "รูป" ของ .story-row แล้วไปหน้าปลายทางได้จริง
  REQ-B2      : about.html — การ์ดผู้บริหาร 11 ใบลิงก์ไปหน้าประวัติ (reuse .leader-card)
  REQ-B3      : about.html — การ์ดภาควิชาชี้ anchor รายภาควิชา + ครอบ card-title ด้วย <a>
  REQ-C-DEAN1 : leadership.html — กล่องคณบดีคลิกได้ทั้งกล่อง ปุ่มภายในยังกดแยกได้
  REQ-D2      : student-life.html — .story-row 3 แถวเพิ่ม .link-arrow
  REQ-D3      : student-life.html — การ์ดกิจกรรม/แลกเปลี่ยน <div> -> <a> ทั้งใบ

ใช้ <a href> จริงทั้งหมด ไม่มี onClick navigation
รันซ้ำได้ (idempotent)
    python gen/fix_v9_phase6.py
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"

# ---------------------------------------------------------------- CSS ------
CSS_MARK = "/* == v9 phase 6 =="

# REQ-A2 — เดิม .link-arrow เป็น position:relative ทำให้ ::after{inset:0}
# คลุมแค่ตัวลิงก์เอง ไม่ใช่ทั้งแถว -> ทำให้ static เพื่อให้อ้าง .story-row (position:relative)
STORY_OLD = """.story-row .link-arrow{position:relative; z-index:1;}
.story-row .link-arrow::after{content:""; position:absolute; inset:0;}"""
STORY_NEW = """.story-row .link-arrow{position:static;}
.story-row .link-arrow::after{content:""; position:absolute; inset:0; z-index:3;}"""

CSS_BLOCK = """

/* == v9 phase 6 == REQ-A2 · REQ-C-DEAN1 =================================
   กล่องทั้งใบคลิกได้ — ใช้ stretched-link เดิมของโปรเจกต์ ไม่สร้างกลไกใหม่
   ===================================================================== */

/* ---- REQ-A2: คลิกที่รูปของ .story-row ได้จริง ------------------------ */
.story-row{ isolation:isolate; cursor:pointer; }
.story-row .story-media .media-img{ transition:transform var(--dur) var(--ease); }
.story-row:hover .story-media .media-img{ transform:scale(1.03); }
@media (prefers-reduced-motion:reduce){
  .story-row:hover .story-media .media-img{ transform:none; }
}

/* ---- REQ-C-DEAN1: กล่องคณบดีคลิกได้ทั้งกล่อง ------------------------- */
.leader-dean{ position:relative; isolation:isolate; }
.leader-dean .dean-link{ color:inherit; text-decoration:none; }
.leader-dean .dean-link::after{ content:""; position:absolute; inset:0; z-index:1; }
.leader-dean:hover .dean-link{ color:var(--brand-700); }
.leader-dean:focus-within{ outline:2px solid var(--focus); outline-offset:3px; }
.leader-dean .dean-link:focus-visible{ outline:none; }
/* ปุ่มรองในกล่องต้องยังกดแยกได้ ไม่ถูก overlay กิน */
.leader-dean .btn,
.leader-dean a[href^="mailto:"]{ position:relative; z-index:2; }
"""


def patch_css():
    s = CSS.read_text(encoding="utf-8")
    if CSS_MARK in s:
        print("  styles.css: patch เฟส 6 มีอยู่แล้ว — ข้าม")
        return
    if STORY_OLD not in s:
        sys.exit("!! หา rule .story-row .link-arrow เดิมไม่เจอ")
    s = s.replace(STORY_OLD, STORY_NEW, 1)
    s = s.rstrip("\n") + "\n" + CSS_BLOCK
    CSS.write_text(s, encoding="utf-8")
    print("  styles.css: REQ-A2 (hit-area รูป) + REQ-C-DEAN1")


# ------------------------------------------------------------- REQ-B2 ------
LEADERS = {
    "ดร.ณัฐินี ฐานะจาโร": "leader-natinee-thanajaro.html",
    "ผศ.ดร.จรินทร์ จารุเสน": "leader-jarin-jarusen.html",
    "ผศ.ดร.ภูธิป มีถาวรกุล": "leader-phutip-meethavornkul.html",
    "ผศ.ดร.กัลยกิตติ์ กีรติอังกูร": "leader-kanyakit-keeratiangkoon.html",
    "ผศ.ดร.เพชรรัตน์ จินต์นุพงศ์": "leader-phetcharat-jinnupong.html",
    "ดร.รสิตา สังข์บุญนาค": "leader-rasita-sangboonnak.html",
    "ผศ.ดร.กังวาน ยอดวิศิษฎ์ศักดิ์": "leader-kangwan-yodwisitsak.html",
    "รศ.ดร.วสันต์ สกุลกิจกาญจน์": "leader-wasan-sakulkijkarn.html",
    "ผศ.ดร.คมกริช นันทะโรจพงศ์": "leader-khomkrit-nantharojphong.html",
    "ดร.สยาม ประเสริฐกุล": "leader-siam-prasertkul.html",
    "ดร.จิรชัย หมื่นฤทธิ์": "leader-jirachai-muenlit.html",
}

# ------------------------------------------------------------- REQ-B3 ------
DEPARTMENTS = {
    "ภาควิชาการบัญชีและการเงิน": "departments.html#accounting-finance",
    "ภาควิชาการตลาดและการจัดการ": "departments.html#marketing-management",
    "ภาควิชาบริหารธุรกิจ": "departments.html#business-administration",
}


def patch_about():
    p = ROOT / "about.html"
    s = p.read_text(encoding="utf-8")

    # --- REQ-B2 ---
    if "leader-link" in s:
        print("  about.html: การ์ดผู้บริหารลิงก์แล้ว — ข้าม")
    else:
        s = s.replace('class="staff-card staff-name-a reveal"',
                      'class="staff-card leader-card staff-name-a reveal"')
        n = 0
        for name, href in LEADERS.items():
            old = '<div class="en-name th-body">%s</div>' % name
            new = ('<div class="en-name th-body">'
                   '<a class="leader-link" href="%s">%s</a></div>' % (href, name))
            if old in s:
                s = s.replace(old, new, 1)
                n += 1
            else:
                print(f"  !! about.html: หาชื่อ {name} ไม่เจอ")
        print(f"  about.html: REQ-B2 ลิงก์การ์ดผู้บริหาร {n}/11 ใบ")

    # --- REQ-B3 ---
    if "departments.html#accounting-finance" in s:
        print("  about.html: การ์ดภาควิชาแก้แล้ว — ข้าม")
    else:
        n = 0
        for dept, href in DEPARTMENTS.items():
            # ครอบ card-title ด้วย <a> (card-linked ใช้ .card-title a::after)
            old_title = '<h3 class="card-title bi-heading"><span class="bi-th th-body">%s</span>' % dept
            new_title = ('<h3 class="card-title bi-heading"><a href="%s">'
                         '<span class="bi-th th-body">%s</span>' % (href, dept))
            if old_title not in s:
                print(f"  !! about.html: หา card-title {dept} ไม่เจอ")
                continue
            i = s.index(old_title)
            j = s.index("</h3>", i)
            s = s[:i] + new_title + s[i + len(old_title):j] + "</a>" + s[j:]
            # ลิงก์ "ดูภาควิชา" ของการ์ดใบนี้ (ตัวถัดไปหลังหัวข้อ)
            k = s.index('<a class="link-arrow mt-3" href="departments.html">', i)
            s = (s[:k] + '<a class="link-arrow mt-3" href="%s">' % href
                 + s[k + len('<a class="link-arrow mt-3" href="departments.html">'):])
            n += 1
        print(f"  about.html: REQ-B3 การ์ดภาควิชา {n}/3 ใบ -> anchor รายภาควิชา")

    p.write_text(s, encoding="utf-8")


def patch_leadership():
    p = ROOT / "leadership.html"
    s = p.read_text(encoding="utf-8")
    if "dean-link" in s:
        print("  leadership.html: กล่องคณบดีลิงก์แล้ว — ข้าม")
        return
    m = re.search(r'(<div class="leader-dean-copy">\s*<h3 class="th-body"[^>]*>)([^<]+)(</h3>)', s)
    if not m:
        sys.exit("!! leadership.html: หา <h3> ชื่อคณบดีในกล่อง .leader-dean ไม่เจอ")
    name = m.group(2)
    slug = LEADERS.get(name.strip())
    if not slug:
        sys.exit(f"!! ไม่รู้จักคณบดี: {name}")
    s = (s[:m.start()] + m.group(1)
         + '<a class="dean-link" href="%s">%s</a>' % (slug, name)
         + m.group(3) + s[m.end():])
    p.write_text(s, encoding="utf-8")
    print(f"  leadership.html: REQ-C-DEAN1 กล่องคณบดี -> {slug}")


# ---------------------------------------------------------- REQ-D2/D3 ------
STORY_LINKS = [
    ("การแข่งขันเคสและโปรเจกต์ประยุกต์", "student-life.html#activities", "ดูกิจกรรมนิสิต"),
    ("ชมรมและสโมสรนิสิต", "student-life.html#activities", "ดูกิจกรรมนิสิต"),
    ("ชีวิตในและรอบแคมปัส", "student-life.html#facilities", "ดูสิ่งอำนวยความสะดวก"),
]

CARD_LINKS = {
    "ปฐมนิเทศและสัปดาห์ต้อนรับ": "news.html?cat=campus",
    "การแข่งขันเคสธุรกิจ": "news.html?cat=academic",
    "งานชมรมและสมัครสมาชิก": "news.html?cat=campus",
    "โอกาสแลกเปลี่ยนที่ประเทศเยอรมนี": "international.html",
    "Frankfurt School of Finance &amp; Management": "international.html",
    "Brokenshire College ประเทศฟิลิปปินส์": "international.html",
}


def patch_student_life():
    p = ROOT / "student-life.html"
    s = p.read_text(encoding="utf-8")

    # --- REQ-D2 ---
    if 'class="story-copy"><h3 class="th-body">การแข่งขันเคสและโปรเจกต์ประยุกต์' in s and "link-arrow" not in s.split("story-row")[1][:900]:
        pass
    n = 0
    for title, href, label in STORY_LINKS:
        i = s.find('<h3 class="th-body">%s</h3>' % title)
        if i < 0:
            continue
        j = s.index("</div></div>", i)          # ปิด .story-copy + .story-row
        if 'class="link-arrow"' in s[i:j]:
            continue
        link = ('<a class="link-arrow" href="%s">%s '
                '<i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>' % (href, label))
        s = s[:j] + link + s[j:]
        n += 1
    print(f"  student-life.html: REQ-D2 เพิ่ม .link-arrow {n}/3 แถว"
          if n else "  student-life.html: REQ-D2 มี .link-arrow แล้ว — ข้าม")

    # --- REQ-D3 : <div class="card reveal">…</div>  ->  <a class="card reveal" href>…</a>
    n = 0
    for title, href in CARD_LINKS.items():
        t = '<h3 class="card-title th-body">%s</h3>' % title
        i = s.find(t)
        if i < 0:
            print(f"  !! student-life.html: หาการ์ด {title} ไม่เจอ")
            continue
        start = s.rfind('<div class="card reveal">', 0, i)
        if start < 0:
            continue                      # แปลงเป็น <a> ไปแล้ว
        end = s.index("</div></div>", i) + len("</div></div>")
        card = s[start:end]
        new = ('<a class="card card-linked reveal" href="%s">' % href) + card[len('<div class="card reveal">'):-len("</div>")] + "</a>"
        s = s[:start] + new + s[end:]
        n += 1
    print(f"  student-life.html: REQ-D3 การ์ด <div> -> <a> {n}/6 ใบ"
          if n else "  student-life.html: REQ-D3 การ์ดเป็น <a> แล้ว — ข้าม")

    p.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    print("REQ-A2 · B2 · B3 · C-DEAN1 · D2 · D3")
    patch_css()
    patch_about()
    patch_leadership()
    patch_student_life()

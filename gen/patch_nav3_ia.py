# -*- coding: utf-8 -*-
"""
สถาปัตยกรรมเมนูที่อนุมัติแล้ว (BAS SWU — Navigation Requirements & Architecture)

- หลักสูตร: Undergraduate · GBM · Graduate Studies (MBA ภายนอก / PhD ภายใน) · 4+1
- นานาชาติ/แลกเปลี่ยน: ยกขึ้นเป็นเมนูระดับบนสุด — Exchange 3+1 (เส้นทาง GBM) · Collaboration
- แยก 3+1 (ปริญญาคู่ GBM) ออกจาก 4+1 (ตรีควบโท) ให้ชัดเจน
- MBA เป็นเว็บไซต์ภายนอก จึงมีสัญลักษณ์ลิงก์ภายนอก + target/rel
แก้ที่ไฟล์นี้ไฟล์เดียว มีผลกับทุกหน้า
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXT_ICON = ('<svg class="ext-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" aria-hidden="true"><path d="M14 5h5v5"/><path d="M19 5l-8 8"/>'
            '<path d="M18 14v5H5V6h5"/></svg>')

# (href, th, en, kind) — kind: "" ปกติ | "ext" ลิงก์ภายนอก | "sub" รายการย่อยใต้หัวข้อกลุ่ม
# ("group", label_th, label_en, "head") = หัวข้อกลุ่มในเมกะเมนู
ABOUT = [
    ("about.html#vision", "วิสัยทัศน์และพันธกิจ", "Vision &amp; Mission", ""),
    ("about.html#history", "ประวัติคณะ", "History", ""),
    ("leadership.html", "ผู้บริหาร", "Leadership", ""),
    ("departments.html", "ภาควิชา", "Departments", ""),
    ("faculty.html", "คณาจารย์และบุคลากร", "Faculty &amp; Staff", ""),
    ("honours.html", "Hall of Fame", "Faculty Awards &amp; Achievements", ""),
    ("green-award.html", "Green Award", "Green Award / Sustainability", ""),
    ("contact.html", "ติดต่อ และ ITA/คู่มือการปฏิบัติงาน", "Contact &amp; ITA / Work Manual", ""),
]
PROGRAMS = [
    ("programs.html", "หลักสูตรทั้งหมด", "All Programmes", ""),
    ("programs.html?level=undergraduate", "ปริญญาตรี (ภาษาไทย)", "Undergraduate", ""),
    ("program-detail.html?p=global-business-management", "GBM — การจัดการธุรกิจโลก",
     "Global Business Management (English-taught)", ""),
    ("group", "บัณฑิตศึกษา", "Graduate Studies", "head"),
    ("https://mba.swu.ac.th/", "MBA — บริหารธุรกิจมหาบัณฑิต",
     "Master of Business Administration — external site", "ext"),
    ("program-detail.html?p=phd", "PhD — ปรัชญาดุษฎีบัณฑิต",
     "Doctor of Philosophy in Business Administration for Society", "sub"),
    ("programs.html#plan41", "หลักสูตรตรีควบโท 4+1", "Bachelor + Master (4+1)", ""),
    ("programs.html#advisors", "ติดต่อที่ปรึกษาหลักสูตร", "Programme Advisors", ""),
]
INTERNATIONAL = [
    ("international.html", "ภาพรวมนานาชาติ", "International Overview", ""),
    ("international.html#exchange", "Exchange 3+1 — ปริญญาคู่",
     "3+1 Double Degree — GBM international pathway", ""),
    ("international.html#collaboration", "ความร่วมมือระหว่างประเทศ", "Collaboration &amp; Partners", ""),
]
STUDENT = [
    ("student-life.html", "ภาพรวมชีวิตนิสิต", "Student Life Overview", ""),
    ("student-life.html#activities", "กิจกรรมนิสิต", "Student Activities", ""),
    ("student-life.html#facilities", "สิ่งอำนวยความสะดวก", "Campus Facilities", ""),
    ("student-life.html#exchange", "โครงการแลกเปลี่ยน", "Exchange &amp; Global Opportunities", ""),
]


def _a(href, th, en, kind, drawer=False):
    if kind == "head":
        return ('<p class="mega-head" role="presentation">%s <span>/ %s</span></p>' % (th, en)
                if not drawer else
                '<p class="drawer-sub-head">%s <span>/ %s</span></p>' % (th, en))
    cls = []
    attrs = ""
    if kind == "sub":
        cls.append("is-sub")
    if kind == "ext":
        cls.append("is-sub")
        cls.append("is-ext")
        attrs = ' target="_blank" rel="noopener noreferrer"'
    cls_attr = ' class="%s"' % " ".join(cls) if cls else ""
    tail = ""
    if kind == "ext":
        tail = EXT_ICON + '<span class="visually-hidden"> (เปิดเว็บไซต์ภายนอกในแท็บใหม่ / opens external site in a new tab)</span>'
    if drawer:
        return ('<a href="%s"%s%s>%s%s <span style="color:var(--muted)">/ %s</span></a>'
                % (href, cls_attr, attrs, th, tail, en))
    return ('<a href="%s"%s%s><span class="th-body">%s</span><span class="en">%s</span>%s</a>'
            % (href, cls_attr, attrs, th, en, tail))


def mega(items):
    return "".join(_a(*it) for it in items)


def drawer_sub(items):
    return "".join(_a(*it, drawer=True) for it in items)


def nav_list():
    def group(key, href, label, items):
        return (
            '<li class="nav-item" data-key="%s"><a class="nav-link" href="%s" aria-haspopup="true">'
            '<span class="th-body">%s</span><span class="chev" aria-hidden="true"></span></a>'
            '<div class="mega">%s</div></li>' % (key, href, label, mega(items))
        )

    return (
        '<ul class="nav-list">'
        '<li class="nav-item" data-key="home"><a class="nav-link" href="index.html">'
        '<span class="th-body">หน้าแรก</span></a></li>'
        + group("about", "about.html", "เกี่ยวกับคณะ", ABOUT)
        + group("programs", "programs.html", "หลักสูตร", PROGRAMS)
        + group("international", "international.html", "นานาชาติ", INTERNATIONAL)
        + group("student-life", "student-life.html", "ชีวิตนิสิต", STUDENT)
        + '<li class="nav-item" data-key="admissions"><a class="nav-link" href="admissions.html">'
        '<span class="th-body">การรับสมัคร</span></a></li>'
        "</ul>"
    )


def drawer_body():
    def group(label, en, items):
        return (
            '<li class="drawer-item"><button type="button" aria-expanded="false">'
            '<span class="th-body">%s <span style="color:var(--muted);font-weight:400;">/ %s</span></span>'
            '<span class="chev" aria-hidden="true"></span></button>'
            '<div class="drawer-sub">%s</div></li>' % (label, en, drawer_sub(items))
        )

    return (
        '<ul class="drawer-body">'
        '<li class="drawer-item"><a href="index.html"><span class="th-body">หน้าแรก '
        '<span style="color:var(--muted);font-weight:400;">/ Home</span></span></a></li>'
        + group("เกี่ยวกับคณะ", "About", ABOUT)
        + group("หลักสูตร", "Programmes", PROGRAMS)
        + group("นานาชาติ", "International &amp; Exchange", INTERNATIONAL)
        + group("ชีวิตนิสิต", "Student Life", STUDENT)
        + '<li class="drawer-item"><a href="admissions.html"><span class="th-body">การรับสมัคร '
        '<span style="color:var(--muted);font-weight:400;">/ Admissions</span></span></a></li>'
        '<li class="drawer-item"><a href="news.html"><span class="th-body">ข่าวและกิจกรรม '
        '<span style="color:var(--muted);font-weight:400;">/ News &amp; Events</span></span></a></li>'
        "</ul>"
    )


NAV = nav_list()
DRAWER = drawer_body()

ACTIVE_BY_FILE = {"international.html": "international"}

for path in sorted(glob.glob(str(ROOT / "*.html"))):
    p = Path(path)
    s = p.read_text(encoding="utf-8")

    m = re.search(r'<li class="nav-item current" data-key="([a-z-]+)">', s)
    active = m.group(1) if m else None
    active = ACTIVE_BY_FILE.get(p.name, active)
    if p.name in ("news.html", "news-detail.html"):
        active = None

    nav = NAV
    if active:
        nav = nav.replace(
            '<li class="nav-item" data-key="%s">' % active,
            '<li class="nav-item current" data-key="%s">' % active,
            1,
        )

    s2 = re.sub(r'<ul class="nav-list">.*?</ul>', lambda _: nav, s, count=1, flags=re.S)
    s2 = re.sub(r'<ul class="drawer-body">.*?</ul>', lambda _: DRAWER, s2, count=1, flags=re.S)
    if s2 != s:
        p.write_text(s2, encoding="utf-8")
        print("nav IA:", p.name)

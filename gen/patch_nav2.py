# -*- coding: utf-8 -*-
"""
ปรับโครงเมนูตามโน้ตประชุม (แก้จุดเดียว มีผลทุกหน้า)

- เอา "ข่าวและกิจกรรม" ออกจากแถบเมนูหลัก (ตามที่ประชุม + อ้างอิง swu.ac.th
  ที่ไม่มีเมนูข่าวระดับบนสุด) แต่ยังคงหน้ารวมข่าวไว้ เข้าถึงได้จาก
  section หน้าแรก / footer / ผลค้นหา
- เพิ่มใต้ "เกี่ยวกับคณะ": เกียรติภูมิ BAS · Green Award · นานาชาติ
- เพิ่มใต้ "หลักสูตร": หลักสูตร 4+1 · ติดต่อที่ปรึกษาหลักสูตร
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ABOUT = [
    ("about.html#vision", "วิสัยทัศน์และพันธกิจ", "Vision &amp; Mission"),
    ("about.html#history", "ประวัติคณะ", "History"),
    ("leadership.html", "ผู้บริหาร", "Leadership"),
    ("departments.html", "ภาควิชา", "Departments"),
    ("faculty.html", "คณาจารย์และบุคลากร", "Faculty &amp; Staff"),
    ("honours.html", "เกียรติภูมิ BAS", "Honours &amp; Awards"),
    ("green-award.html", "Green Award", "Green Award"),
    ("international.html", "นานาชาติ", "International"),
    ("contact.html", "ติดต่อ และ ITA/คู่มือการปฏิบัติงาน", "Contact &amp; ITA / Work Manual"),
]
PROGRAMS = [
    ("programs.html", "หลักสูตรทั้งหมด", "All Programs"),
    ("programs.html?level=undergraduate", "ปริญญาตรี ภาษาไทย", "Undergraduate — Thai Curriculum"),
    ("program-detail.html?p=global-business-management", "หลักสูตรภาษาอังกฤษ", "Global Business Management (English)"),
    ("programs.html?level=graduate", "ปริญญาโท-เอก", "Graduate — MBA &amp; PhD"),
    ("programs.html#plan41", "หลักสูตร 4+1", "Bachelor + Master (4+1)"),
    ("programs.html#advisors", "ติดต่อที่ปรึกษาหลักสูตร", "Programme Advisors"),
]
STUDENT = [
    ("student-life.html", "ภาพรวมชีวิตนิสิต", "Student Life Overview"),
    ("student-life.html#activities", "กิจกรรมนิสิต", "Student Activities"),
    ("student-life.html#facilities", "สิ่งอำนวยความสะดวก", "Campus Facilities"),
    ("student-life.html#exchange", "โครงการแลกเปลี่ยน", "Exchange &amp; Global Opportunities"),
]


def mega(items):
    return "".join(
        '<a href="%s"><span class="th-body">%s</span><span class="en">%s</span></a>' % it for it in items
    )


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
        + group("student-life", "student-life.html", "ชีวิตนิสิต", STUDENT)
        + '<li class="nav-item" data-key="admissions"><a class="nav-link" href="admissions.html">'
        '<span class="th-body">การรับสมัคร</span></a></li>'
        "</ul>"
    )


def drawer_sub(items):
    return "".join(
        '<a href="%s">%s <span style="color:var(--muted)">/ %s</span></a>' % it for it in items
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
        + group("หลักสูตร", "Programs", PROGRAMS)
        + group("ชีวิตนิสิต", "Student Life", STUDENT)
        + '<li class="drawer-item"><a href="admissions.html"><span class="th-body">การรับสมัคร '
        '<span style="color:var(--muted);font-weight:400;">/ Admissions</span></span></a></li>'
        '<li class="drawer-item"><a href="news.html"><span class="th-body">ข่าวและกิจกรรม '
        '<span style="color:var(--muted);font-weight:400;">/ News &amp; Events</span></span></a></li>'
        "</ul>"
    )


NAV = nav_list()
DRAWER = drawer_body()

for path in sorted(glob.glob(str(ROOT / "*.html"))):
    p = Path(path)
    s = p.read_text(encoding="utf-8")

    m = re.search(r'<li class="nav-item current" data-key="([a-z-]+)">', s)
    active = m.group(1) if m else None
    if p.name == "news.html" or p.name == "news-detail.html":
        active = None  # ข่าวไม่อยู่ในเมนูหลักแล้ว

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
        print("nav updated:", p.name)

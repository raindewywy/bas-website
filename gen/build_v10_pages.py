#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_v10_pages.py — v10: เติมหน้าที่ขาดจากเว็บต้นแบบ (bas / bas2)

สร้าง 7 หน้าใหม่ + เพิ่มเมนูหลัก "วิชาการและวิจัย" + เติม 2 section ใน about.html
เนื้อหาทุกบรรทัดอ้างจาก docs/content-audit-v10.md (ดึงจากเว็บต้นแบบจริง)

  academic.html            ภาพรวมวิชาการและวิจัย (hub) + UKPSF
  qa.html                  ประกันคุณภาพ — TQF / EdPEx / AUN-QA
  mou.html                 ความร่วมมือทางวิชาการ 4 กลุ่ม
  academic-calendar.html   ปฏิทินการศึกษา (PDF 3 ฉบับ)
  sustainability.html      ความยั่งยืน ESG 3 เสา
  student-services.html    บริการนิสิต 6 บริการ
  staff-deans-office.html  บุคลากรสำนักงานคณบดี 24 คน

reuse component เดิมทั้งหมด: .card · .honour-card · .advisor-card · .grid-3
.split · .edu-list · .stat-tile-v2 · .staff-grid · .section-head · .page-hero--image

รันซ้ำได้ (idempotent) — จากนั้นรัน  python build.py
    python gen/build_v10_pages.py
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates"
PG = TPL / "pages"
PAGES_JSON = ROOT / "data" / "pages.json"

E = "https://"


def crumb(*parts):
    """parts = (ข้อความ, href|None) ตัวสุดท้ายเป็นหน้าปัจจุบัน"""
    out = ['<nav class="breadcrumb wrap" aria-label="เส้นทางหน้าเว็บ">']
    sep = '<span class="sep" aria-hidden="true">/</span>'
    for i, (label, href) in enumerate(parts):
        if i:
            out.append(sep)
        out.append(f'<a href="{href}">{label}</a>' if href
                   else f'<span aria-current="page">{label}</span>')
    return "".join(out) + "</nav>"


def hero(img, eyebrow, th, en, lede):
    return (
        f'<section class="page-hero page-hero--image">'
        f'<img class="hero-bg" src="assets/media/{img}" alt="" aria-hidden="true" '
        f'loading="eager" decoding="async" fetchpriority="high"><div class="wrap">'
        f'<p class="eyebrow th-body">{eyebrow}</p>'
        f'<h1 class="bi-heading"><span class="bi-th th-body">{th}</span>'
        f'<span class="bi-en">{en}</span></h1>'
        f'<p class="lede th-body">{lede}</p></div></section>'
    )


def head(eyebrow, th, en, lede=""):
    l = f'<p class="lede th-body">{lede}</p>' if lede else ""
    return (f'<div class="section-head reveal"><div><p class="eyebrow">{eyebrow}</p>'
            f'<h2 class="bi-heading"><span class="bi-th th-body">{th}</span>'
            f'<span class="bi-en">{en}</span></h2>{l}</div></div>')


def hcard(title, en, body):
    return (f'<div class="honour-card reveal"><h3 class="th-body">{title}</h3>'
            f'<p class="en" style="color:var(--muted);font-size:.8rem;margin-bottom:.5rem;">{en}</p>'
            f'<p>{body}</p></div>')


def ext(href, label, note=""):
    n = f'<span class="en">{note}</span>' if note else ""
    return (f'<a class="link-arrow" href="{href}" target="_blank" rel="noopener noreferrer">{label} '
            f'<i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>'
            f'<span class="visually-hidden"> (เปิดเว็บไซต์ภายนอกในแท็บใหม่)</span></a>{n}')


def page(body):
    return '{% extends "base.html" %}\n{% block main %}\n' + body + "\n{% endblock %}\n"


# =========================================================== 1. academic ====
UKPSF_LEVELS = [
    ("Senior Fellow", "SFHEA", 1, "ระดับสูงสุด สำหรับผู้นำด้านการเรียนการสอนที่มีผลต่อผู้อื่นในวงกว้าง"),
    ("Fellow", "FHEA", 10, "ระดับหลัก สำหรับอาจารย์ที่รับผิดชอบการสอนและสนับสนุนการเรียนรู้อย่างเต็มรูปแบบ"),
    ("Associate Fellow", "AFHEA", 1, "ระดับเริ่มต้น สำหรับผู้เริ่มมีบทบาทด้านการสอนและสนับสนุนการเรียนรู้"),
]

ACADEMIC = page(
    crumb(("หน้าแรก", "index.html"), ("วิชาการและวิจัย", None))
    + hero("academic-research.jpg", "วิชาการและวิจัย", "วิชาการและวิจัย",
           "Academic &amp; Research",
           "มาตรฐานการเรียนการสอน การประกันคุณภาพ ความร่วมมือทางวิชาการ และข้อมูลสำหรับการวางแผนการศึกษา")
    + '<section class="section"><div class="wrap">'
    + head("ภาพรวม", "งานวิชาการของคณะ", "What We Do",
           "คณะดูแลคุณภาพการเรียนการสอนผ่านสามเสาหลัก — การรับรองสมรรถนะอาจารย์ การประกันคุณภาพตามเกณฑ์สากล และเครือข่ายความร่วมมือกับหน่วยงานภายนอก")
    + '<div class="grid-3 mt-5">'
    + hcard("การรับรองสมรรถนะอาจารย์", "UKPSF",
            "อาจารย์ของคณะได้รับการรับรองตามกรอบมาตรฐานวิชาชีพของสหราชอาณาจักรแล้ว 12 คน")
    + hcard("ประกันคุณภาพการศึกษา", "TQF · EdPEx · AUN-QA",
            "ประเมินคุณภาพสามระดับ ตั้งแต่มาตรฐานหลักสูตรไปจนถึงเกณฑ์ระดับอาเซียน")
    + hcard("ความร่วมมือทางวิชาการ", "MOU",
            "ลงนามบันทึกข้อตกลงกับสถาบันการศึกษา หน่วยงานรัฐ และภาคเอกชนทั้งในและต่างประเทศ")
    + "</div>"
    + '<div class="grid-3 mt-4">'
    + '<div class="card card-linked reveal"><div class="card-body">'
      '<span class="card-tag th-body">ประกันคุณภาพ</span>'
      '<h3 class="card-title th-body"><a href="qa.html">ระบบประกันคุณภาพการศึกษา</a></h3>'
      '<p class="card-desc th-body">เกณฑ์ที่คณะใช้ในแต่ละระดับ และรอบการประเมินปัจจุบัน</p>'
      '<a class="link-arrow mt-3" href="qa.html">ดูรายละเอียด <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>'
      "</div></div>"
    + '<div class="card card-linked reveal"><div class="card-body">'
      '<span class="card-tag th-body">MOU</span>'
      '<h3 class="card-title th-body"><a href="mou.html">โครงการความร่วมมือทางวิชาการ</a></h3>'
      '<p class="card-desc th-body">หน่วยงานพันธมิตรทั้ง 4 กลุ่มที่คณะลงนามความร่วมมือด้วย</p>'
      '<a class="link-arrow mt-3" href="mou.html">ดูรายชื่อพันธมิตร <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>'
      "</div></div>"
    + '<div class="card card-linked reveal"><div class="card-body">'
      '<span class="card-tag th-body">ปฏิทิน</span>'
      '<h3 class="card-title th-body"><a href="academic-calendar.html">ปฏิทินการศึกษา</a></h3>'
      '<p class="card-desc th-body">กำหนดการเปิด-ปิดภาคเรียน ลงทะเบียน และสอบ ทุกระดับการศึกษา</p>'
      '<a class="link-arrow mt-3" href="academic-calendar.html">เปิดปฏิทิน <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>'
      "</div></div>"
    + "</div></div></section>"
    # ---- UKPSF ----
    + '<section class="section" id="ukpsf" style="background:var(--paper-dim);"><div class="wrap">'
    + head("การรับรองสมรรถนะอาจารย์", "UKPSF", "UK Professional Standards Framework",
           "การรับรองสมรรถนะวิชาชีพอาจารย์ตามกรอบมาตรฐานของสหราชอาณาจักร ปัจจุบันคณะมีผู้ได้รับการรับรองแล้ว 12 คน")
    + '<div class="grid-3 mt-5">'
    + "".join(
        f'<div class="honour-card reveal"><h3 class="th-body">{th}</h3>'
        f'<p class="en" style="color:var(--muted);font-size:.8rem;margin-bottom:.5rem;">{en}</p>'
        f'<p class="th-body" style="font-family:var(--font-mono);font-size:1.6rem;font-weight:700;'
        f'color:var(--brand-700);line-height:1.1;">{n} <span style="font-size:.9rem;font-weight:600;">คน</span></p>'
        f'<p style="margin-top:.5rem;">{d}</p></div>'
        for th, en, n, d in UKPSF_LEVELS)
    + "</div>"
    + '<div class="notice th-body mt-5"><span>รายชื่อผู้ได้รับการรับรองรายบุคคลอยู่ระหว่างรวบรวมจากคณะ '
      "เว็บไซต์ต้นฉบับเผยแพร่เป็นรูปภาพจึงยังไม่มีข้อมูลเป็นข้อความ</span></div>"
    + "</div></section>"
    # ---- ลิงก์ภายนอก ----
    + '<section class="section"><div class="wrap">'
    + head("แหล่งข้อมูลภายนอก", "ระบบและเอกสารที่เกี่ยวข้อง", "External Resources")
    + '<div class="grid-3 mt-5">'
    + '<div class="advisor-card reveal"><h3 class="th-body">ค่าธรรมเนียมการศึกษา</h3>'
      '<p class="en" style="color:var(--muted);font-size:.78rem;">Tuition Fees</p>'
      '<p class="th-body" style="margin-top:.5rem;">อัตราค่าธรรมเนียมของทุกหลักสูตร เผยแพร่โดยส่วนส่งเสริมและบริการการศึกษา มศว</p>'
      '<p style="margin-top:.6rem;">' + ext("https://academic.swu.ac.th/tuition", "academic.swu.ac.th/tuition") + "</p></div>"
    + '<div class="advisor-card reveal"><h3 class="th-body">วารสารบริหารธุรกิจเพื่อสังคม</h3>'
      '<p class="en" style="color:var(--muted);font-size:.78rem;">BASSBJ Journal</p>'
      '<p class="th-body" style="margin-top:.5rem;">วารสารวิชาการของคณะ เผยแพร่ผ่านระบบ ThaiJO</p>'
      '<p style="margin-top:.6rem;">' + ext("https://so17.tci-thaijo.org/index.php/BASSBJ", "so17.tci-thaijo.org") + "</p></div>"
    + '<div class="advisor-card reveal"><h3 class="th-body">E-Learning</h3>'
      '<p class="en" style="color:var(--muted);font-size:.78rem;">e-SWUBAS</p>'
      '<p class="th-body" style="margin-top:.5rem;">ระบบการเรียนออนไลน์ของคณะ</p>'
      '<p style="margin-top:.6rem;">' + ext("https://www.e-swubas.com/", "e-swubas.com") + "</p></div>"
    + "</div></div></section>"
)

# ================================================================= 2. qa ====
QA_LEVELS = [
    ("มาตรฐานหลักสูตร", "TQF", "Thai Qualifications Framework",
     "บริหารจัดการหลักสูตรตามเกณฑ์มาตรฐาน ทั้งด้านการออกแบบหลักสูตรและการดำเนินการจัดการเรียนการสอน", ""),
    ("ระดับคณะ", "EdPEx", "Education Criteria for Performance Excellence",
     "ประเมินตามเกณฑ์คุณภาพการศึกษาเพื่อการดำเนินการที่เป็นเลิศ", "รอบ พ.ศ. 2567–2570"),
    ("ระดับหลักสูตร (สากล)", "AUN-QA", "ASEAN University Network Quality Assurance",
     "ประเมินหลักสูตรตามมาตรฐานเครือข่ายมหาวิทยาลัยอาเซียน", ""),
]

QA = page(
    crumb(("หน้าแรก", "index.html"), ("วิชาการและวิจัย", "academic.html"), ("ประกันคุณภาพ", None))
    + hero("banner-ita.jpg", "วิชาการและวิจัย", "ประกันคุณภาพการศึกษา",
           "Quality Assurance",
           "ระบบประเมินคุณภาพการศึกษาของคณะ ครอบคลุมตั้งแต่ระดับหลักสูตรจนถึงระดับคณะ")
    + '<section class="section"><div class="wrap">'
    + head("ระบบประเมิน", "เกณฑ์ที่คณะใช้", "Assessment Frameworks",
           "คณะใช้ระบบประเมินคุณภาพสามระดับควบคู่กัน เพื่อให้ครอบคลุมทั้งมาตรฐานภายในประเทศและมาตรฐานสากล")
    + '<div class="grid-3 mt-5">'
    + "".join(
        f'<div class="honour-card reveal"><h3 class="th-body">{name}</h3>'
        f'<p class="en" style="color:var(--muted);font-size:.8rem;margin-bottom:.5rem;">{full}</p>'
        f'<p class="th-body" style="font-family:var(--font-mono);font-size:1.35rem;font-weight:700;'
        f'color:var(--brand-700);line-height:1.2;">{code}</p>'
        f'<p style="margin-top:.5rem;">{desc}</p>'
        + (f'<p class="card-meta th-body mt-2">{extra}</p>' if extra else "")
        + "</div>"
        for name, code, full, desc, extra in QA_LEVELS)
    + "</div>"
    + '<div class="notice th-body mt-5"><span><strong>เอกสารผลการประเมิน</strong> — รายงานการประเมินตนเอง (SAR) '
      "และผลการประเมินรายปียังไม่ได้เผยแพร่เป็นไฟล์บนเว็บไซต์ของคณะ "
      "หากต้องการเอกสารฉบับเต็มติดต่องานนโยบายและแผน สำนักงานคณบดี</span></div>"
    + '<p class="th-body mt-4">ผู้รับผิดชอบงานประกันคุณภาพ: <strong>นางสาวธัญชนก บุญแปลง</strong> '
      "· งานนโยบายและแผน · โทรภายใน 11757 · "
      '<a href="mailto:thanchanokb@g.swu.ac.th">thanchanokb@g.swu.ac.th</a></p>'
    + "</div></section>"
)

# ================================================================ 3. mou ====
MOU_GROUPS = [
    ("สถาบันการศึกษาต่างประเทศ", "International Institutions", 4,
     [("skku.png", "Sungkyunkwan University (SKKU)", "สาธารณรัฐเกาหลี"),
      ("meiji-university.png", "Meiji University", "ญี่ปุ่น")]),
    ("สถาบันการศึกษาในประเทศ", "Domestic Institutions", 7,
     [("kmitl.png", "สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง", ""),
      ("swu-social-sciences.png", "คณะสังคมศาสตร์ มหาวิทยาลัยศรีนครินทรวิโรฒ", ""),
      ("rajinibon-school.png", "โรงเรียนราชินีบน", ""),
      ("sarasas-witaed-nakhonpathom.png", "โรงเรียนสารสาสน์วิเทศนครปฐม", "")]),
    ("หน่วยงานภาครัฐ", "Government Agencies", 8,
     [("ocsc.png", "สำนักงาน ก.พ.", ""),
      ("nrct.png", "สำนักงานการวิจัยแห่งชาติ (วช.)", ""),
      ("nia.png", "สำนักงานนวัตกรรมแห่งชาติ (NIA)", ""),
      ("etda.png", "สำนักงานพัฒนาธุรกรรมทางอิเล็กทรอนิกส์ (ETDA)", ""),
      ("set.png", "ตลาดหลักทรัพย์แห่งประเทศไทย (SET)", ""),
      ("gsb.png", "ธนาคารออมสิน", "")]),
    ("หน่วยงานภาคเอกชน", "Private Sector", 9,
     [("tax-auditor-association.png", "สมาคมผู้สอบบัญชีภาษีอากรแห่งประเทศไทย", ""),
      ("flowaccount.png", "FlowAccount", ""),
      ("finansia.png", "Finansia", ""),
      ("big-c-retail.png", "Big C Retail", ""),
      ("staybridge-suites.png", "Staybridge Suites", ""),
      ("soho-hospitality.png", "SOHO Hospitality", ""),
      ("the-blacksmith.png", "The Blacksmith", ""),
      ("nise.png", "NISE", "")]),
]


def mou_group(th, en, total, items):
    cards = "".join(
        f'<div class="card reveal"><div class="card-media" style="aspect-ratio:16/9;display:flex;'
        f'align-items:center;justify-content:center;padding:var(--space-4);background:var(--surface);">'
        f'<img src="assets/media/partners/{f}" alt="{alt}" loading="lazy" decoding="async" '
        f'style="max-height:72px;max-width:100%;width:auto;object-fit:contain;"></div>'
        f'<div class="card-body"><h3 class="card-title th-body" style="font-size:1rem;">{alt}</h3>'
        + (f'<p class="card-meta th-body">{note}</p>' if note else "")
        + "</div></div>"
        for f, alt, note in items)
    missing = total - len(items)
    note = ("" if missing <= 0 else
            f'<p class="card-meta th-body mt-3">เว็บไซต์ต้นฉบับระบุกลุ่มนี้ทั้งหมด {total} แห่ง '
            f"— แสดงได้ {len(items)} แห่ง อีก {missing} แห่งอยู่ระหว่างขอไฟล์โลโก้และชื่อจากคณะ</p>")
    return (f'<div class="leader-group"><div class="leader-group-head">'
            f'<h2 class="th-body">{th}</h2><span class="en">{en}</span></div>'
            f'<div class="grid-3 mt-4">{cards}</div>{note}</div>')


MOU = page(
    crumb(("หน้าแรก", "index.html"), ("วิชาการและวิจัย", "academic.html"),
          ("ความร่วมมือทางวิชาการ", None))
    + hero("banner-mou.jpg", "วิชาการและวิจัย", "โครงการความร่วมมือทางวิชาการ",
           "Academic Collaboration &amp; MOU",
           "คณะลงนามบันทึกข้อตกลงความร่วมมือกับหน่วยงานต่าง ๆ เพื่อส่งเสริมและสนับสนุนให้นิสิตได้รับความรู้ ทักษะ และประสบการณ์ทางวิชาชีพ")
    + '<section class="section"><div class="wrap">'
    + "".join(mou_group(*g) for g in MOU_GROUPS)
    + "</div></section>"
)

# =================================================== 4. academic-calendar ====
CALENDARS = [
    ("ปฏิทินการศึกษา ระดับปริญญาตรี", "Undergraduate Academic Calendar", "ปีการศึกษา 2569",
     "วันเปิดและปิดภาคเรียน ช่วงเวลาการลงทะเบียนเรียน วันสอบ และกำหนดการทางวิชาการที่เกี่ยวข้อง",
     "https://academic.swu.ac.th/Portals/62/files/%E0%B8%9B%E0%B8%8F%E0%B8%B4%E0%B8%97%E0%B8%B4%E0%B8%99%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%A8%E0%B8%B6%E0%B8%81%E0%B8%A9%E0%B8%B2/%E0%B8%9B%E0%B8%8F%E0%B8%B4%E0%B8%97%E0%B8%B4%E0%B8%99%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%A8%E0%B8%B6%E0%B8%81%E0%B8%A9%E0%B8%B2%202569.pdf"),
    ("ปฏิทินการศึกษา ระดับบัณฑิตศึกษา", "Graduate Academic Calendar", "บัณฑิตวิทยาลัย มศว",
     "กำหนดการสำคัญของบัณฑิตวิทยาลัยสำหรับนิสิตระดับปริญญาโทและปริญญาเอก",
     "http://grad.swu.ac.th/SWU.BACKEND/fileupload/BANNER/00615/027be228-a0bc-435a-afd9-9c897c676767.pdf"),
    ("SWU Academic Calendar", "English Version", "Academic Year 2025",
     "ปฏิทินการศึกษาฉบับภาษาอังกฤษสำหรับหลักสูตรระดับปริญญาตรี เผยแพร่โดยส่วนวิเทศสัมพันธ์ฯ",
     "https://irco.op.swu.ac.th/Portals/29/Documents/Calendar/Academic%20Calendar%202025%20for%20Bachelor%20Degree.pdf"),
]

CALENDAR = page(
    crumb(("หน้าแรก", "index.html"), ("วิชาการและวิจัย", "academic.html"), ("ปฏิทินการศึกษา", None))
    + hero("banner-program.jpg", "วิชาการและวิจัย", "ปฏิทินการศึกษา",
           "Academic Calendar",
           "กำหนดการเปิด-ปิดภาคเรียน การลงทะเบียน และการสอบของแต่ละระดับการศึกษา")
    + '<section class="section"><div class="wrap">'
    + head("เอกสาร", "ปฏิทินที่เผยแพร่", "Published Calendars",
           "ปฏิทินการศึกษาเป็นเอกสารกลางของมหาวิทยาลัย เปิดจากเว็บไซต์ต้นทางเพื่อให้ได้ฉบับล่าสุดเสมอ")
    + '<div class="grid-3 mt-5">'
    + "".join(
        f'<div class="card card-linked reveal"><div class="card-body">'
        f'<span class="card-tag th-body">{tag}</span>'
        f'<h3 class="card-title th-body">{th}</h3>'
        f'<p class="card-meta th-body">{en}</p>'
        f'<p class="card-desc th-body mt-2">{desc}</p>'
        f'<p class="mt-3">' + ext(url, "เปิดไฟล์ PDF") + "</p></div></div>"
        for th, en, tag, desc, url in CALENDARS)
    + "</div>"
    + '<div class="notice th-body mt-5"><span>ไฟล์ทั้งหมดโฮสต์อยู่บนเว็บไซต์ของมหาวิทยาลัย '
      "หากลิงก์ใดเปิดไม่ได้แปลว่ามีการเผยแพร่ฉบับใหม่ทับ — แจ้งงานบริการการศึกษาเพื่ออัปเดตลิงก์</span></div>"
    + "</div></section>"
)

# ==================================================== 5. sustainability =====
ESG_STATS = [
    ("fa-users", "955", "ผู้เข้าร่วมกิจกรรม", "Participants"),
    ("fa-bolt", "12,201", "จำนวน action", "Actions logged"),
    ("fa-building-ngo", "28", "กิจกรรมองค์กร", "Organisational activities"),
    ("fa-leaf", "18.80", "kg CO₂ eq ที่ลดได้", "CO₂ reduced"),
    ("fa-star", "20,711", "คะแนนรวม", "Total points"),
]

SE_TRAINING = [
    ("ภาษีสำหรับผู้ประกอบการวัยเกษียณ",
     "ให้ความรู้ด้านภาษีและการวางแผนการเงินสำหรับผู้ประกอบการวัยเกษียณ"),
    ("การพัฒนาองค์กร ESG",
     "ยกระดับองค์กรวิสาหกิจเพื่อสังคมให้เติบโตอย่างยั่งยืนตามแนวทาง ESG"),
    ("เตรียมความพร้อมผู้ประกอบการ",
     "พัฒนาทักษะที่จำเป็นสำหรับผู้ประกอบการรุ่นใหม่"),
]

SUSTAINABILITY = page(
    crumb(("หน้าแรก", "index.html"), ("เกี่ยวกับคณะ", "about.html"), ("ความยั่งยืน", None))
    + hero("activity-community.jpg", "เกี่ยวกับคณะ", "ความยั่งยืน",
           "Sustainability &amp; ESG",
           "นโยบายและการดำเนินงานด้านความยั่งยืนของคณะ ครอบคลุมสามเสาหลัก สิ่งแวดล้อม สังคม และธรรมาภิบาล")
    # ---- Environmental ----
    + '<section class="section" id="environmental"><div class="wrap">'
    + head("เสาที่ 1", "สิ่งแวดล้อม", "Environmental",
           "ลดผลกระทบต่อสิ่งแวดล้อมจากการดำเนินงานของคณะ ตั้งแต่การใช้ทรัพยากรในสำนักงานจนถึงกิจกรรมร่วมกับนิสิตและบุคลากร")
    + '<div class="grid-3 mt-5">'
    + hcard("กิจกรรมทิ้งขยะอิเล็กทรอนิกส์", "สิงหาคม 2568",
            "เปิดจุดรับขยะอิเล็กทรอนิกส์ให้นิสิตและบุคลากรนำมาทิ้งอย่างถูกวิธี")
    + hcard("BAS SWU × ECO LIFE", "รางวัล ESG STAR",
            "โครงการร่วมกับ ECO LIFE พร้อมประกาศรางวัล ESG STAR เพื่อยกย่องแนวทางความยั่งยืน")
    + hcard("สำนักงานสีเขียว", "Green Office 2568",
            "ออกแบบและใช้งานสำนักงานที่ช่วยประหยัดพลังงาน ตามเกณฑ์สำนักงานสีเขียว 6 หมวด")
    + "</div>"
    + '<div class="split mt-5"><div class="split-copy reveal">'
      '<h3 class="th-body" style="font-size:1.05rem;">นโยบาย Green Meetings</h3>'
      '<p class="th-body mt-2" style="color:var(--muted);">ประชุมในรูปแบบ e-Meeting และเลือกใช้วัสดุที่เป็นมิตรต่อสิ่งแวดล้อม '
      "เพื่อลดการใช้กระดาษและการเดินทาง</p></div>"
      '<div class="split-copy reveal"><h3 class="th-body" style="font-size:1.05rem;">มาตรการที่ดำเนินการ</h3>'
      '<ul class="edu-list th-body mt-3">'
      "<li>กำหนดนโยบายและเป้าหมายด้านสิ่งแวดล้อมของคณะ</li>"
      "<li>บันทึกปริมาณการใช้น้ำ ไฟฟ้า และกระดาษอย่างต่อเนื่อง</li>"
      "<li>วัดและลดการปล่อยก๊าซเรือนกระจก</li>"
      "</ul></div></div>"
    + '<p class="th-body mt-5"><a class="link-arrow" href="green-award.html">'
      'ดูรายละเอียดสำนักงานสีเขียวและเกณฑ์ 6 หมวด <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p>'
    + "</div></section>"
    # ---- Social ----
    + '<section class="section" id="social" style="background:var(--paper-dim);"><div class="wrap">'
    + head("เสาที่ 2", "สังคม", "Social",
           "นำความเชี่ยวชาญด้านบริหารธุรกิจไปสร้างผลกระทบเชิงบวกต่อสังคม ผ่านหลักสูตรอบรมและกิจกรรมร่วมกับชุมชน")
    + '<h3 class="th-body mt-5" style="font-size:1.05rem;">SWU SE TRAINING — หลักสูตรอบรมเพื่อสังคม 3 หลักสูตร</h3>'
    + '<div class="grid-3 mt-4">'
    + "".join(
        f'<div class="advisor-card reveal"><h3 class="th-body">{i+1}. {t}</h3>'
        f'<p class="th-body" style="margin-top:.5rem;color:var(--muted);">{d}</p></div>'
        for i, (t, d) in enumerate(SE_TRAINING))
    + "</div>"
    + '<h3 class="th-body mt-6" style="font-size:1.05rem;">ตัวชี้วัดกิจกรรม ESG</h3>'
    + '<div class="stat-band-v2 reveal mt-4"><div class="stat-grid-v2">'
    + "".join(
        f'<div class="stat-tile-v2 reveal"><span class="stat-ico" aria-hidden="true">'
        f'<i class="fa-solid {ico}" aria-hidden="true"></i></span>'
        f'<div class="value">{v}</div>'
        f'<div class="label th-body">{th}<span class="en">{en}</span></div></div>'
        for ico, v, th, en in ESG_STATS)
    + "</div></div>"
    + "</div></section>"
    # ---- Governance ----
    + '<section class="section" id="governance"><div class="wrap">'
    + head("เสาที่ 3", "ธรรมาภิบาล", "Governance",
           "ความโปร่งใสในการดำเนินงานและช่องทางตรวจสอบ")
    + '<div class="grid-3 mt-5">'
    + hcard("รายงานประจำปี", "Annual Report",
            "เผยแพร่ผลการดำเนินงานตามแผนปฏิบัติการของคณะเป็นประจำทุกปี")
    + hcard("ITA", "Integrity &amp; Transparency Assessment",
            "การส่งเสริมคุณธรรมและความโปร่งใสในการดำเนินงานของหน่วยงานภาครัฐ")
    + hcard("แผนป้องกันทุจริต", "ปีงบประมาณ 2568",
            "แผนปฏิบัติการป้องกันทุจริตและส่งเสริมคุณธรรมของคณะ")
    + "</div>"
    + '<p class="th-body mt-5">ช่องทางร้องเรียนและเอกสาร ITA ฉบับเต็มอยู่ที่ '
      '<a class="link-arrow" href="contact.html#ita">หน้าติดต่อคณะ <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p>'
    + '<p class="source-note th-body mt-5">ที่มาข้อมูล: '
    + ext("https://bas2.swu.ac.th/sustainability", "bas2.swu.ac.th/sustainability")
    + " · ตรวจสอบเมื่อ 10 กันยายน 2569</p>"
    + "</div></section>"
)

# ==================================================== 6. student-services ===
SERVICES = [
    ("กิจกรรมเสริมหลักสูตร", "Curricular Activities", "fa-calendar-check",
     "ระบบบันทึกกิจกรรมเสริมหลักสูตรของนิสิต มศว",
     "https://studentaffairs.op.swu.ac.th/activityrecord"),
    ("ทุนการศึกษา", "Scholarships", "fa-hand-holding-dollar",
     "ทุนการศึกษาสำหรับนิสิตคณะบริหารธุรกิจเพื่อสังคม", "https://bas.swu.ac.th/"),
    ("ประกันอุบัติเหตุสำหรับนิสิต", "Accident Insurance", "fa-shield-heart",
     "สิทธิและขั้นตอนการเคลมประกันอุบัติเหตุของนิสิต",
     "https://studentaffairs.op.swu.ac.th/Accident"),
    ("กองทุนกู้ยืมเพื่อการศึกษา", "Student Loan Fund", "fa-piggy-bank",
     "ข้อมูล กยศ. และขั้นตอนการยื่นกู้ยืมเพื่อการศึกษา",
     "https://studentaffairs.op.swu.ac.th/StudentLoanFund"),
    ("SWU DSS Center", "Disability Support Services", "fa-universal-access",
     "ศูนย์บริการสนับสนุนนิสิตพิการของมหาวิทยาลัย",
     "https://studentaffairs.op.swu.ac.th/dsscenter"),
    ("สโมสรนิสิตคณะบริหารธุรกิจเพื่อสังคม", "BAS Student Club", "fa-people-group",
     "ข่าวสารและกิจกรรมจากสโมสรนิสิตของคณะ",
     "https://www.facebook.com/SWUSMOBAS"),
]

SERVICES_PAGE = page(
    crumb(("หน้าแรก", "index.html"), ("ชีวิตนิสิต", "student-life.html"), ("บริการนิสิต", None))
    + hero("banner-student-support.jpg", "ชีวิตนิสิต", "บริการนิสิต",
           "Student Services",
           "ช่องทางและระบบสนับสนุนนิสิตตลอดช่วงเวลาที่ศึกษาอยู่กับคณะ")
    + '<section class="section"><div class="wrap">'
    + head("บริการ", "ระบบและช่องทางสนับสนุนนิสิต", "Services &amp; Support",
           "บริการส่วนใหญ่ดำเนินการโดยส่วนกิจการนิสิตของมหาวิทยาลัย เปิดจากระบบต้นทางเพื่อให้ได้ข้อมูลล่าสุดเสมอ")
    + '<div class="grid-3 mt-5">'
    + "".join(
        f'<div class="advisor-card reveal">'
        f'<h3 class="th-body"><i class="fa-solid {ico}" aria-hidden="true" '
        f'style="color:var(--brand-700);margin-right:.45rem;"></i>{th}</h3>'
        f'<p class="en" style="color:var(--muted);font-size:.78rem;">{en}</p>'
        f'<p class="th-body" style="margin-top:.5rem;">{d}</p>'
        f'<p style="margin-top:.6rem;">' + ext(url, "เปิดระบบ") + "</p></div>"
        for th, en, ico, d, url in SERVICES)
    + "</div>"
    + '<p class="th-body mt-5">สิ่งอำนวยความสะดวกภายในคณะและบรรยากาศแคมปัสดูได้ที่ '
      '<a class="link-arrow" href="student-life.html#facilities">ชีวิตนิสิต <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p>'
    + "</div></section>"
)

# ================================================= 7. staff-deans-office ====
STAFF = [
    ("งานบริหารและธุรการ", "Administration &amp; General Affairs", [
        ("นางสาวปฤษณา ทิพย์สุวรรณ", "หัวหน้างาน", "11749", "prisaha@g.swu.ac.th"),
        ("นายปกป้อง คุ้มไทย", "ทรัพยากรบุคคล", "11750", "pokpong@g.swu.ac.th"),
        ("นายยอดชาย ไทยประเสริฐ", "อาคารและสถานที่", "11749", "yoadchai@g.swu.ac.th"),
        ("นายจีระบุญ รอดกร", "โสตทัศนูปกรณ์", "11750", "jeraboon@g.swu.ac.th"),
        ("นายวริศพล อุปไมย์", "ประชาสัมพันธ์", "11749 · 02-169-1018", "warrispon@g.swu.ac.th"),
        ("นายอรรถพล บุญอุ้ม", "ยานพาหนะ", "11749", "atthapolb@g.swu.ac.th"),
    ]),
    ("งานบริการการศึกษา", "Academic Services", [
        ("นางสาวปุณยนุช เรือนโนวา", "หัวหน้างาน", "11756", "punyanut@g.swu.ac.th"),
        ("ว่าที่ ร.ต.หญิง สาวิตรี แก้วสุวรรณ์", "กิจการนิสิต", "11748", "sawitreeke@g.swu.ac.th"),
        ("นางสาวสุภาวดี หว่างเจริญศักดิ์", "วิจัย", "11754", "supawadeew@g.swu.ac.th"),
        ("นายพุทไธสงค์ สงฆ์ประชา", "บริการการศึกษา", "11756", "putthaisong@g.swu.ac.th"),
    ]),
    ("ผู้ประสานงานหลักสูตร — ปริญญาตรี", "Undergraduate Programme Coordinators", [
        ("นางสาวกมลทิพย์ ประสิทธิ์นราพันธุ์", "การตลาด · ธุรกิจระหว่างประเทศ", "11746 · 02-169-1014", "kamontip@g.swu.ac.th"),
        ("นายอุเทน กางกรณ์", "ท่องเที่ยวและการโรงแรม · ธุรกิจเพื่อสังคม", "15500 · 02-169-1013", "uten@g.swu.ac.th"),
        ("นางสาวธนิษฐา คำนุชนารถ", "บัญชี · การเงิน", "15500 · 02-169-1017", "tanittha@g.swu.ac.th"),
        ("นางสาวกัญญ์ณพัชญ์ สวัสดิ์ธนากุล", "การจัดการธุรกิจโลก (GBM)", "11756", "kannapats@g.swu.ac.th"),
    ]),
    ("ผู้ประสานงานหลักสูตร — บัณฑิตศึกษา", "Graduate Programme Coordinators", [
        ("นายกฤดินิธิ ไตรพิษ", "บริหารธุรกิจมหาบัณฑิต (MBA)", "15501 · 02-169-1016", "kritnithi@g.swu.ac.th"),
        ("นางสาวอรญา ไทยบุญมี", "ปรัชญาดุษฎีบัณฑิต (PhD)", "15501 · 02-169-1016", "orayat@g.swu.ac.th"),
    ]),
    ("งานคลังและพัสดุ", "Finance &amp; Procurement", [
        ("นางสาวศิรรัตน์ จิตรนพรัตน์", "หัวหน้างาน", "11755", "sirarut@g.swu.ac.th"),
        ("นางสาววัชราภรณ์ อักษรแหลม", "การเงินและบัญชี", "11752", "watcharaporna@g.swu.ac.th"),
        ("นายวิฑูร หรรษา", "พัสดุ", "11747", "witun@g.swu.ac.th"),
        ("นางสาวนิตยา โพธิ์เงิน", "พัสดุ", "11747 · 02-169-1015", "nittayaph@g.swu.ac.th"),
    ]),
    ("งานนโยบายและแผน", "Policy &amp; Planning", [
        ("นางสาวประภานิช ดวงเพ็ชร", "หัวหน้างาน", "11770", "prapun@g.swu.ac.th"),
        ("นางสาวธัญชนก บุญแปลง", "บริการวิชาการและประกันคุณภาพ", "11757", "thanchanokb@g.swu.ac.th"),
        ("นางสาวณันธภัท พรมดวง", "นโยบายและแผน", "11757", "aungsadan@g.swu.ac.th"),
        ("นางสาวอัญธิกา สัตยกิจกุล", "วิเทศสัมพันธ์และความร่วมมือ", "11770", "anthika@g.swu.ac.th"),
    ]),
]


def staff_group(th, en, people):
    rows = "".join(
        f'<div class="advisor-card reveal"><h3 class="th-body" style="font-size:1rem;">{name}</h3>'
        f'<p class="th-body" style="color:var(--muted);font-size:.88rem;margin-top:.2rem;">{role}</p>'
        f'<p class="card-meta th-body mt-2"><i class="fa-solid fa-phone" aria-hidden="true"></i> '
        f'โทรภายใน {tel}</p>'
        f'<p style="margin-top:.35rem;"><a href="mailto:{mail}">{mail}</a></p></div>'
        for name, role, tel, mail in people)
    return (f'<div class="leader-group"><div class="leader-group-head">'
            f'<h2 class="th-body">{th}</h2><span class="en">{en}</span></div>'
            f'<div class="advisor-grid mt-4">{rows}</div></div>')


STAFF_PAGE = page(
    crumb(("หน้าแรก", "index.html"), ("เกี่ยวกับคณะ", "about.html"),
          ("บุคลากรสำนักงานคณบดี", None))
    + hero("banner-inmotion.jpg", "เกี่ยวกับคณะ", "บุคลากรสำนักงานคณบดี",
           "Dean&rsquo;s Office Staff",
           "เจ้าหน้าที่ผู้ดูแลงานสนับสนุนของคณะ แบ่งตามงานที่รับผิดชอบ พร้อมช่องทางติดต่อโดยตรง")
    + '<section class="section"><div class="wrap">'
    + '<div class="notice th-body"><span>ติดต่อสำนักงานคณบดี: ชั้น 16 อาคารนวัตกรรม '
      "มหาวิทยาลัยศรีนครินทรวิโรฒ · โทร 02-169-1018, 098-829-0098 · "
      '<a href="mailto:saraban_bas@g.swu.ac.th">saraban_bas@g.swu.ac.th</a></span></div>'
    + '<div class="mt-6">' + "".join(staff_group(*g) for g in STAFF) + "</div>"
    + '<p class="th-body mt-5">คณาจารย์ประจำภาควิชาดูได้ที่ '
      '<a class="link-arrow" href="faculty.html">คณาจารย์และบุคลากร <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p>'
    + "</div></section>"
)

# =============================================================== META =======
NEW_PAGES = {
    "academic.html": (ACADEMIC, "Academic & Research — BAS SWU",
                      "Academic standards, quality assurance, UKPSF recognition and collaboration at BAS SWU.",
                      "academic"),
    "qa.html": (QA, "Quality Assurance — BAS SWU",
                "TQF, EdPEx and AUN-QA quality assurance frameworks used by BAS SWU.", "academic"),
    "mou.html": (MOU, "Academic Collaboration (MOU) — BAS SWU",
                 "Partner institutions, government agencies and companies with signed MOUs with BAS SWU.",
                 "academic"),
    "academic-calendar.html": (CALENDAR, "Academic Calendar — BAS SWU",
                               "Undergraduate and graduate academic calendars for BAS SWU.", "academic"),
    "sustainability.html": (SUSTAINABILITY, "Sustainability — BAS SWU",
                            "Environmental, social and governance work at BAS SWU.", "about"),
    "student-services.html": (SERVICES_PAGE, "Student Services — BAS SWU",
                              "Support systems and services for BAS SWU students.", "student-life"),
    "staff-deans-office.html": (STAFF_PAGE, "Dean's Office Staff — BAS SWU",
                                "Support staff of the BAS SWU Dean's Office with direct contact details.",
                                "about"),
}

# ----------------------------------------------------------------- NAV -----
ACADEMIC_MENU = [
    ("academic.html", "ภาพรวมวิชาการและวิจัย", "Academic &amp; Research Overview", False),
    ("academic.html#ukpsf", "UKPSF — การรับรองสมรรถนะอาจารย์", "UK Professional Standards Framework", False),
    ("qa.html", "ประกันคุณภาพ", "Quality Assurance", False),
    ("mou.html", "ความร่วมมือทางวิชาการ (MOU)", "Academic Collaboration", False),
    ("academic-calendar.html", "ปฏิทินการศึกษา", "Academic Calendar", False),
    ("https://academic.swu.ac.th/tuition", "ค่าธรรมเนียมการศึกษา", "Tuition Fees — external site", True),
    ("https://so17.tci-thaijo.org/index.php/BASSBJ", "วารสารบริหารธุรกิจ", "BASSBJ Journal — external site", True),
]

EXT_ATTR = (' class="is-ext" target="_blank" rel="noopener noreferrer"')
EXT_ICO = ('<i class="ext-ico fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>'
           '<span class="visually-hidden"> (เปิดเว็บไซต์ภายนอกในแท็บใหม่)</span>')

NAV_ITEM = (
    '<li class="nav-item{% if page.nav == "academic" %} current{% endif %}" data-key="academic">'
    '<a class="nav-link" href="academic.html" aria-haspopup="true">'
    '<span class="th-body">วิชาการและวิจัย</span><span class="chev" aria-hidden="true"></span></a>'
    '<div class="mega">'
    + "".join(
        f'<a href="{h}"{EXT_ATTR if e else ""}><span class="th-body">{th}</span>'
        f'<span class="en">{en}</span>{EXT_ICO if e else ""}</a>'
        for h, th, en, e in ACADEMIC_MENU)
    + "</div></li>"
)

DRAWER_ITEM = (
    '<li class="drawer-item"><button type="button" aria-expanded="false">'
    '<span class="th-body">วิชาการและวิจัย <span style="color:var(--muted);font-weight:400;">'
    "/ Academic &amp; Research</span></span><span class=\"chev\" aria-hidden=\"true\"></span></button>"
    '<div class="drawer-sub">'
    + "".join(
        f'<a href="{h}"{EXT_ATTR if e else ""}>{th} '
        f'<span style="color:var(--muted)">/ {en}</span></a>'
        for h, th, en, e in ACADEMIC_MENU)
    + "</div></li>"
)

# ลิงก์ที่ต้องเพิ่มเข้าเมนูเดิม  (anchor ที่ใช้หาจุดแทรก, html ที่จะแทรกต่อท้าย)
MENU_ADDITIONS = [
    # mega "เกี่ยวกับคณะ": เพิ่มค่านิยม/โครงสร้างองค์กร/บุคลากรสำนักงานคณบดี/ความยั่งยืน
    ('<a href="departments.html"><span class="th-body">ภาควิชา</span><span class="en">Departments</span></a>',
     '<a href="about.html#values"><span class="th-body">ค่านิยมและสมรรถนะหลัก</span><span class="en">Core Values</span></a>'
     '<a href="about.html#org"><span class="th-body">โครงสร้างองค์กร</span><span class="en">Organisation Structure</span></a>'),
    ('<a href="faculty.html"><span class="th-body">คณาจารย์และบุคลากร</span><span class="en">Faculty &amp; Staff</span></a>',
     '<a href="staff-deans-office.html"><span class="th-body">บุคลากรสำนักงานคณบดี</span><span class="en">Dean&rsquo;s Office Staff</span></a>'),
    ('<a href="green-award.html"><span class="th-body">Green Award</span><span class="en">Green Award / Sustainability</span></a>',
     '<a href="sustainability.html"><span class="th-body">ความยั่งยืน (ESG)</span><span class="en">Sustainability</span></a>'),
    # mega "ชีวิตนิสิต": เพิ่มบริการนิสิต
    ('<a href="student-life.html#facilities"><span class="th-body">สิ่งอำนวยความสะดวก</span><span class="en">Campus Facilities</span></a>',
     '<a href="student-services.html"><span class="th-body">บริการนิสิต</span><span class="en">Student Services</span></a>'),
    # drawer "เกี่ยวกับคณะ"
    ('<a href="faculty.html">คณาจารย์และบุคลากร <span style="color:var(--muted)">/ Faculty &amp; Staff</span></a>',
     '<a href="staff-deans-office.html">บุคลากรสำนักงานคณบดี <span style="color:var(--muted)">/ Dean&rsquo;s Office Staff</span></a>'),
    ('<a href="green-award.html">Green Award <span style="color:var(--muted)">/ Green Award / Sustainability</span></a>',
     '<a href="sustainability.html">ความยั่งยืน (ESG) <span style="color:var(--muted)">/ Sustainability</span></a>'),
]

NAV_ANCHOR = '<li class="nav-item{% if page.nav == "programs" %} current{% endif %}" data-key="programs">'
DRAWER_ANCHOR = ('<li class="drawer-item"><button type="button" aria-expanded="false">'
                 '<span class="th-body">หลักสูตร ')

# footer: เพิ่มคอลัมน์ลิงก์ใหม่เข้า "วิชาการ"
FOOTER_ANCHOR = '<a href="admissions.html">การรับสมัคร</a>'
FOOTER_ADD = ('<a href="academic.html">วิชาการและวิจัย</a>'
              '<a href="mou.html">ความร่วมมือ (MOU)</a>'
              '<a href="academic-calendar.html">ปฏิทินการศึกษา</a>')

# ---------------------------------------------------- about.html sections --
VALUES_ORG = (
    '<section class="section" id="values" style="background:var(--paper-dim);">\n'
    '  <div class="wrap">\n'
    + head("ค่านิยมองค์กร", "ค่านิยมและสมรรถนะหลัก", "Core Values &amp; Core Competency",
           "ค่านิยมของคณะสะกดเป็นคำว่า BAS ตรงกับชื่อคณะ — สามตัวอักษรนี้คือสิ่งที่คณะคาดหวังจากบุคลากรและบัณฑิตทุกคน")
    + '<div class="grid-3 mt-5">'
    + "".join(
        f'<div class="honour-card reveal">'
        f'<p class="th-body" style="font-family:var(--font-display);font-size:2.6rem;font-weight:700;'
        f'color:var(--brand-700);line-height:1;">{letter}</p>'
        f'<h3 class="th-body mt-2">{word}</h3>'
        f'<p style="margin-top:.5rem;">{desc}</p></div>'
        for letter, word, desc in [
            ("B", "Business",
             "ผู้มีความสามารถในการใช้และถ่ายทอดองค์ความรู้และความเชี่ยวชาญด้านบริหารธุรกิจให้กับผู้อื่น"),
            ("A", "Administration", "ผู้เน้นการลงมือปฏิบัติและมุ่งผลสัมฤทธิ์"),
            ("S", "Society", "ผู้ร่วมแบ่งปันสู่สังคม ชุมชน และประเทศชาติ"),
        ])
    + "</div>"
    + '<div class="notice th-body mt-5"><span><strong>สมรรถนะหลักของคณะ</strong> — '
      "&ldquo;สร้างการเปลี่ยนแปลงทางธุรกิจสู่การปฏิบัติ เพื่อสังคมที่ยั่งยืน&rdquo;</span></div>"
    + "\n  </div>\n</section>\n\n"
    '<section class="section" id="org">\n  <div class="wrap">\n'
    + head("โครงสร้างองค์กร", "โครงสร้างองค์กร", "Organisation Structure",
           "คณะแบ่งเป็นสำนักงานคณบดีและภาควิชา 3 ภาควิชา โดยสำนักงานคณบดีแบ่งงานภายในออกเป็น 5 งาน")
    + '<div class="grid-2 mt-5">'
      '<div class="vm-card reveal"><h3 class="th-body">สำนักงานคณบดี</h3>'
      '<p class="en" style="color:var(--muted);font-size:.8rem;">Dean&rsquo;s Office</p>'
      '<ul class="edu-list th-body mt-3">'
      "<li>งานบริหารและธุรการ</li><li>งานบริการการศึกษา</li><li>งานคลังและพัสดุ</li>"
      "<li>งานนโยบายและแผน</li><li>หน่วยประสานงานหลักสูตร</li></ul>"
      '<p class="mt-3"><a class="link-arrow" href="staff-deans-office.html">ดูรายชื่อบุคลากร '
      '<i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p></div>'
      '<div class="vm-card reveal"><h3 class="th-body">ภาควิชา</h3>'
      '<p class="en" style="color:var(--muted);font-size:.8rem;">Academic Departments</p>'
      '<ul class="edu-list th-body mt-3">'
      '<li><a href="departments.html#accounting-finance">ภาควิชาการบัญชีและการเงิน</a></li>'
      '<li><a href="departments.html#marketing-management">ภาควิชาการตลาดและการจัดการ</a></li>'
      '<li><a href="departments.html#business-administration">ภาควิชาบริหารธุรกิจ</a></li></ul>'
      '<p class="mt-3"><a class="link-arrow" href="departments.html">ดูรายละเอียดภาควิชา '
      '<i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p></div>'
      "</div>\n  </div>\n</section>\n\n"
)

ABOUT_ANCHOR = '<section class="section" style="background:var(--paper-dim);" id="history">'


def run():
    base = TPL / "base.html"
    if not base.exists():
        sys.exit("!! ไม่พบ templates/base.html — รัน build.py/ย้ายมาใช้ template ก่อน")

    # --- 1. หน้าใหม่ ---
    meta = json.loads(PAGES_JSON.read_text(encoding="utf-8"))
    n_new = 0
    for name, (body, title, desc, nav) in NEW_PAGES.items():
        p = PG / name
        if not p.exists():
            n_new += 1
        p.write_text(body, encoding="utf-8")
        meta[name] = {"title": title, "description": desc, "nav": nav}
    PAGES_JSON.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  templates/pages/: เขียน {len(NEW_PAGES)} หน้า (ใหม่ {n_new})  ·  data/pages.json รวม {len(meta)} หน้า")

    # --- 2. เมนู ---
    s = base.read_text(encoding="utf-8")
    if 'data-key="academic"' in s:
        print("  base.html: มีเมนู 'วิชาการและวิจัย' แล้ว — ข้าม")
    else:
        if NAV_ANCHOR not in s:
            sys.exit("!! หาจุดแทรกเมนูหลักไม่เจอ")
        s = s.replace(NAV_ANCHOR, NAV_ITEM + NAV_ANCHOR, 1)
        i = s.find(DRAWER_ANCHOR)
        if i < 0:
            sys.exit("!! หาจุดแทรก drawer ไม่เจอ")
        s = s[:i] + DRAWER_ITEM + s[i:]
        print("  base.html: เพิ่มเมนูหลัก 'วิชาการและวิจัย' (nav + drawer)")

    added = 0
    for anchor, extra in MENU_ADDITIONS:
        if extra.split('"')[1] in s and extra[:60] in s:
            continue
        if anchor not in s:
            print(f"  !! หา anchor เมนูไม่เจอ: {anchor[:48]}…")
            continue
        s = s.replace(anchor, anchor + extra, 1)
        added += 1
    print(f"  base.html: เพิ่มลิงก์ในเมนูเดิม {added} จุด" if added
          else "  base.html: ลิงก์เมนูเดิมครบแล้ว — ข้าม")

    if "ความร่วมมือ (MOU)" in s:
        print("  base.html: footer มีลิงก์ใหม่แล้ว — ข้าม")
    elif FOOTER_ANCHOR in s:
        s = s.replace(FOOTER_ANCHOR, FOOTER_ANCHOR + FOOTER_ADD, 1)
        print("  base.html: เพิ่มลิงก์ footer 3 รายการ")
    else:
        print("  !! หา anchor footer ไม่เจอ")
    base.write_text(s, encoding="utf-8")

    # --- 3. about.html: ค่านิยม + โครงสร้างองค์กร ---
    a = PG / "about.html"
    t = a.read_text(encoding="utf-8")
    if 'id="values"' in t:
        print("  about.html: มี section ค่านิยม/โครงสร้างองค์กรแล้ว — ข้าม")
    elif ABOUT_ANCHOR not in t:
        print("  !! about.html: หาจุดแทรกไม่เจอ")
    else:
        a.write_text(t.replace(ABOUT_ANCHOR, VALUES_ORG + ABOUT_ANCHOR, 1), encoding="utf-8")
        print("  about.html: เพิ่ม section ค่านิยม (BAS) + โครงสร้างองค์กร")

    print("\nต่อไปรัน:  python build.py")


if __name__ == "__main__":
    print("v10 — เติมหน้าที่ขาดจากเว็บต้นแบบ")
    run()

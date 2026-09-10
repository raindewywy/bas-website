#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_greenoffice.py — REQUIREMENTS v9 · เฟส 8 (REQ-E1 / REQ-E2)

  REQ-E2  เติมเนื้อหา Green Office จาก bas2.swu.ac.th/greenoffice
            1) นิยาม Green Office
            2) แนวทางดำเนินการ
            3) สิ่งที่ทำได้ทันที
            4) ชื่อเกณฑ์ประเมิน 6 หมวด ให้ตรงต้นฉบับ (ของเดิมเรียบเรียงใหม่ ไม่ตรงชื่อทางการ)
          reuse .split / .notice / .edu-list / .honour-card ที่มีอยู่ ไม่สร้าง component ใหม่

  REQ-E1  ใส่ hero banner — ทำอัตโนมัติ "ถ้ามีไฟล์" assets/media/banner-greenoffice.jpg
          (ยังดาวน์โหลดจาก bas2 ไม่ได้จากเครื่องนี้ ดูหมายเหตุท้ายไฟล์)

  แกลเลอรีรูปกิจกรรม: แสดงเป็น .grid-3 การ์ดรูป (reuse .card + .card-media)
  เปิดอัตโนมัติเมื่อมีไฟล์ assets/media/greenoffice-*.jpg|png ตั้งแต่ 3 รูปขึ้นไป
  ถ้ายังไม่มีรูปจะไม่ใส่กล่อง placeholder ตามกติกา REQ-A4

รันซ้ำได้ (idempotent)
    python gen/fix_v9_greenoffice.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
BANNER = ROOT / "assets" / "media" / "banner-greenoffice.jpg"


def page_path(name):
    """หลังย้ายมาใช้ template แล้ว ต้องแก้ที่ templates/pages/ ไม่ใช่ .html ที่ root
    (root ถูก build.py เขียนทับ) — ถ้ายังไม่มี templates/ ก็แก้ที่ root เหมือนเดิม"""
    tpl = ROOT / "templates" / "pages" / name
    return tpl if tpl.exists() else ROOT / name

PAGE = None  # กำหนดใน __main__

# ---- REQ-E2 (1)(2)(3) — บล็อกเนื้อหาที่ยังขาด ------------------------------
INTRO = """<section class="section"><div class="wrap">
  <div class="split">
    <div class="split-copy reveal">
      <p class="eyebrow th-body">สำนักงานสีเขียว</p>
      <h2 class="bi-heading"><span class="bi-th th-body">Green Office คืออะไร</span><span class="bi-en">What is a Green Office</span></h2>
      <p class="th-body mt-3"><strong>&ldquo;สำนักงานและกิจกรรมต่าง ๆ ภายในสำนักงาน ที่ส่งผลกระทบต่อสิ่งแวดล้อมน้อยที่สุด&rdquo;</strong> โดยใช้ทรัพยากรและพลังงานอย่างประหยัด พร้อมระบบการจัดการของเสียที่มีประสิทธิภาพ</p>
      <h3 class="th-body mt-5" style="font-size:1.05rem;">แนวทางดำเนินการ</h3>
      <p class="th-body mt-2" style="color:var(--muted);">การปรับเปลี่ยนเป็นสำนักงานสีเขียวครอบคลุมตั้งแต่การออกแบบสถาปัตยกรรมและการก่อสร้าง การจัดหาอุปกรณ์ที่ประหยัดพลังงานและเป็นมิตรต่อสิ่งแวดล้อม ไปจนถึงพฤติกรรมของบุคลากรในการใช้ทรัพยากรและพลังงาน</p>
    </div>
    <div class="split-copy reveal">
      <h3 class="th-body" style="font-size:1.05rem;">สิ่งที่ทำได้ทันที</h3>
      <p class="th-body mt-2" style="color:var(--muted);">การเปลี่ยนแปลงเริ่มได้จากพฤติกรรมประจำวันของทุกคนในสำนักงาน</p>
      <ul class="edu-list th-body mt-3">
        <li>ปิดไฟและอุปกรณ์สำนักงานทุกครั้งเมื่อเลิกใช้งาน</li>
        <li>สร้างนิสัยการใช้พลังงานอย่างรู้คุณค่าในชีวิตประจำวัน</li>
        <li>จัดซื้อวัสดุสำนักงานที่ประหยัดพลังงานและเป็นมิตรต่อสิ่งแวดล้อม</li>
      </ul>
    </div>
  </div>
</div></section>

"""

# ---- REQ-E2 (4) — ชื่อ 6 หมวดตามต้นฉบับ ------------------------------------
CATEGORIES = [
    ("นโยบายและแผนดำเนินงานต่อเนื่อง",
     "หมวดที่ 1 · นโยบาย การวางแผนการดำเนินงาน และการปรับปรุงอย่างต่อเนื่อง"),
    ("การสื่อสารและสร้างความตระหนัก",
     "หมวดที่ 2 · การสื่อสารและสร้างจิตสำนึก"),
    ("การใช้ทรัพยากรและพลังงาน",
     "หมวดที่ 3 · การใช้ทรัพยากรและพลังงาน"),
    ("การจัดการของเสีย",
     "หมวดที่ 4 · การจัดการของเสีย"),
    ("สภาพแวดล้อมและความปลอดภัย",
     "หมวดที่ 5 · สภาพแวดล้อมและความปลอดภัย"),
    ("การจัดซื้อจัดจ้างที่เป็นมิตรต่อสิ่งแวดล้อม",
     "หมวดที่ 6 · การจัดซื้อและจัดจ้างที่เป็นมิตรกับสิ่งแวดล้อม"),
]

HERO_OLD = '<section class="page-hero"><div class="wrap"><p class="eyebrow th-body">เกี่ยวกับคณะ</p>'
HERO_NEW = ('<section class="page-hero page-hero--image">'
            '<img class="hero-bg" src="assets/media/banner-greenoffice.jpg" alt="" aria-hidden="true" '
            'loading="eager" decoding="async" fetchpriority="high">'
            '<div class="wrap"><p class="eyebrow th-body">เกี่ยวกับคณะ</p>')

DUP_HEAD_OLD = ('<h2 class="bi-heading"><span class="bi-th th-body">Green Office</span>'
                '<span class="bi-en">Sustainable Office Programme</span></h2>')
DUP_HEAD_NEW = ('<h2 class="bi-heading"><span class="bi-th th-body">เกณฑ์ประเมิน 6 หมวด</span>'
                '<span class="bi-en">Six Assessment Categories</span></h2>')

GALLERY_CANDIDATES = ["greenoffice-01.jpg", "greenoffice-02.jpg", "greenoffice-03.png",
                      "greenoffice-04.png", "greenoffice-05.png"]
GALLERY_CAPTIONS = {
    "greenoffice-01.jpg": "กิจกรรมสำนักงานสีเขียวของคณะ",
    "greenoffice-02.jpg": "การสื่อสารและสร้างจิตสำนึกด้านสิ่งแวดล้อม",
    "greenoffice-03.png": "การใช้ทรัพยากรและพลังงานอย่างรู้คุณค่า",
    "greenoffice-04.png": "การจัดการของเสียภายในสำนักงาน",
    "greenoffice-05.png": "การจัดซื้อจัดจ้างที่เป็นมิตรกับสิ่งแวดล้อม",
}
GALLERY_MARK = 'id="greenoffice-gallery"'

SECTION_ANCHOR = '<section class="section"><div class="wrap">\n\n<div class="section-head reveal">'


if __name__ == "__main__":
    print("REQ-E1 / REQ-E2 — Green Office")
    PAGE = page_path("green-award.html")
    print(f"  แก้ไฟล์: {PAGE.relative_to(ROOT)}")
    if not PAGE.exists():
        sys.exit("!! ไม่พบ green-award.html")
    s = PAGE.read_text(encoding="utf-8")

    # --- REQ-E2 (1)(2)(3) ---
    if "Green Office คืออะไร" in s:
        print("  green-award.html: มีบล็อกนิยาม/แนวทางแล้ว — ข้าม")
    elif SECTION_ANCHOR not in s:
        print("  !! หาจุดแทรกบล็อกนิยามไม่เจอ — ข้ามส่วนนี้")
    else:
        s = s.replace(SECTION_ANCHOR, INTRO + SECTION_ANCHOR, 1)
        print("  green-award.html: เพิ่มนิยาม + แนวทางดำเนินการ + สิ่งที่ทำได้ทันที")

    # --- REQ-E2 (4) ---
    n = 0
    for old, new in CATEGORIES:
        tag = '<h3 class="th-body" style="font-size:1rem;">%s</h3>' % old
        if tag in s:
            s = s.replace(tag, '<h3 class="th-body" style="font-size:1rem;">%s</h3>' % new, 1)
            n += 1
    print(f"  green-award.html: ปรับชื่อเกณฑ์ {n}/6 หมวดให้ตรงต้นฉบับ"
          if n else "  green-award.html: ชื่อ 6 หมวดตรงแล้ว — ข้าม")

    # --- ตัดหัวข้อ H2 ที่ซ้ำกับบล็อกนิยามด้านบน ---
    if DUP_HEAD_OLD in s:
        s = s.replace(DUP_HEAD_OLD, DUP_HEAD_NEW, 1)
        print("  green-award.html: เปลี่ยนหัวข้อ section ที่ 2 เป็น 'เกณฑ์ประเมิน 6 หมวด' (เดิมซ้ำกับด้านบน)")

    # --- REQ-E2 (5) แกลเลอรีรูปกิจกรรม ---
    have = [f for f in GALLERY_CANDIDATES if (ROOT / "assets" / "media" / f).exists()]
    if GALLERY_MARK in s:
        print("  green-award.html: มีแกลเลอรีแล้ว — ข้าม")
    elif len(have) < 3:
        print(f"  ** ข้ามแกลเลอรี: มีรูป {len(have)}/5 (ต้องการอย่างน้อย 3)")
        print("     รัน python gen/fetch_bas2_media.py ก่อน แล้วรันสคริปต์นี้ซ้ำ")
    else:
        cards = "".join(
            '<div class="card reveal"><div class="card-media">'
            '<img class="media-img" src="assets/media/%s" alt="%s" loading="lazy" decoding="async">'
            '</div><div class="card-body"><p class="card-desc th-body">%s</p></div></div>'
            % (f, GALLERY_CAPTIONS[f], GALLERY_CAPTIONS[f]) for f in have)
        gallery = ('<section class="section" id="greenoffice-gallery" style="background:var(--paper-dim);">'
                   '<div class="wrap"><div class="section-head reveal"><div>'
                   '<p class="eyebrow th-body">ภาพกิจกรรม</p>'
                   '<h2 class="bi-heading"><span class="bi-th th-body">การดำเนินงานสำนักงานสีเขียว</span>'
                   '<span class="bi-en">Green Office in Action</span></h2>'
                   '</div></div><div class="grid-3 mt-5">' + cards + "</div></div></section>\n")
        s = s.replace("{% endblock %}", gallery + "{% endblock %}", 1) if "{% endblock %}" in s else s.replace("</main>", gallery + "</main>", 1)
        print(f"  green-award.html: เพิ่มแกลเลอรี grid-3 ({len(have)} รูป)")

    # --- REQ-E1 ---
    if "page-hero--image" in s:
        print("  green-award.html: hero มีรูปแล้ว — ข้าม")
    elif not BANNER.exists():
        print("  ** ข้าม REQ-E1: ยังไม่มี assets/media/banner-greenoffice.jpg")
        print("     บันทึกไฟล์นี้ลง assets/media/ แล้วรันสคริปต์นี้ซ้ำ hero จะขึ้นเอง")
    elif HERO_OLD not in s:
        print("  !! หา page-hero ของ green-award.html ไม่เจอ")
    else:
        s = s.replace(HERO_OLD, HERO_NEW, 1)
        print("  green-award.html: REQ-E1 hero -> assets/media/banner-greenoffice.jpg")

    PAGE.write_text(s, encoding="utf-8")

# หมายเหตุรูปที่ยังต้องเตรียม (ดาวน์โหลดเองจาก bas2 แล้ววางใน assets/media/):
#   banner-greenoffice.jpg  <- Portals/64/BlockBuilderImages/23855/GreenOffice1600x6003.jpg
#   greenoffice-logo.png    <- Portals/64/BlockBuilderImages/23856/logo-150x150.png
#   greenoffice-01.jpg …    <- Portals/64/BlockBuilderImages/23856/02-9.jpg ฯลฯ

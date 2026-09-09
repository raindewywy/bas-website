# -*- coding: utf-8 -*-
"""
หน้าแรก — ปรับลำดับการมองเห็นและการเข้าถึงตามทิศทางที่อนุมัติ (SYSTEMS)
ไม่ย้าย/ไม่ลบ section เดิม เพิ่มเฉพาะแถบทางลัดระดับหลักสูตรในหมวด "หลักสูตร"
ที่แยก 3+1 (ปริญญาคู่ GBM) ออกจาก 4+1 (ตรีควบโท) อย่างชัดเจน
และทำเครื่องหมายลิงก์ภายนอกให้ MBA
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "index.html"

EXT_ICON = ('<svg class="ext-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" aria-hidden="true"><path d="M14 5h5v5"/><path d="M19 5l-8 8"/>'
            '<path d="M18 14v5H5V6h5"/></svg>')

ROUTES = [
    ("01", "programs.html?level=undergraduate", "ปริญญาตรี (ภาษาไทย)", "Undergraduate", "", ""),
    ("02", "program-detail.html?p=global-business-management", "GBM — การจัดการธุรกิจโลก",
     "Global Business Management (English-taught)", "", ""),
    ("03", "https://mba.swu.ac.th/", "MBA", "Master of Business Administration", "ext",
     "เว็บไซต์ภายนอก"),
    ("04", "program-detail.html?p=phd", "PhD", "Doctor of Philosophy", "", ""),
    ("05", "programs.html#plan41", "ตรีควบโท 4+1", "Bachelor + Master (4+1)", "",
     "ปริญญาตรีต่อเนื่องปริญญาโท"),
    ("06", "international.html#exchange", "ปริญญาคู่ 3+1", "3+1 Double Degree — GBM", "",
     "เรียนที่ มศว 3 ปี + สถาบันพันธมิตร 1 ปี"),
]


def route(idx, href, th, en, kind, note):
    ext = kind == "ext"
    attrs = ' target="_blank" rel="noopener noreferrer"' if ext else ""
    cls = "prog-route is-ext" if ext else "prog-route"
    hint = '<span class="prog-route-note th-body">%s</span>' % note if note else ""
    tail = (EXT_ICON + '<span class="visually-hidden"> (เปิดเว็บไซต์ภายนอกในแท็บใหม่ / '
            'opens an external site in a new tab)</span>') if ext else ""
    return ('<a class="%s" href="%s"%s>'
            '<span class="prog-route-k" aria-hidden="true">%s</span>'
            '<span class="prog-route-t th-body">%s%s</span>'
            '<span class="prog-route-e">%s</span>%s</a>'
            % (cls, href, attrs, idx, th, tail, en, hint))


STRIP = ('<nav class="prog-routes reveal" aria-label="ทางลัดไปยังระดับหลักสูตร / Programme routes">'
         + "".join(route(*r) for r in ROUTES)
         + "</nav>")

s = IDX.read_text(encoding="utf-8")

if "prog-routes" not in s:
    anchor = '<div class="grid-3 mt-5"><a class="card program-card reveal" data-filter="undergraduate"'
    i = s.index(anchor)
    s = s[:i] + STRIP + "\n    " + s[i:]

# หมวดข่าวหน้าแรก: ให้ heading ของการ์ดเป็นระดับที่ถูกต้องอยู่แล้ว — ตรวจเฉพาะ alt ที่หายไป
s = s.replace('<img ', '<img loading="lazy" ').replace('<img loading="lazy" class="brand-mark"',
                                                       '<img class="brand-mark"')
s = re.sub(r'<img loading="lazy" loading="lazy" ', '<img loading="lazy" ', s)

IDX.write_text(s, encoding="utf-8")
print("home: programme routes strip + lazy images")

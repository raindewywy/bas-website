# -*- coding: utf-8 -*-
"""
แก้ทุกไฟล์พร้อมกัน (จุดเดียว มีผลทุกหน้า):
  1. ชื่อผู้บริหารที่สะกดผิด -> ชื่อที่ถูกต้องตามเว็บทางการ
  2. ลิงก์ "ผู้บริหาร" ในเมนู/drawer/footer: about.html#leadership -> leadership.html
  3. หน้า about.html: เพิ่มปุ่มไปหน้าผู้บริหารเต็ม
"""
import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_leaders import NAME_FIXES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

targets = sorted(glob.glob(str(ROOT / "*.html"))) + [str(ROOT / "assets" / "data.js")]
counts = {"names": 0, "links": 0}

for path in targets:
    p = Path(path)
    s = orig = p.read_text(encoding="utf-8")

    for wrong, right in NAME_FIXES.items():
        if wrong in s:
            counts["names"] += s.count(wrong)
            s = s.replace(wrong, right)

    # ลิงก์ผู้บริหาร -> หน้าใหม่ (ยกเว้นในหน้า about เองที่ยังมี section id=leadership อยู่)
    n = s.count('href="about.html#leadership"')
    if n:
        s = s.replace('href="about.html#leadership"', 'href="leadership.html"')
        counts["links"] += n

    if s != orig:
        p.write_text(s, encoding="utf-8")
        print("patched", p.name)

# ---- about.html: ให้ section ผู้บริหารชี้ไปหน้าเต็ม ----
about = ROOT / "about.html"
s = about.read_text(encoding="utf-8")
anchor = '<p class="lede">สำนักคณบดี หัวหน้าภาควิชา และผู้ช่วยคณบดี ผู้นำ BAS SWU</p>'
cta = ('<a class="btn btn-secondary btn-sm" href="leadership.html">'
       'ดูผู้บริหารทั้งหมดและประวัติรายบุคคล</a>')
if anchor in s and "leader-natinee" not in s and cta not in s:
    s = s.replace(anchor, anchor + "\n      </div>\n      <div>" + cta, 1)
    # ปิด div ที่เปิดเพิ่มไม่ได้ -> ใช้วิธีแทรกปุ่มในช่องว่างของ section-head แทน
    s = s.replace(anchor + "\n      </div>\n      <div>" + cta, anchor + "\n      </div>\n      " + cta, 1)
    about.write_text(s, encoding="utf-8")
    print("patched about.html section CTA")

print(counts)

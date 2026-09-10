#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_tweaks.py — ปรับย่อยตามที่ผู้ใช้สั่ง (v9)

  1) ลบ "เส้น interact" ท้ายการ์ด Academic (.programme-accent)
  2) index.html มี <h1> สองตัว (eyebrow ถูกทำเป็น h1) -> เปลี่ยนตัว eyebrow เป็น <p>
     ไม่กระทบหน้าตา เพราะ .eyebrow คุมสไตล์อยู่แล้ว

ข้อ 1 ซ่อนด้วย CSS อย่างเดียว ไม่แตะ markup และไม่แตะ hover/focus effect อื่น
ของ .programme-card (ยกการ์ด · ไอคอนขยาย · หัวข้อขยับ ยังทำงานปกติ)

รันซ้ำได้ (idempotent)
    python gen/fix_v9_tweaks.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"
MARK = "/* == v9 tweaks =="

BLOCK = """

/* == v9 tweaks ==========================================================
   ลบเส้น interact ท้ายการ์ด Academic ตามที่ผู้ใช้สั่ง
   ซ่อนเฉพาะเส้นนี้ ไม่กระทบ hover/focus อื่นของ .programme-card
   ===================================================================== */
.programme-accent{ display:none; }
"""


def page_path(name):
    """หลังย้ายมาใช้ template แล้ว ต้องแก้ที่ templates/pages/ ไม่ใช่ .html ที่ root
    (root ถูก build.py เขียนทับ) — ถ้ายังไม่มี templates/ ก็แก้ที่ root เหมือนเดิม"""
    tpl = ROOT / "templates" / "pages" / name
    return tpl if tpl.exists() else ROOT / name


H1_OLD = '<h1 class="eyebrow th-body">\n          คณะบริหารธุรกิจเพื่อสังคม\n        </h1>'
H1_NEW = '<p class="eyebrow th-body">\n          คณะบริหารธุรกิจเพื่อสังคม\n        </p>'


def patch_index_h1():
    INDEX = page_path("index.html")
    if not INDEX.exists():
        return
    h = INDEX.read_text(encoding="utf-8")
    if H1_OLD not in h:
        print("  index.html: h1 ซ้ำแก้แล้ว/ไม่พบรูปแบบเดิม — ข้าม")
        return
    INDEX.write_text(h.replace(H1_OLD, H1_NEW, 1), encoding="utf-8")
    print(f"  {INDEX.name}: eyebrow <h1> -> <p>  (เหลือ h1 เดียวต่อหน้า)")


if __name__ == "__main__":
    print("ปรับย่อย v9")
    s = CSS.read_text(encoding="utf-8")
    if MARK in s:
        print("  styles.css: patch นี้มีอยู่แล้ว — ข้าม")
    else:
        CSS.write_text(s.rstrip("\n") + "\n" + BLOCK, encoding="utf-8")
        print("  styles.css: .programme-accent -> display:none")
    patch_index_h1()

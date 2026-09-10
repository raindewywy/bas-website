#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_media_clean.py — REQUIREMENTS v9 · REQ-M1/M2 (เก็บตก)
  .news-row .news-thumb ยังเหลือ "ลายน้ำ" ทับรูปจริง 2 ชั้น:
    1) พื้นหลัง linear-gradient(brand-800 -> brand-700 -> brand-300)  = ติดโทนฟ้า
    2) ::after repeating-linear-gradient 115deg                        = ลายเส้นทแยง
  ทั้งคู่ออกแบบไว้สมัยยังเป็นกล่อง placeholder ตอนนี้มีรูปจริงแล้วจึงต้องปิด

  หมายเหตุ: rule เดิม `.news-row .news-thumb` มี specificity (0,2,0)
  จึงทับ `.news-thumb{background:#EDEFF1}` ของ REQ-M1 ที่เป็น (0,1,0) อยู่
  ต้องแก้ด้วย selector ที่เจาะจงเท่ากันขึ้นไป

รันซ้ำได้ (idempotent)
    python gen/fix_v9_media_clean.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"
MARK = "/* == v9 media clean =="

BLOCK = """

/* == v9 media clean == REQ-M1/M2 ========================================
   ปิดลายน้ำ/โทนฟ้าที่ยังทับรูปจริงใน .news-thumb
   ===================================================================== */
.news-row .news-thumb{ background:#EDEFF1; }
.news-row .news-thumb:has(> .media-img)::after,
.news-row .news-thumb:has(> picture)::after,
.news-thumb:has(> .media-img)::after,
.news-thumb:has(> picture)::after{ display:none; }

/* กันพลาดสำหรับกรอบรูปอื่น ๆ ที่อาจมีลายตกแต่งเพิ่มภายหลัง */
.act-media:has(> .media-img)::after,
.split-media:has(> .media-img)::after,
.staff-photo:has(> .media-img)::after{ display:none; }
"""


if __name__ == "__main__":
    print("REQ-M1/M2 — ลบลายน้ำที่ยังทับรูปจริง")
    s = CSS.read_text(encoding="utf-8")
    if MARK in s:
        print("  styles.css: patch นี้มีอยู่แล้ว — ข้าม")
    else:
        CSS.write_text(s.rstrip("\n") + "\n" + BLOCK, encoding="utf-8")
        print("  styles.css: ปิด gradient + ลายเส้นทแยงบน .news-thumb")

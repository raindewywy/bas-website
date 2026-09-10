#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_phase7.py — REQUIREMENTS v9 · REQ-C3 (Academic component)
  - การ์ด .programme-card 4 ใบใน index.html: เลิกใช้ hex hardcode -> ไล่เฉดฟ้า 4 ระดับต่อเนื่อง
  - .programme-accent: เส้นเน้นใช้ var(--brand-400)
  - เพิ่ม token --brand-650 (ขั้นระหว่าง 600/700 ที่ตัวอักษรขาวขนาดเล็กยังผ่าน AA)

เหตุผลที่ไม่ใช้ --brand-600 ตามตารางในเอกสาร:
  ข้อความในการ์ดคือ .programme-en 14px และ .programme-description ~15.7px
  = "ตัวอักษรเล็ก" ต้องการ >= 4.5:1 แต่ brand-600 ให้ 3.71:1
  เอกสารระบุเองว่า "ถ้าตัวเล็กให้ใช้ --brand-700 แทน" จึงใช้ขั้น 650 (4.55:1)
  เพื่อยังคงเป็นไล่เฉด 4 ระดับที่ต่างกันจริงและผ่าน AA ทุกใบ

รันซ้ำได้ (idempotent)
    python gen/fix_v9_phase7.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"
INDEX = ROOT / "index.html"

# เข้ม -> สว่าง ซ้ายไปขวา (contrast กับตัวอักษรขาว)
# ใช้ modifier class ใน styles.css ไม่ใช่ Tailwind arbitrary value เพราะ
# .programme-card ทั้งคอมโพเนนต์อยู่ใน styles.css อยู่แล้ว และไม่ต้องพึ่ง JIT ของ CDN
TILES = [
    ("bg-[#005A66]", "programme-card--tone-1", "การรับสมัคร", "11.95:1"),
    ("bg-[#087783]", "programme-card--tone-2", "ปริญญาตรี", "9.07:1"),
    ("bg-[#18242A]", "programme-card--tone-3", "บัณฑิตศึกษา", "5.61:1"),
    ("bg-[#53616A]", "programme-card--tone-4", "โอกาสระดับนานาชาติ", "4.55:1"),
]

TONE_CSS = """
/* ---- REQ-C3 (v9): ไล่เฉดฟ้า 4 ระดับของการ์ด Academic --------------------
   เข้ม -> สว่าง ตามลำดับการ์ดซ้ายไปขวา ตัวอักษรขาวผ่าน AA ทุกใบ           */
.programme-card--tone-1{ background:var(--brand-900); }  /* 11.95:1 */
.programme-card--tone-2{ background:var(--brand-800); }  /*  9.07:1 */
.programme-card--tone-3{ background:var(--brand-700); }  /*  5.61:1 */
.programme-card--tone-4{ background:var(--brand-650); }  /*  4.55:1 */
"""

TOKEN_ANCHOR = "  --brand-700:#00718C;"
TOKEN_NEW = ("  --brand-650:#0080A3;   /* ขั้นกลาง 600/700 — ตัวอักษรขาวเล็กผ่าน AA (4.55:1) */\n"
             "  --brand-700:#00718C;")


def patch_css():
    s = CSS.read_text(encoding="utf-8")
    if "--brand-650" in s:
        print("  styles.css: มี --brand-650 แล้ว — ข้าม")
    else:
        if TOKEN_ANCHOR not in s:
            sys.exit("!! หา token --brand-700 ไม่เจอ")
        s = s.replace(TOKEN_ANCHOR, TOKEN_NEW, 1)
        print("  styles.css: เพิ่ม token --brand-650")

    old_accent = "  height: 4px;\n  margin-left: auto;\n  background: #fff;"
    new_accent = "  height: 4px;\n  margin-left: auto;\n  background: var(--brand-400);"
    if old_accent in s:
        s = s.replace(old_accent, new_accent, 1)
        print("  styles.css: .programme-accent -> var(--brand-400)")
    else:
        print("  styles.css: .programme-accent แก้ไปแล้ว — ข้าม")

    if "programme-card--tone-1" not in s:
        anchor = ".programme-card:hover,"
        if anchor not in s:
            sys.exit("!! หา .programme-card:hover ไม่เจอ")
        s = s.replace(anchor, TONE_CSS + "\n" + anchor, 1)
        print("  styles.css: เพิ่ม .programme-card--tone-1..4")

    CSS.write_text(s, encoding="utf-8")


def patch_index():
    s = INDEX.read_text(encoding="utf-8")
    n = 0
    for old, new, label, ratio in TILES:
        if old in s:
            s = s.replace(old, new, 1)
            print(f"  index.html: {label} {old} -> {new}  (ขาวบนพื้น {ratio})")
            n += 1
    if n:
        INDEX.write_text(s, encoding="utf-8")
    else:
        print("  index.html: การ์ด Academic แก้ไปแล้ว — ข้าม")


if __name__ == "__main__":
    print("REQ-C3 — Academic component")
    patch_css()
    patch_index()

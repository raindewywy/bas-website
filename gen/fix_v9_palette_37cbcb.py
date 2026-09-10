#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_palette_37cbcb.py — เปลี่ยนสีหลักเป็น #37CBCB

โครงสร้าง token เดิม (REQ-C1) ไม่เปลี่ยน เปลี่ยนเฉพาะ "ค่า" ของแต่ละขั้น
  - ขั้นสว่าง 50/100/300/400/500 : ยึด hue 180 ตาม #37CBCB
  - ขั้นเข้ม 600-900             : ไล่ hue ไปทางน้ำเงิน 184->202
                                   และล็อกค่า contrast กับตัวอักษรขาวไว้เท่าเดิม
                                   (3.70 / 4.55 / 5.63 / 9.07 / 11.99)
  - rgba ที่ hardcode อ้าง brand-500 / brand-900 อัปเดตตามค่าใหม่

#37CBCB เองมี contrast กับสีขาวเพียง 1.99:1 จึงห้ามใช้เป็นพื้นของตัวอักษรขาว
โครงที่วางไว้เดิมส่ง surface พวกนั้นไป --brand-700 อยู่แล้ว จึงไม่ต้องแก้ซ้ำ

รันซ้ำได้ (idempotent)
    python gen/fix_v9_palette_37cbcb.py
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"

TOKENS = {
    "brand-50": "#EFFBFB",
    "brand-100": "#CDF3F3",
    "brand-300": "#86EAEA",
    "brand-400": "#58E4E4",
    "brand-500": "#37CBCB",   # <- สีหลัก
    "brand-600": "#13939C",
    "brand-650": "#0F8198",
    "brand-700": "#087090",
    "brand-800": "#0B4E6B",
    "brand-900": "#0E3A54",
}

# rgba ที่อ้างสีเดิมโดยตรง
RGBA = {
    "rgba(0,179,201,": "rgba(55,203,203,",   # brand-500 เดิม #00B3C9 -> #37CBCB
    "rgba(11,58,87,": "rgba(14,58,84,",      # brand-900 เดิม #0B3A57 -> #0E3A54
}


if __name__ == "__main__":
    print("เปลี่ยนสีหลักเป็น #37CBCB")
    s = CSS.read_text(encoding="utf-8")
    if "#37CBCB" in s:
        print("  styles.css: ใช้ #37CBCB อยู่แล้ว — ข้าม")
        sys.exit(0)

    n = 0
    for name, val in TOKENS.items():
        pat = re.compile(r"(--%s\s*:\s*)#[0-9A-Fa-f]{6}" % re.escape(name))
        s, k = pat.subn(lambda m: m.group(1) + val, s, count=1)
        if k:
            n += 1
        else:
            print(f"  !! ไม่พบ token --{name}")
    print(f"  styles.css: อัปเดต token {n}/{len(TOKENS)} ขั้น")

    for old, new in RGBA.items():
        c = s.count(old)
        if c:
            s = s.replace(old, new)
            print(f"  styles.css: {old}…) -> {new}…)  {c} จุด")

    CSS.write_text(s, encoding="utf-8")

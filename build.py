#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — สร้างไฟล์ .html ทั้งเว็บจาก template + data

โครงสร้าง (แยก Model / View / Controller)
    data/pages.json        Model  — metadata ของแต่ละหน้า (title, description, เมนูที่ active)
    assets/data.js         Model  — ข้อมูลหลักสูตร ข่าว ภาควิชา ผู้บริหาร (โหลดฝั่ง client)
    templates/base.html    View   — โครงหน้าเดียว: head · header/nav · footer · script
    templates/pages/*.html View   — เนื้อหาเฉพาะหน้า (เฉพาะส่วนใน <main>)
    build.py               Controller — ประกอบทั้งหมดออกมาเป็น static HTML ที่ root

ผลลัพธ์ยังเป็น static HTML ล้วน ไม่ต้องมี runtime บนเซิร์ฟเวอร์
deploy กับ Vercel / Netlify / GitHub Pages ได้ตรง ๆ

    python build.py            # สร้างไฟล์ทั้งหมด
    python build.py --check    # ตรวจว่าไฟล์ที่มีอยู่ตรงกับ template ไหม (ไม่เขียนทับ)

ต้องมี:  pip install -r requirements.txt
"""
from pathlib import Path
import json
import sys

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    sys.exit("!! ต้องติดตั้งก่อน:  pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
PAGES_JSON = ROOT / "data" / "pages.json"


def build(check_only=False):
    pages = json.loads(PAGES_JSON.read_text(encoding="utf-8"))
    env = Environment(
        loader=FileSystemLoader([TEMPLATES, TEMPLATES / "pages"]),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    written, unchanged, drift = 0, 0, []
    for name, meta in sorted(pages.items()):
        html = env.get_template(name).render(page=meta, pages=pages)
        dest = ROOT / name
        current = dest.read_text(encoding="utf-8") if dest.exists() else None
        if current == html:
            unchanged += 1
            continue
        if check_only:
            drift.append(name)
            continue
        dest.write_text(html, encoding="utf-8")
        written += 1

    if check_only:
        if drift:
            print(f"ไม่ตรงกับ template {len(drift)} ไฟล์: {', '.join(drift)}")
            print("รัน  python build.py  เพื่อสร้างใหม่")
            return 1
        print(f"ตรงกับ template ครบ {unchanged} ไฟล์")
        return 0

    print(f"สร้างใหม่ {written} ไฟล์ · ไม่เปลี่ยน {unchanged} ไฟล์ · รวม {len(pages)} หน้า")
    return 0


if __name__ == "__main__":
    sys.exit(build(check_only="--check" in sys.argv))

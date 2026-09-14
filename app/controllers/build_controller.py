#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app/controllers/build_controller.py — Controller

ดึงข้อมูลจาก Model (app/models/pages.py) มา render ผ่าน View (app/views/*.html)
ด้วย Jinja2 แล้วเขียนผลลัพธ์เป็น static .html ที่ public/

public/ เป็นโฟลเดอร์ deploy — ตั้ง publish/output directory ของ host เป็น `public`
public/assets/ คือที่เก็บ CSS/JS/รูป "ที่เดียว" (ไม่มีสำเนาที่ root แล้ว)
build.py จึงไม่ต้อง copy อะไร และไม่แตะ public/assets/ เลย
"""
from pathlib import Path
import sys

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    sys.exit("!! ต้องติดตั้งก่อน:  pip install -r requirements.txt")

APP_DIR = Path(__file__).resolve().parent.parent      # .../app
ROOT = APP_DIR.parent                                  # โฟลเดอร์โปรเจกต์
VIEWS = APP_DIR / "views"
PUBLIC = ROOT / "public"                                # โฟลเดอร์ deploy

sys.path.insert(0, str(APP_DIR))
from models.pages import load_pages  # noqa: E402


def build(check_only: bool = False) -> int:
    pages = load_pages()
    env = Environment(
        loader=FileSystemLoader([VIEWS, VIEWS / "pages"]),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    PUBLIC.mkdir(exist_ok=True)

    written, unchanged, drift = 0, 0, []
    for name, meta in sorted(pages.items()):
        html = env.get_template(name).render(page=meta, pages=pages)
        dest = PUBLIC / name
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

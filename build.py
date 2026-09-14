#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — entry point: เรียก Controller ให้ประกอบ Model + View ออกมาเป็น static HTML

โครงสร้าง MVC
    app/models/pages.py     Model      — โหลด/ตรวจสอบ metadata ของแต่ละหน้า (pages.json)
    app/models/pages.json   Model      — ข้อมูลดิบ: title, description, เมนูที่ active ของแต่ละหน้า
    app/views/base.html     View       — โครงหน้าเดียว: head · header/nav · footer · script
    app/views/pages/*.html  View       — เนื้อหาเฉพาะหน้า (เฉพาะส่วนใน <main>)
    app/views/partials/     View       — ชิ้นส่วนที่ใช้ร่วมกันหลายหน้า
    app/controllers/build_controller.py
                             Controller — ประกอบ Model + View ออกมาเป็น static HTML ที่ public/
    public/                  โฟลเดอร์ deploy — *.html ที่ build ออกมา (ห้ามแก้)
    public/assets/           CSS · JS · รูป — ต้นฉบับที่แก้ได้ตรง ๆ เก็บที่เดียว build.py ไม่แตะ
    public/assets/data.js    Model ฝั่ง client — หลักสูตร ข่าว ภาควิชา ผู้บริหาร (โหลดตอน runtime)

ผลลัพธ์ยังเป็น static HTML ล้วน ไม่ต้องมี runtime บนเซิร์ฟเวอร์
deploy กับ Vercel / Netlify / GitHub Pages ได้ตรง ๆ — ตั้ง publish/output directory เป็น `public`

    python build.py            # สร้างไฟล์ทั้งหมด
    python build.py --check    # ตรวจว่าไฟล์ที่มีอยู่ตรงกับ template ไหม (ไม่เขียนทับ)

ต้องมี:  pip install -r requirements.txt
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "app"))
from controllers.build_controller import build  # noqa: E402

if __name__ == "__main__":
    sys.exit(build(check_only="--check" in sys.argv))

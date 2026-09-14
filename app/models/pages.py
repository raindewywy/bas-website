#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app/models/pages.py — Model

โหลด metadata ของแต่ละหน้า (title, description, เมนูที่ active) จาก pages.json
ทุกอย่างที่เกี่ยวกับ "ข้อมูลหน้าเว็บมีอะไรบ้าง" อยู่ที่นี่ที่เดียว
Controller (app/controllers/build_controller.py) เรียกใช้ load_pages() เท่านั้น
ไม่อ่านไฟล์ JSON ตรง ๆ
"""
from pathlib import Path
import json

MODELS_DIR = Path(__file__).resolve().parent
PAGES_JSON = MODELS_DIR / "pages.json"


def load_pages() -> dict:
    """คืนค่า dict ของทุกหน้า: { "index.html": {title, description, nav}, ... }"""
    return json.loads(PAGES_JSON.read_text(encoding="utf-8"))

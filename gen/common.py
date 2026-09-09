# -*- coding: utf-8 -*-
"""
เชลล์กลางของเว็บ BAS SWU

ที่มา: ดึง header / nav / mega-menu / mobile drawer / footer / scripts ออกจาก
ไฟล์ HTML ที่มีอยู่จริง (about.html) แทนการเขียนใหม่ — จึงรับประกันว่าหน้าใหม่
ที่สร้างจากไฟล์นี้ใช้เชลล์ชุดเดียวกับหน้าเดิมเป๊ะ ๆ ไม่มีเมนูเพี้ยนระหว่างหน้า

ใช้ร่วมกับ patch_nav.py ซึ่งแก้เมนูในทุกไฟล์พร้อมกัน
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCE_PAGE = ROOT / "about.html"

_MAIN_OPEN = '<main id="main">'
_MAIN_CLOSE = "</main>"


def _read_reference():
    s = REFERENCE_PAGE.read_text(encoding="utf-8")
    a = s.index(_MAIN_OPEN)
    b = s.index(_MAIN_CLOSE) + len(_MAIN_CLOSE)
    return s[:a], s[b:]


def _set_title(head_html: str, title: str, description: str) -> str:
    head_html = re.sub(
        r"<title>.*?</title>",
        "<title>%s</title>" % html.escape(title),
        head_html,
        count=1,
        flags=re.S,
    )
    head_html = re.sub(
        r'(<meta name="description" content=")[^"]*(">)',
        lambda m: m.group(1) + html.escape(description, quote=True) + m.group(2),
        head_html,
        count=1,
    )
    return head_html


def _set_active(head_html: str, active_key: str) -> str:
    # ล้าง current ทั้งหมดก่อน แล้วค่อยติดให้เมนูที่ active — กันสถานะค้างจากหน้าอ้างอิง
    head_html = head_html.replace('class="nav-item current"', 'class="nav-item"')
    if active_key:
        head_html = head_html.replace(
            '<li class="nav-item" data-key="%s">' % active_key,
            '<li class="nav-item current" data-key="%s">' % active_key,
            1,
        )
    return head_html


def breadcrumb(trail):
    """trail = [(label, href|None), ...] — รายการสุดท้ายคือหน้าปัจจุบัน (href=None)"""
    parts = []
    for label, href in trail:
        if href:
            parts.append('<a href="%s">%s</a>' % (href, html.escape(label)))
        else:
            parts.append('<span aria-current="page">%s</span>' % html.escape(label))
    return (
        '<nav class="breadcrumb wrap" aria-label="เส้นทางหน้าเว็บ">'
        + '<span class="sep" aria-hidden="true">/</span>'.join(parts)
        + "</nav>"
    )


def page(filename: str, title: str, description: str, active_key: str, body: str) -> Path:
    head, tail = _read_reference()
    head = _set_title(head, title, description)
    head = _set_active(head, active_key)
    out = ROOT / filename
    out.write_text(head + _MAIN_OPEN + "\n" + body + "\n" + _MAIN_CLOSE + tail, encoding="utf-8")
    return out

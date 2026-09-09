# -*- coding: utf-8 -*-
"""QA อัตโนมัติ: ลิงก์ตาย / console error / horizontal overflow / h1 / เมนูตรงกันทุกหน้า"""
import glob
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted(p.name for p in ROOT.glob("*.html"))
WIDTHS = [(1400, 900), (768, 900), (390, 844)]

fail = []


def check_links():
    existing = set(PAGES)
    for name in PAGES:
        s = (ROOT / name).read_text(encoding="utf-8")
        for href in set(re.findall(r'href="([^"]+)"', s)):
            if href.startswith(("http", "mailto:", "#", "data:", "tel:")):
                continue
            target = urlparse(href).path
            if not target:
                continue
            if target.startswith("assets/"):
                if not (ROOT / target).exists():
                    fail.append(f"[link] {name} -> {href} (asset missing)")
                continue
            if target not in existing:
                fail.append(f"[link] {name} -> {href} (page missing)")


def check_nav_consistency():
    sigs = {}
    for name in PAGES:
        s = (ROOT / name).read_text(encoding="utf-8")
        m = re.search(r'<ul class="nav-list">.*?</ul>', s, re.S)
        if not m:
            fail.append(f"[nav] {name} has no nav-list")
            continue
        sig = m.group(0).replace('class="nav-item current"', 'class="nav-item"')
        sigs.setdefault(sig, []).append(name)
    if len(sigs) > 1:
        for sig, names in sigs.items():
            fail.append(f"[nav] variant used by: {', '.join(names)}")


def main():
    check_links()
    check_nav_consistency()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name in PAGES:
            for w, h in WIDTHS:
                pg = b.new_page(viewport={"width": w, "height": h})
                errs = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.goto((ROOT / name).as_uri(), wait_until="networkidle")
                sw = pg.evaluate("document.documentElement.scrollWidth")
                cw = pg.evaluate("document.documentElement.clientWidth")
                if sw > cw + 1:
                    fail.append(f"[overflow] {name} @{w}px scrollWidth={sw} clientWidth={cw}")
                if w == 1400:
                    n = pg.locator("h1").count()
                    if n != 1:
                        fail.append(f"[h1] {name} has {n} h1")
                    txt = pg.evaluate("document.body.innerText")
                    if "�" in txt or "â€" in txt:
                        fail.append(f"[mojibake] {name}")
                for e in errs:
                    # โหลดฟอนต์จาก Google Fonts ถูกบล็อกในแซนด์บ็อกซ์ QA — ไม่ใช่บั๊กของเว็บ
                    if "ERR_TUNNEL_CONNECTION_FAILED" in e or "fonts.g" in e:
                        continue
                    fail.append(f"[console] {name} @{w}px: {e[:160]}")
                pg.close()
        b.close()

    print(f"pages checked: {len(PAGES)}")
    if fail:
        print(f"\nISSUES ({len(fail)}):")
        for f in fail:
            print(" -", f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()

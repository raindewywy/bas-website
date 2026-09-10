#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_bas2_media.py — ดึงรูปจาก bas2.swu.ac.th มาเก็บในเครื่อง (รันบนเครื่องคุณ)

ทำ 3 อย่าง:
  1) REQ §9.3  ดาวน์โหลดรูปผู้บริหารที่ยัง hotlink อยู่ -> assets/media/leaders/
                แล้วแก้ src ใน templates/pages/*.html ให้ชี้ path ในเครื่อง
                (แก้ที่ template แล้วรัน build.py ไม่ใช่แก้ .html ที่ root)
  2) REQ-E1    ดาวน์โหลด banner Green Office -> assets/media/banner-greenoffice.jpg
  3) REQ-E2    ดาวน์โหลดรูปแกลเลอรี Green Office -> assets/media/greenoffice-*.jpg

ทุกไฟล์ถูกย่อ/บีบตามข้อกำหนด §6 (กว้างสุด 1600px, JPEG q82) และตั้งชื่อ ASCII ตัวพิมพ์เล็ก

    python gen/fetch_bas2_media.py             # ทำจริง
    python gen/fetch_bas2_media.py --dry-run   # ดูรายการที่จะดาวน์โหลด
    python gen/fetch_bas2_media.py --skip-leaders   # เอาเฉพาะรูป Green Office

ต้องมี: pip install pillow requests
รันซ้ำได้ — ไฟล์ที่มีแล้วจะข้าม
"""
from pathlib import Path
import io
import re
import sys

try:
    import requests
    from PIL import Image
except ImportError:
    sys.exit("!! ต้องติดตั้งก่อน:  pip install pillow requests")

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "assets" / "media"
LEADERS_DIR = MEDIA / "leaders"

BASE = "https://bas2.swu.ac.th/Portals/64/BlockBuilderImages"
MAX_W = 1600
QUALITY = 82
UA = {"User-Agent": "Mozilla/5.0 (compatible; bas-website-asset-fetch/1.0)"}

# ---- REQ-E1 / REQ-E2 ------------------------------------------------------
GREEN_OFFICE = [
    (f"{BASE}/23855/GreenOffice1600x6003.jpg", "banner-greenoffice.jpg"),
    (f"{BASE}/23856/logo-150x150.png", "greenoffice-logo.png"),
    (f"{BASE}/23856/02-9.jpg", "greenoffice-01.jpg"),
    (f"{BASE}/25323/หมวด2-1.jpg", "greenoffice-02.jpg"),
    (f"{BASE}/24195/Picture2-removebg-preview1.png", "greenoffice-03.png"),
    (f"{BASE}/24195/Picture2-removebg-preview2.png", "greenoffice-04.png"),
    (f"{BASE}/24195/Picture2-removebg-preview3.png", "greenoffice-05.png"),
]


def slugify(name):
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return stem or "image"


def save(content, dest, keep_alpha=False):
    im = Image.open(io.BytesIO(content))
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(MAX_W * im.height / im.width)), Image.LANCZOS)
    if keep_alpha and im.mode in ("RGBA", "LA", "P"):
        im.convert("RGBA").save(dest, "PNG", optimize=True)
    else:
        im.convert("RGB").save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    return dest.stat().st_size // 1024


def get(url):
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    return r.content


def fetch_leaders(dry):
    urls = set()
    tpl = ROOT / "templates" / "pages"
    pages = sorted(tpl.glob("*.html")) if tpl.is_dir() else sorted(ROOT.glob("*.html"))
    for p in pages:
        urls |= set(re.findall(r'src="(https://bas2\.swu\.ac\.th/[^"]+)"', p.read_text(encoding="utf-8")))
    if not urls:
        print("  ไม่มีรูป hotlink จาก bas2 เหลืออยู่ — ข้าม")
        return
    print(f"  พบรูป hotlink {len(urls)} ไฟล์")
    if not dry:
        LEADERS_DIR.mkdir(parents=True, exist_ok=True)

    mapping = {}
    for url in sorted(urls):
        name = slugify(url.split("/")[-1]) + ".jpg"
        dest = LEADERS_DIR / name
        rel = f"assets/media/leaders/{name}"
        mapping[url] = rel
        if dry:
            print(f"    {url.split('/')[-1]}  ->  {rel}")
            continue
        if dest.exists():
            print(f"    ข้าม (มีแล้ว) {rel}")
            continue
        try:
            kb = save(get(url), dest)
            print(f"    {rel}  {kb} KB")
        except Exception as e:                          # noqa: BLE001
            print(f"    !! ดาวน์โหลดไม่สำเร็จ {url}\n       {e}")
            mapping.pop(url, None)

    if dry or not mapping:
        return
    n = 0
    for p in pages:
        s = p.read_text(encoding="utf-8")
        orig = s
        for url, rel in mapping.items():
            s = s.replace('src="%s"' % url, 'src="%s"' % rel)
        # ไม่ต้องใช้ referrerpolicy อีกแล้วเมื่อรูปอยู่ในเครื่อง
        if s != orig:
            s = s.replace(' referrerpolicy="no-referrer"', "")
            p.write_text(s, encoding="utf-8")
            n += 1
    where = "templates/pages" if (ROOT / "templates" / "pages").is_dir() else "root"
    print(f"  แก้ src ใน {where} {n} ไฟล์ -> path ในเครื่อง")


def fetch_green(dry):
    if not dry:
        MEDIA.mkdir(parents=True, exist_ok=True)
    for url, name in GREEN_OFFICE:
        dest = MEDIA / name
        if dry:
            print(f"    {name}  <-  {url}")
            continue
        if dest.exists():
            print(f"    ข้าม (มีแล้ว) {name}")
            continue
        try:
            kb = save(get(url), dest, keep_alpha=name.endswith(".png"))
            print(f"    {name}  {kb} KB")
        except Exception as e:                          # noqa: BLE001
            print(f"    !! ดาวน์โหลดไม่สำเร็จ {name}\n       {e}")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    print("ดึงรูปจาก bas2.swu.ac.th" + (" (dry-run)" if dry else ""))
    print("\n[1/2] Green Office (REQ-E1 / REQ-E2)")
    fetch_green(dry)
    if "--skip-leaders" not in sys.argv:
        print("\n[2/2] รูปผู้บริหารที่ยัง hotlink (REQ §9.3)")
        fetch_leaders(dry)
    if not dry:
        print("\nเสร็จแล้ว — ขั้นต่อไป:")
        print("  1) python gen/fix_v9_greenoffice.py   (เปิด hero + แกลเลอรี Green Office)")
        print("  2) python build.py                    (สร้าง .html ใหม่จาก template)")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_detint_media.py — REQUIREMENTS v9 · REQ-M2 (ระดับไฟล์รูป)

ปัญหา: ไฟล์ banner-*.jpg ใน assets/media/ ถูก "อาบสีฟ้า" มาตั้งแต่ไฟล์ต้นฉบับ
       (ค่าเฉลี่ย R~55 / G~178 / B~192) ไม่ใช่ overlay ของ CSS
       จึงลบด้วย CSS ไม่ได้ ต้องแก้ที่ตัวไฟล์

วิธี: per-channel levels stretch — ยืดแต่ละ channel กลับเต็มช่วง 0-255
      คืนภาพถ่ายเดิมได้ดีมากเพราะ overlay เป็นสีทึบชั้นเดียว

ปลอดภัย: - สำรองไฟล์เดิมไว้ที่ assets/media/_original-tinted/ ก่อนเขียนทับ
         - ข้ามไฟล์ที่ค่า cast ต่ำอยู่แล้ว (รันซ้ำได้ ไม่ทำให้ภาพเพี้ยนซ้ำ)

    python gen/fix_v9_detint_media.py            # ทำจริง
    python gen/fix_v9_detint_media.py --dry-run  # ดูรายการเฉย ๆ
"""
from pathlib import Path
import shutil
import sys

try:
    from PIL import Image
    import numpy as np
except ImportError:
    sys.exit("!! ต้องติดตั้งก่อน:  pip install pillow numpy")

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "assets" / "media"
BACKUP = MEDIA / "_original-tinted"

CAST_THRESHOLD = 60      # (G+B)/2 - R เกินเท่านี้ถือว่าอาบสีฟ้า
# ไฟล์ที่โทนฟ้าเป็น "งานออกแบบ" ไม่ใช่ overlay — ห้ามแตะ
SKIP = {"exchange-3plus1.jpg", "poster-3plus1.jpg", "tcas69-quota.jpg"}
JPEG_QUALITY = 82


def cast_of(im):
    a = np.asarray(im.convert("RGB").resize((48, 48))).astype(np.float32)
    r, g, b = a[..., 0].mean(), a[..., 1].mean(), a[..., 2].mean()
    return (g + b) / 2 - r


def detint(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    out = np.empty_like(a)
    for c in range(3):
        ch = a[..., c]
        lo, hi = np.percentile(ch, 0.5), np.percentile(ch, 99.5)
        out[..., c] = np.clip((ch - lo) / max(hi - lo, 1.0) * 255.0, 0, 255)
    return Image.fromarray(out.astype(np.uint8))


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    print("REQ-M2 — ลบโทนฟ้าที่อาบมาในไฟล์รูป" + (" (dry-run)" if dry else ""))
    if not MEDIA.exists():
        sys.exit("!! ไม่พบ assets/media")

    targets = []
    for p in sorted(MEDIA.glob("*.jpg")):
        if p.name in SKIP:
            continue
        c = cast_of(Image.open(p))
        if c >= CAST_THRESHOLD:
            targets.append((p, c))

    if not targets:
        print("  ไม่มีไฟล์ที่ติดโทนฟ้าเกินเกณฑ์ — ไม่ต้องแก้")
        sys.exit(0)

    if not dry:
        BACKUP.mkdir(exist_ok=True)
    for p, c in targets:
        if dry:
            print(f"  จะแก้ {p.name}  (cast {c:.0f})")
            continue
        bak = BACKUP / p.name
        if not bak.exists():
            shutil.copy2(p, bak)
        im = detint(Image.open(p))
        im.save(p, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        print(f"  {p.name}: cast {c:.0f} -> {cast_of(Image.open(p)):.0f}   "
              f"{bak.stat().st_size//1024} KB -> {p.stat().st_size//1024} KB")

    if not dry:
        print(f"\n  สำรองไฟล์เดิมไว้ที่ assets/media/_original-tinted/ ({len(targets)} ไฟล์)")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_phase5.py — REQUIREMENTS v9 · เฟส 5
  REQ-C-DEAN2 : ย้าย section #dean-direct จาก contact.html -> leadership.html
  REQ-F1/F2   : contact.html เหลือลิงก์ redirect 1 บรรทัด (คง id เดิมกัน bookmark พัง)
  ตามแก้      : ปุ่มลอยหน้าแรก href -> leadership.html#dean-direct

หมายเหตุ generator: build_contact.py / build_leadership.py / build_home.py
ถูกแก้ให้ตรงกันแล้ว สคริปต์นี้ใช้ patch ไฟล์ HTML ที่ generate ไว้แล้วโดยไม่ต้อง rebuild

รันซ้ำได้ (idempotent)
    python gen/fix_v9_phase5.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

DEAN_SECTION = """<section class="section" id="dean-direct" style="background:var(--paper-dim);">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">สายตรงคณบดี</p>
        <h2 class="bi-heading"><span class="bi-th th-body">สายตรงคณบดี</span><span class="bi-en">Direct Line to the Dean</span></h2>
        <p class="lede th-body">ช่องทางส่งข้อเสนอแนะ ข้อร้องเรียน หรือเรื่องที่ต้องการให้คณบดีรับทราบโดยตรง</p>
      </div>
    </div>
    <div class="split mt-5">
      <div class="split-copy reveal">
        <p class="th-body"><strong>ดร.ณัฐินี ฐานะจาโร</strong> · คณบดี</p>
        <p class="mt-3"><a class="btn dean-mail-btn" href="mailto:natinee@g.swu.ac.th"><i class="fa-solid fa-envelope" aria-hidden="true"></i><span>ส่งอีเมลถึงคณบดีโดยตรง</span></a></p>
        <p class="th-body mt-3"><a class="link-arrow" href="leader-natinee-thanajaro.html">ดูประวัติคณบดี</a></p>
      </div>
      <div class="split-copy reveal">

      </div>
    </div>
  </div>
</section>

"""

CONTACT_REDIRECT = """<section class="section" id="dean-direct" style="background:var(--paper-dim);padding-top:var(--space-5);padding-bottom:var(--space-5);">
  <div class="wrap">
    <p class="th-body">ต้องการติดต่อคณบดีโดยตรง — <a class="link-arrow" href="leadership.html#dean-direct">ไปที่ &ldquo;สายตรงคณบดี&rdquo; ในหน้าผู้บริหารคณะ</a></p>
  </div>
</section>

"""

ITA_MARKER = '<section class="section" style="background:var(--paper-dim);" id="ita">'
FOOTER_MARKER = '<footer class="site-footer">'


def patch_contact():
    p = ROOT / "contact.html"
    s = p.read_text(encoding="utf-8")
    if "leadership.html#dean-direct" in s:
        print("  contact.html: ย้ายแล้ว — ข้าม")
        return None
    start = s.find('<section class="section" id="dean-direct"')
    end = s.find(ITA_MARKER)
    if start < 0 or end < 0 or end < start:
        sys.exit("!! contact.html: หา section #dean-direct หรือ marker #ita ไม่เจอ")
    moved = s[start:end]
    s = s[:start] + CONTACT_REDIRECT + s[end:]
    p.write_text(s, encoding="utf-8")
    print("  contact.html: section #dean-direct -> ลิงก์ redirect 1 บรรทัด")
    return moved


def patch_leadership():
    p = ROOT / "leadership.html"
    s = p.read_text(encoding="utf-8")
    if 'id="dean-direct"' in s:
        print("  leadership.html: มี #dean-direct แล้ว — ข้าม")
        return
    i = s.find(FOOTER_MARKER)
    if i < 0:
        sys.exit("!! leadership.html: หา <footer class=\"site-footer\"> ไม่เจอ")
    s = s[:i] + DEAN_SECTION + s[i:]
    p.write_text(s, encoding="utf-8")
    print("  leadership.html: เพิ่ม section #dean-direct ต่อท้ายก่อน footer")


def patch_links():
    n = 0
    for f in sorted(ROOT.glob("*.html")):
        s = f.read_text(encoding="utf-8")
        if "contact.html#dean-direct" not in s:
            continue
        f.write_text(s.replace("contact.html#dean-direct", "leadership.html#dean-direct"), encoding="utf-8")
        print(f"  {f.name}: แก้ลิงก์ -> leadership.html#dean-direct")
        n += 1
    if not n:
        print("  ไม่มีลิงก์ contact.html#dean-direct เหลืออยู่")


if __name__ == "__main__":
    print("REQ-C-DEAN2 · REQ-F1 · REQ-F2")
    patch_leadership()
    patch_contact()
    patch_links()
    left = [f.name for f in ROOT.glob("*.html")
            if "contact.html#dean-direct" in f.read_text(encoding="utf-8")]
    print("\nตรวจ: ลิงก์ contact.html#dean-direct ที่เหลือ =", len(left), left or "")

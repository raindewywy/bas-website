#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_partners.py — REQUIREMENTS v9 · REQ-A4 (เครือข่ายพันธมิตร)
  - แทน <span class="marquee-item">องค์กรพันธมิตร 0x</span> ที่เป็น placeholder
    ด้วยโลโก้จริงจาก assets/media/partners/
  - เพิ่ม CSS .partner-logo + ปรับ .marquee-item ให้เป็นกรอบใส
  - ปรับหัวข้อ section ให้ตรงกับเนื้อหาจริง (พันธมิตร MOU ไม่ใช่เฉพาะภาคอุตสาหกรรม)

ต้องมีไฟล์ assets/media/partners/*.png ครบก่อนรัน มิฉะนั้นสคริปต์จะหยุด
รันซ้ำได้ (idempotent)
    python gen/fix_v9_partners.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"
INDEX = ROOT / "index.html"
PARTNER_DIR = ROOT / "assets" / "media" / "partners"

# (ชื่อไฟล์, alt = ชื่อองค์กรจริง)
PARTNERS = [
    ("skku.png", "Sungkyunkwan University (SKKU)"),
    ("meiji-university.png", "Meiji University"),
    ("kmitl.png", "สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง"),
    ("swu-social-sciences.png", "คณะสังคมศาสตร์ มหาวิทยาลัยศรีนครินทรวิโรฒ"),
    ("rajinibon-school.png", "โรงเรียนราชินีบน"),
    ("sarasas-witaed-nakhonpathom.png", "โรงเรียนสารสาสน์วิเทศนครปฐม"),
    ("ocsc.png", "สำนักงาน ก.พ."),
    ("nrct.png", "สำนักงานการวิจัยแห่งชาติ (วช.)"),
    ("nia.png", "สำนักงานนวัตกรรมแห่งชาติ (NIA)"),
    ("etda.png", "สำนักงานพัฒนาธุรกรรมทางอิเล็กทรอนิกส์ (ETDA)"),
    ("set.png", "ตลาดหลักทรัพย์แห่งประเทศไทย (SET)"),
    ("gsb.png", "ธนาคารออมสิน"),
    ("finansia.png", "Finansia"),
    ("tax-auditor-association.png", "สมาคมผู้สอบบัญชีภาษีอากรแห่งประเทศไทย"),
    ("flowaccount.png", "FlowAccount"),
    ("big-c-retail.png", "Big C Retail"),
    ("staybridge-suites.png", "Staybridge Suites"),
    ("soho-hospitality.png", "SOHO Hospitality"),
    ("the-blacksmith.png", "The Blacksmith"),
    ("nise.png", "NISE"),
]

OLD_TRACK_START = '<div class="marquee-track"><span class="marquee-item">องค์กรพันธมิตร 01</span>'

OLD_HEAD = ('    <p class="eyebrow">เครือข่ายด้านอาชีพและอุตสาหกรรม</p>\n'
            '    <h3 class="th-body" style="margin-top:.5rem;font-size:1.1rem;color:var(--muted);'
            'font-weight:500;">องค์กรที่บัณฑิตของเราทำงานด้วย และพันธมิตรโครงการ In-House Training</h3>')
NEW_HEAD = ('    <p class="eyebrow">เครือข่ายความร่วมมือ</p>\n'
            '    <h3 class="th-body" style="margin-top:.5rem;font-size:1.1rem;color:var(--muted);'
            'font-weight:500;">หน่วยงาน สถาบันการศึกษา และองค์กรพันธมิตรที่คณะลงนามความร่วมมือ (MOU) '
            'รวมถึงองค์กรที่บัณฑิตของเราทำงานด้วย</h3>')

CSS_MARK = "/* == v9 partners =="
CSS_BLOCK = """

/* == v9 partners == REQ-A4 =============================================
   โลโก้พันธมิตรจริงแทนกล่องข้อความ placeholder
   ===================================================================== */
.marquee-item{
  padding:0 var(--space-4); border:0; background:none; opacity:1;
  height:auto; white-space:normal;
}
.partner-logo{
  height:44px; width:auto; max-width:160px; object-fit:contain;
  filter:grayscale(1); opacity:.62;
  transition:filter var(--dur), opacity var(--dur);
}
.marquee-item:hover .partner-logo{ filter:none; opacity:1; }
@media (max-width:600px){ .partner-logo{ height:34px; max-width:120px; } }
@media (prefers-reduced-motion:reduce){
  .marquee-track{ gap:var(--space-5) var(--space-6); row-gap:var(--space-4); }
}
"""


def build_track():
    # หมายเหตุ: assets/script.js -> initMarqueeClone() ทำ track.innerHTML += track.innerHTML
    # ให้เองอยู่แล้ว จึงใส่ชุดเดียวพอ ไม่งั้นจะได้ 4 ชุดและ DOM บวมโดยไม่จำเป็น
    items = "".join(
        '<span class="marquee-item">'
        '<img class="partner-logo" src="assets/media/partners/%s" alt="%s" '
        'loading="lazy" decoding="async"></span>' % (f, alt)
        for f, alt in PARTNERS
    )
    return '<div class="marquee-track">' + items + "</div>"


def main():
    missing = [f for f, _ in PARTNERS if not (PARTNER_DIR / f).exists()]
    if missing:
        sys.exit("!! ไม่พบไฟล์โลโก้: " + ", ".join(missing))

    s = CSS.read_text(encoding="utf-8")
    if CSS_MARK in s:
        print("  styles.css: มี CSS พันธมิตรแล้ว — ข้าม")
    else:
        CSS.write_text(s.rstrip("\n") + "\n" + CSS_BLOCK, encoding="utf-8")
        print("  styles.css: เพิ่ม .partner-logo")

    h = INDEX.read_text(encoding="utf-8")
    if "partner-logo" in h:
        print("  index.html: marquee ใช้โลโก้จริงแล้ว — ข้าม")
        return
    if OLD_TRACK_START not in h:
        sys.exit("!! index.html: หา marquee-track เดิมไม่เจอ")
    i = h.index(OLD_TRACK_START)
    j = h.index("</div>", i) + len("</div>")
    h = h[:i] + build_track() + h[j:]
    if OLD_HEAD in h:
        h = h.replace(OLD_HEAD, NEW_HEAD, 1)
        print("  index.html: ปรับหัวข้อ section เป็นเครือข่ายความร่วมมือ (MOU)")
    else:
        print("  !! index.html: หาหัวข้อ section เดิมไม่เจอ — ไม่ได้ปรับข้อความ")
    INDEX.write_text(h, encoding="utf-8")
    print(f"  index.html: REQ-A4 ใส่โลโก้ {len(PARTNERS)} องค์กร (script.js โคลนเป็น 2 ชุดตอนรัน)")


if __name__ == "__main__":
    print("REQ-A4 — เครือข่ายพันธมิตร")
    main()

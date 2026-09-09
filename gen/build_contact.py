# -*- coding: utf-8 -*-
"""หน้าติดต่อเรา: จัดใหม่ให้เป็นช่องทางของคณะเป็นหลัก + ติดต่อตามเรื่อง + สายตรงคณบดี"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_leaders import LEADERS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "contact.html"
s = p.read_text(encoding="utf-8")

by = {x["slug"]: x for x in LEADERS}

# แต่ละเรื่อง -> ผู้บริหารที่รับผิดชอบตามตำแหน่งจริง (ไม่ได้เดา — อิงชื่อตำแหน่งบนเว็บทางการ)
TOPICS = [
    ("การรับสมัครและหลักสูตร", "Admissions &amp; Programmes", "phutip-meethavornkul",
     'ดูรายละเอียดหลักสูตรและที่ปรึกษารายหลักสูตรได้ที่ <a href="programs.html#advisors">หน้าหลักสูตร</a>'),
    ("กิจการนิสิตและศิษย์เก่า", "Student Affairs &amp; Alumni", "phetcharat-jinnupong", ""),
    ("วิเทศสัมพันธ์และสื่อสารองค์กร", "International &amp; Communications", "siam-prasertkul",
     'ความร่วมมือระหว่างประเทศดูที่ <a href="international.html">หน้านานาชาติ</a>'),
    ("วิจัยและบริการวิชาการ", "Research &amp; Academic Services", "khomkrit-nantharojphong", ""),
    ("พันธกิจสัมพันธ์เพื่อสังคม / ความร่วมมือกับภาคธุรกิจ", "Social Engagement &amp; Partnerships",
     "jirachai-muenlit", ""),
    ("งานบริหารและธุรการ", "Administration", "jarin-jarusen", ""),
]

rows = "".join(
    '<div class="advisor-card reveal"><h3 class="th-body">%s</h3>'
    '<p class="en" style="color:var(--muted);font-size:.78rem;">%s</p>'
    '<p class="who th-body" style="margin-top:.5rem;">%s · <a href="leader-%s.html">%s</a></p>'
    '<p style="margin-top:.35rem;"><a href="mailto:%s">%s</a></p>%s</div>'
    % (th, en, by[slug]["role_th"], slug, by[slug]["name_th"], by[slug]["email"], by[slug]["email"],
       ('<p class="th-body" style="margin-top:.5rem;font-size:.86rem;">%s</p>' % extra) if extra else "")
    for th, en, slug, extra in TOPICS
)

dean = by["natinee-thanajaro"]

BLOCK = """
<section class="section" id="topics">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">ติดต่อตามเรื่อง</p>
        <h2 class="bi-heading"><span class="bi-th th-body">ติดต่อตามเรื่องที่ต้องการ</span><span class="bi-en">Who to Contact</span></h2>
        <p class="lede th-body">เพื่อลดการติดต่อผิดฝ่าย หน้านี้แยกช่องทางตามเรื่อง โดยระบุผู้บริหารที่รับผิดชอบตามตำแหน่งจริง ส่วนการติดต่อทั่วไปยังใช้เบอร์และอีเมลกลางของคณะด้านบน</p>
      </div>
    </div>
    <div class="advisor-grid mt-5">%s</div>
    <div class="notice th-body" style="margin-top:var(--space-4);"><span>ช่องทางที่แสดงคืออีเมลของผู้บริหารตามตำแหน่ง (ยืนยันจากเว็บไซต์ทางการ) — หากคณะมี <strong>อีเมลกลางรายฝ่าย</strong> หรือเจ้าหน้าที่ผู้ประสานงานแต่ละเรื่อง ควรใช้ช่องทางนั้นแทนอีเมลส่วนบุคคล เพื่อไม่ให้งานติดที่คนคนเดียวและยังใช้ได้เมื่อเปลี่ยนวาระผู้บริหาร</span></div>
  </div>
</section>

<section class="section" id="dean-direct" style="background:var(--paper-dim);">
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
        <p class="th-body"><strong>%s</strong> · %s</p>
        <p class="th-body mt-2"><a href="mailto:%s">%s</a></p>
        <p class="th-body mt-3"><a class="link-arrow" href="leader-%s.html">ดูประวัติคณบดี</a></p>
      </div>
      <div class="split-copy reveal">
        <div class="notice th-body"><span><strong>สิ่งที่ต้องทำก่อนขึ้นจริง:</strong> ช่องทางนี้ควรเป็น<strong>แบบฟอร์มที่ส่งเข้าระบบของสำนักงานคณบดี</strong> ไม่ใช่อีเมลส่วนบุคคล เพราะเรื่องร้องเรียนต้องมีเลขรับเรื่อง ผู้ติดตาม และการเก็บข้อมูลตาม PDPA ต้นแบบนี้จึงแสดงเป็นช่องทางติดต่อไว้ก่อน และรอให้คณะยืนยันว่าจะใช้ฟอร์มหรือระบบใด</span></div>
      </div>
    </div>
  </div>
</section>
""" % (rows, dean["name_th"], dean["role_th"], dean["email"], dean["email"], dean["slug"])

if 'id="topics"' not in s:
    i = s.index('<section class="section" style="background:var(--paper-dim);" id="ita">')
    s = s[:i] + BLOCK + "\n" + s[i:]
    p.write_text(s, encoding="utf-8")
    print("contact.html: topics + dean-direct added")
else:
    print("contact.html: already patched")

# -*- coding: utf-8 -*-
"""
หน้าหลักสูตร: ย้าย 4+1 และช่องทางติดต่อที่ปรึกษามาไว้ใต้แท็บหลักสูตร (ตามที่ประชุม)
+ บล็อกทางเข้าหลักสูตรบัณฑิตศึกษา (ลิงก์ออกนอกเว็บอย่างมีบริบท)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_leaders import LEADERS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "programs.html"
s = p.read_text(encoding="utf-8")

EXT = ('<svg class="ext-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'aria-hidden="true"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/>'
       '<path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>')

heads = [x for x in LEADERS if x["group"] == "dept_head"]

advisor_cards = "".join(
    '<div class="advisor-card reveal"><h3 class="th-body">%s</h3>'
    '<p class="who th-body">หัวหน้าภาควิชา · <a href="leader-%s.html">%s</a></p>'
    '<p style="margin-top:.5rem;"><a href="mailto:%s">%s</a></p></div>'
    % (h["dept_th"], h["slug"], h["name_th"], h["email"], h["email"])
    for h in heads
)

BLOCK = """
<section class="section" id="graduate-entry" style="background:var(--paper-dim);">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">บัณฑิตศึกษา</p>
        <h2 class="bi-heading"><span class="bi-th th-body">หลักสูตรปริญญาโทและปริญญาเอก</span><span class="bi-en">Graduate Programmes</span></h2>
        <p class="lede th-body">หลักสูตรระดับบัณฑิตศึกษาของคณะดูแลโดยศูนย์การจัดการหลักสูตรระดับบัณฑิตศึกษา ครอบคลุมปริญญาโท 3 แขนง (การตลาด · การจัดการ · ธุรกิจเพื่อสังคม) และปริญญาเอกบริหารธุรกิจเพื่อสังคม</p>
      </div>
    </div>
    <p class="th-body" style="display:flex;gap:.7rem;flex-wrap:wrap;margin-top:var(--space-4);">
      <a class="btn btn-primary" href="programs.html?level=graduate">ดูสรุปหลักสูตรบัณฑิตศึกษาในเว็บคณะ</a>
      <a class="btn btn-secondary" href="https://mba.swu.ac.th/" target="_blank" rel="noopener"
         aria-label="ไปเว็บไซต์หลักสูตรบัณฑิตศึกษา mba.swu.ac.th (เปิดในแท็บใหม่)">ไปเว็บไซต์หลักสูตรบัณฑิตศึกษา %s</a>
    </p>
    <div class="notice th-body" style="margin-top:var(--space-4);"><span>ที่ประชุมขอให้กดแล้วไปเว็บ MBA โดยตรง — ฝั่งออกแบบเสนอให้คงหน้าสรุปฝั่งเว็บคณะไว้ก่อนแล้วมีปุ่มออกไปชัดเจน เพราะผู้สมัคร ป.โท/ป.เอก มักเปรียบเทียบหลายสถาบัน ถ้าเว็บคณะไม่มีข้อมูลเลยจะเสียทั้งการค้นหาบน Google และความน่าเชื่อถือ หากยืนยันว่าต้องการให้เด้งออกทันที ปรับได้ที่จุดเดียว</span></div>
  </div>
</section>

<section class="section" id="plan41">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">เส้นทางการศึกษา</p>
        <h2 class="bi-heading"><span class="bi-th th-body">หลักสูตร 4+1</span><span class="bi-en">Bachelor + Master (4+1)</span></h2>
        <p class="lede th-body">เส้นทางเรียนต่อเนื่องปริญญาตรีควบปริญญาโท ย้ายมาอยู่ใต้แท็บหลักสูตรตามมติที่ประชุม จากเดิมที่อยู่ในแท็บย่อยอื่น</p>
      </div>
    </div>
    <div class="plan41 th-body mt-4">
      <p>แนวคิดของเส้นทาง 4+1 คือให้นิสิตปริญญาตรีที่มีผลการเรียนตามเกณฑ์ ลงทะเบียนเรียนรายวิชาระดับปริญญาโทล่วงหน้าในช่วงปลายปริญญาตรี แล้วเรียนต่อจนจบปริญญาโทได้ในเวลาที่สั้นลง</p>
      <ol>
        <li>เรียนปริญญาตรีตามหลักสูตรปกติ และสะสมหน่วยกิตรายวิชาระดับบัณฑิตศึกษาตามเงื่อนไข</li>
        <li>สำเร็จปริญญาตรี แล้วเข้าศึกษาต่อระดับปริญญาโท</li>
        <li>ใช้เวลาระดับปริญญาโทสั้นลง เพราะเทียบโอนหน่วยกิตที่สะสมไว้</li>
      </ol>
      <div class="notice th-body" style="margin-top:var(--space-4);"><span><strong>ต้องได้ข้อมูลจริงจากคณะ</strong> — เกณฑ์ GPA ขั้นต่ำ · หลักสูตรปริญญาตรีที่เข้าร่วมได้ · รายวิชาที่เทียบโอนได้ · จำนวนหน่วยกิต · ระยะเวลารวม · ช่วงเวลาสมัคร ยังไม่ได้รับ จึงยังไม่ใส่ตัวเลขใด ๆ ในหน้านี้ (ไม่ใส่ข้อมูลสมมติ) ขอเนื้อหา 4+1 จากแท็บเดิมบนเว็บไซต์ปัจจุบันเพื่อย้ายมาให้ครบ</span></div>
    </div>
  </div>
</section>

<section class="section" id="advisors" style="background:var(--paper-dim);">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">สอบถามเรื่องหลักสูตร</p>
        <h2 class="bi-heading"><span class="bi-th th-body">ติดต่อที่ปรึกษาหลักสูตร</span><span class="bi-en">Programme Advisors</span></h2>
        <p class="lede th-body">ย้ายมาจากหน้าติดต่อเราตามมติที่ประชุม — คนที่กำลังดูหลักสูตรอยู่ควรหาผู้ให้คำปรึกษาได้จากหน้าเดียวกัน ไม่ต้องย้อนไปหน้าติดต่อ</p>
      </div>
    </div>
    <div class="advisor-grid mt-5">%s</div>
    <div class="notice th-body" style="margin-top:var(--space-4);"><span>ขณะนี้แสดงผู้ติดต่อระดับภาควิชา (ข้อมูลยืนยันแล้วจากเว็บไซต์ทางการ) — <strong>รายชื่ออาจารย์ที่ปรึกษารายหลักสูตรพร้อมอีเมล/เบอร์/ช่องทางไลน์</strong> ยังต้องขอจากคณะ เมื่อได้รับจะแยกเป็นรายหลักสูตรทั้ง 9 หลักสูตร</span></div>
    <p style="margin-top:var(--space-4);"><a class="link-arrow" href="contact.html">ติดต่อสำนักงานคณะ (เรื่องทั่วไป / ธุรการ)</a></p>
  </div>
</section>
""" % (EXT, advisor_cards)

if "id=\"plan41\"" not in s:
    s = s.replace("</main>", BLOCK + "</main>", 1)
    p.write_text(s, encoding="utf-8")
    print("programs.html: graduate entry + 4+1 + advisors added")
else:
    print("programs.html: already patched")

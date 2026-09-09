# -*- coding: utf-8 -*-
"""หน้าใหม่ใต้ 'เกี่ยวกับคณะ': เกียรติภูมิ BAS · Green Award · นานาชาติ"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

NOTE_ICON = ""


def notice(text):
    return '<div class="notice th-body"><span>%s</span></div>' % text


def hero(eyebrow, th, en, lede):
    return (
        '<section class="page-hero"><div class="wrap">'
        '<p class="eyebrow th-body">%s</p>'
        '<h1 class="bi-heading"><span class="bi-th th-body">%s</span><span class="bi-en">%s</span></h1>'
        '<p class="lede th-body">%s</p>'
        "</div></section>" % (eyebrow, th, en, lede)
    )


def crumbs(label):
    return common.breadcrumb(
        [("หน้าแรก", "index.html"), ("เกี่ยวกับคณะ", "about.html"), (label, None)]
    )


# ------------------------------------------------------------ เกียรติภูมิ ----
HONOUR_GROUPS = [
    ("awards", "รางวัลระดับคณะและมหาวิทยาลัย", "Faculty &amp; University Awards",
     "รางวัลและการรับรองคุณภาพที่คณะได้รับ ทั้งในระดับมหาวิทยาลัย ระดับชาติ และระดับนานาชาติ"),
    ("students", "ความสำเร็จของนิสิต", "Student Achievements",
     "ผลงานการแข่งขัน โครงการที่ได้รับรางวัล และความสำเร็จของนิสิตปัจจุบัน"),
    ("alumni", "ศิษย์เก่าที่โดดเด่น", "Distinguished Alumni",
     "เส้นทางอาชีพของศิษย์เก่าที่สร้างผลกระทบทางธุรกิจและสังคม"),
]

honours_body = [
    crumbs("เกียรติภูมิ BAS"),
    hero("เกี่ยวกับคณะ", "เกียรติภูมิ BAS", "Honours &amp; Awards",
         "รางวัล ผลงาน และความสำเร็จที่สะท้อนคุณภาพการศึกษาและพันธกิจเพื่อสังคมของคณะ"),
    '<section class="section"><div class="wrap">',
    notice('<strong>ชื่อเมนูยังเป็นชื่อชั่วคราว</strong> — ที่ประชุมเสนอชื่อ "Hall of Fame" '
           'ข้อเสนอจากฝั่งออกแบบคือใช้ชื่อไทยเป็นหลักให้สอดคล้องกับทั้งเว็บ เช่น '
           '"เกียรติภูมิ BAS / Honours &amp; Awards" หรือ "ความภาคภูมิใจ / Achievements" '
           'โปรดยืนยันชื่อที่ต้องการก่อนเผยแพร่'),
    '<div class="honour-grid mt-5">'
    + "".join(
        '<div class="honour-card reveal"><h3 class="th-body">%s</h3>'
        '<p class="en" style="color:var(--muted);font-size:.8rem;margin-bottom:.5rem;">%s</p>'
        '<p>%s</p></div>' % (th, en, desc)
        for _k, th, en, desc in HONOUR_GROUPS
    )
    + "</div>",
]
for k, th, en, desc in HONOUR_GROUPS:
    honours_body.append(
        '<div class="profile-section" id="%s"><h2 class="th-body">%s '
        '<span style="color:var(--muted);font-size:.6em;font-weight:400;">%s</span></h2>'
        '<p class="th-body" style="color:var(--muted);margin-bottom:var(--space-3);">%s</p>%s</div>'
        % (k, th, en, desc,
           notice("ยังไม่มีข้อมูลในส่วนนี้ — รอรายการรางวัล/ผลงานพร้อมปีที่ได้รับจากคณะ "
                  "หน้านี้จัดโครงไว้พร้อมแล้ว เติมข้อมูลได้ทันทีเมื่อได้รับ (ไม่ใส่ข้อมูลสมมติ)"))
    )
honours_body.append("</div></section>")

common.page(
    "honours.html",
    "เกียรติภูมิ BAS — BAS SWU",
    "รางวัล ผลงาน และความสำเร็จของคณะ นิสิต และศิษย์เก่า คณะบริหารธุรกิจเพื่อสังคม มศว",
    "about",
    "\n".join(honours_body),
)

# ----------------------------------------------------------- Green Award ----
green_body = [
    crumbs("Green Award"),
    hero("เกี่ยวกับคณะ", "Green Award", "Green Award",
         "รางวัลและการดำเนินงานด้านความยั่งยืนและสิ่งแวดล้อมของคณะบริหารธุรกิจเพื่อสังคม"),
    '<section class="section"><div class="wrap">',
    notice("<strong>รอเนื้อหาจากเว็บไซต์เดิม</strong> — ที่ประชุมระบุให้ย้าย Green Award "
           "จากเว็บเดิมมาไว้ใต้แท็บเกี่ยวกับคณะ แต่ยังไม่ได้รับ URL ของหน้าเดิม "
           "และค้นหาแล้วยังไม่พบหน้าดังกล่าวบนเว็บทางการ ขอ URL หรือไฟล์เนื้อหาเดิม "
           "(ข้อความ ภาพ ปีที่ได้รับรางวัล) เพื่อย้ายมาให้ครบถ้วน"),
    '<div class="profile-section"><h2 class="th-body">โครงหน้าที่เตรียมไว้</h2>'
    '<ul class="edu-list th-body">'
    "<li>ที่มาและความหมายของรางวัล / เกณฑ์การประเมิน</li>"
    "<li>ปีที่คณะได้รับ และระดับของรางวัล</li>"
    "<li>โครงการหรือแนวปฏิบัติที่ทำให้ได้รับรางวัล</li>"
    "<li>ภาพกิจกรรมและเอกสารอ้างอิง</li>"
    "<li>ความเชื่อมโยงกับพันธกิจ &ldquo;ธุรกิจเพื่อสังคม&rdquo; ของคณะ</li>"
    "</ul></div>",
    '<div class="profile-section">'
    + notice("<strong>ข้อเสนอเชิงโครงสร้าง:</strong> Green Award ไม่ควรเป็นรายการลอย ๆ "
             "แต่ควรอยู่ในกลุ่มเนื้อหา &ldquo;ความยั่งยืนและผลกระทบทางสังคม&rdquo; ร่วมกับงาน "
             "พันธกิจสัมพันธ์เพื่อสังคมของคณะ เพื่อให้เล่าเรื่องจุดยืนของคณะได้ต่อเนื่อง "
             "ไม่ใช่แค่แสดงว่าเคยได้รางวัล")
    + "</div>",
    "</div></section>",
]
common.page(
    "green-award.html",
    "Green Award — BAS SWU",
    "รางวัลและการดำเนินงานด้านความยั่งยืนของคณะบริหารธุรกิจเพื่อสังคม มศว",
    "about",
    "\n".join(green_body),
)

# -------------------------------------------------------------- นานาชาติ ----
inter_body = [
    crumbs("นานาชาติ"),
    hero("เกี่ยวกับคณะ", "นานาชาติ", "International",
         "โอกาสแลกเปลี่ยน เส้นทางปริญญาคู่ และความร่วมมือกับสถาบันในต่างประเทศ"),
    '<section class="section"><div class="wrap">',
    notice('<strong>หมายเหตุการออกแบบ:</strong> ที่ประชุมเสนอทำเป็น pop-up ชื่อ "Inter" '
           'แทน "Be Go" เดิม ฝั่งออกแบบเสนอทำเป็น<strong>หน้าจริง</strong>แทน pop-up '
           'เพราะเนื้อหาความร่วมมือระหว่างประเทศต้องแชร์ลิงก์ได้ ค้นหาใน Google เจอ '
           'และใช้งานบนมือถือได้ — เมนูย่อยในแถบเมนูยังชี้มาที่หัวข้อในหน้านี้เหมือนเดิม '
           'ส่วนชื่อเสนอใช้ "นานาชาติ / International" แทน "Inter" เพื่อให้สื่อกับผู้อ่านต่างชาติ'),

    '<div class="profile-section" id="exchange"><h2 class="th-body">Exchange 3+1 '
    '<span style="color:var(--muted);font-size:.6em;font-weight:400;">Exchange &amp; Double Degree</span></h2>'
    '<p class="th-body">นิสิตหลักสูตรการจัดการธุรกิจโลก (Global Business Management) '
    'ซึ่งสอนเป็นภาษาอังกฤษทั้งหลักสูตร มีเส้นทางปริญญาคู่แบบ 3+1 — เรียนที่ มศว 3 ปี '
    'และไปเรียนกับสถาบันพันธมิตรในต่างประเทศอีก 1 ปี</p>'
    '<div class="honour-grid mt-4">'
    '<div class="honour-card"><h3 class="th-body">Frankfurt School of Finance &amp; Management</h3>'
    '<p>สถาบันพันธมิตรในประเทศเยอรมนี สำหรับโครงการแลกเปลี่ยนและเส้นทางปริญญาคู่</p></div>'
    '<div class="honour-card"><h3 class="th-body">Brokenshire College</h3>'
    '<p>สถาบันพันธมิตรในประเทศฟิลิปปินส์ ลงนามบันทึกข้อตกลงความร่วมมือ (MOU) ร่วมกับ มศว</p></div>'
    '<div class="honour-card"><h3 class="th-body">University of York</h3>'
    '<p>คณะผู้แทนเข้าเยี่ยมชมคณะเพื่อหารือความร่วมมือทางวิชาการ</p></div>'
    "</div>"
    '<p style="margin-top:var(--space-4);"><a class="link-arrow" href="student-life.html#exchange">'
    'รายละเอียดโครงการแลกเปลี่ยนในหน้าชีวิตนิสิต</a></p>'
    "</div>",

    '<div class="profile-section" id="collaboration"><h2 class="th-body">Collaboration '
    '<span style="color:var(--muted);font-size:.6em;font-weight:400;">ความร่วมมือทางวิชาการ</span></h2>'
    '<p class="th-body">ความร่วมมือทางวิชาการ การลงนาม MOU การบรรยายพิเศษโดยวิทยากรต่างประเทศ '
    'และการต้อนรับคณะผู้แทนจากสถาบันในต่างประเทศ</p>'
    + notice("รายการความร่วมมือฉบับเต็ม (ชื่อสถาบัน ปีที่ลงนาม ขอบเขตความร่วมมือ อายุข้อตกลง) "
             "ยังต้องขอจากฝ่ายวิเทศสัมพันธ์ ตอนนี้หน้านี้แสดงเฉพาะความร่วมมือที่ยืนยันได้จาก "
             "ข่าวบนเว็บไซต์ทางการเท่านั้น")
    + '<p style="margin-top:var(--space-4);"><a class="link-arrow" href="news.html?cat=inter">'
    'ดูข่าวหมวดความร่วมมือและนานาชาติทั้งหมด</a></p>'
    "</div>",

    '<div class="profile-section"><h2 class="th-body">ผู้ประสานงาน</h2>'
    '<p class="th-body">ผู้ช่วยคณบดีฝ่ายวิเทศสัมพันธ์และสื่อสารองค์กร — '
    '<a href="leader-siam-prasertkul.html">ดร.สยาม ประเสริฐกุล</a> '
    '(<a href="mailto:siamp@g.swu.ac.th">siamp@g.swu.ac.th</a>)</p></div>',
    "</div></section>",
]
common.page(
    "international.html",
    "นานาชาติ — BAS SWU",
    "โอกาสแลกเปลี่ยน Exchange 3+1 และความร่วมมือระหว่างประเทศของคณะบริหารธุรกิจเพื่อสังคม มศว",
    "about",
    "\n".join(inter_body),
)

print("built honours.html / green-award.html / international.html")

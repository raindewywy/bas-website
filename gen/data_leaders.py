# -*- coding: utf-8 -*-
"""
ข้อมูลผู้บริหาร BAS SWU — ดึงจากเว็บไซต์ทางการ 2 แหล่ง (ตรวจสอบข้ามกันแล้ว)
  - https://bas.swu.ac.th/about                (หน้าผู้บริหาร)
  - https://bas2.swu.ac.th/executive-committee (หน้าผู้บริหาร)
  - หน้าโปรไฟล์รายบุคคลบน bas2.swu.ac.th      (ประวัติการศึกษา / ความเชี่ยวชาญ / CV)
ตรวจล่าสุด: 5 ก.ย. 2026

หมายเหตุสำคัญ: ชื่อภาษาไทยในชุดนี้ยึดตามเว็บทางการ ไม่ใช่การถอดเสียงกลับจาก
ชื่อภาษาอังกฤษ (ต้นแบบรุ่นก่อนสะกดผิดหลายคนเพราะถอดเสียงกลับ)

ORDER = คณบดี -> รองคณบดี -> ผู้ช่วยคณบดี -> หัวหน้าภาควิชา
"""

GROUPS = [
    ("dean",           "คณบดี",             "Dean"),
    ("vice_dean",      "รองคณบดี",          "Associate Deans"),
    ("assistant_dean", "ผู้ช่วยคณบดี",       "Assistant Deans"),
    ("dept_head",      "หัวหน้าภาควิชา",     "Department Heads"),
]

CV_BASE = "https://bas2.swu.ac.th/Portals/64/CV/"

LEADERS = [
    dict(
        slug="natinee-thanajaro", group="dean",
        name_th="ดร.ณัฐินี ฐานะจาโร", name_en="Dr. Natinee Thanajaro",
        role_th="คณบดี", role_en="Dean",
        dept_th="ภาควิชาบริหารธุรกิจ", dept_en="Department of Business Administration",
        email="natinee@g.swu.ac.th",
        cert_th="ได้รับการรับรองคุณภาพการจัดการเรียนการสอนตามกรอบมาตรฐานวิชาชีพของสหราชอาณาจักร UKPSF ในระดับ Fellow (FHEA)",
        edu=[
            "B.A. (British and American Studies) มหาวิทยาลัยธรรมศาสตร์",
            "M.Sc. (Business Management) University of East Anglia, UK",
            "M.Res. (Accounting) University of Essex, UK",
            "Ph.D. (Marketing) Brunel University, UK",
        ],
        expertise_th="บริหารธุรกิจ การตลาด การบัญชี",
        cv=CV_BASE + "07-CV-natinee_thanajaro.pdf",
        source="https://bas2.swu.ac.th/teacher/inter_program/natinee",
    ),
    dict(
        slug="jarin-jarusen", group="vice_dean",
        name_th="ผู้ช่วยศาสตราจารย์ ดร.จรินทร์ จารุเสน", name_en="Asst. Prof. Dr. Jarin Jarusen",
        role_th="รองคณบดีฝ่ายบริหาร", role_en="Associate Dean for Administration",
        dept_th="ภาควิชาบัญชีและการเงิน", dept_en="Department of Accounting and Finance",
        email="jarin@g.swu.ac.th",
        edu=[
            "บธ.บ. (การบัญชี) มหาวิทยาลัยรามคำแหง",
            "บธ.ม. (การเงินและการธนาคาร) มหาวิทยาลัยรามคำแหง",
            "บธ.ด. (การจัดการ) มหาวิทยาลัยรามคำแหง",
        ],
        expertise_th="การบัญชี การเงินและการธนาคาร",
        cv=CV_BASE + "02-CV-asst_prof_jarin_jarusen.pdf",
        source="https://bas2.swu.ac.th/program/finance/teacher/jarin",
    ),
    dict(
        slug="phutip-meethavornkul", group="vice_dean",
        name_th="ผู้ช่วยศาสตราจารย์ ดร.ภูธิป มีถาวรกุล", name_en="Asst. Prof. Dr. Phutip Meethavornkul",
        role_th="รองคณบดีฝ่ายวิชาการ", role_en="Associate Dean for Academic Affairs",
        dept_th="ภาควิชาบริหารธุรกิจ", dept_en="Department of Business Administration",
        email="phutip@g.swu.ac.th",
        edu=[
            "ศ.บ. (ออกแบบนิเทศศิลป์) มหาวิทยาลัยรังสิต",
            "วท.ม. (การจัดการโรงแรมและการท่องเที่ยว) มหาวิทยาลัยนเรศวร",
            "MITH (International Hotel and Tourism) Southern Cross University, Australia",
            "ปร.ด. (การจัดการ) มหาวิทยาลัยศิลปากร",
        ],
        expertise_th="การจัดการบริหารธุรกิจเพื่อสังคม การจัดการโรงแรมและท่องเที่ยว การออกแบบสื่อประชาสัมพันธ์",
        cv=CV_BASE + "08-CV-phutip_meethavornkul.pdf",
        source="https://bas2.swu.ac.th/program/social_enterprise/phutip",
    ),
    dict(
        slug="kanyakit-keeratiangkoon", group="vice_dean",
        name_th="ผู้ช่วยศาสตราจารย์ ดร.กัลยกิตติ์ กีรติอังกูร", name_en="Asst. Prof. Dr. Kanyakit Keeratiangkoon",
        role_th="รองคณบดีฝ่ายแผนและพัฒนาองค์กร", role_en="Associate Dean for Planning and Organisational Development",
        dept_th="ภาควิชาบัญชีและการเงิน", dept_en="Department of Accounting and Finance",
        email="kanyakit@g.swu.ac.th",
        edu=[
            "บธ.บ. (การบัญชี) มหาวิทยาลัยศรีนครินทรวิโรฒ",
            "วศ.ม. (เทคโนโลยีสารสนเทศทางธุรกิจ) จุฬาลงกรณ์มหาวิทยาลัย",
            "ปร.ด. (ธุรกิจเทคโนโลยีและการจัดการนวัตกรรม) จุฬาลงกรณ์มหาวิทยาลัย",
        ],
        expertise_th="ระบบสารสนเทศทางบัญชี เทคโนโลยีสารสนเทศ การวิเคราะห์และออกแบบระบบสารสนเทศ การจัดการนวัตกรรม",
        cv=CV_BASE + "accountancy/06-CV-kanyakit_keeratiangkoon.pdf",
        source="https://bas2.swu.ac.th/program/accountancy/teacher/kanyakit",
    ),
    dict(
        slug="phetcharat-jinnupong", group="vice_dean",
        name_th="ผู้ช่วยศาสตราจารย์ ดร.เพชรรัตน์ จินต์นุพงศ์", name_en="Asst. Prof. Dr. Phetcharat Jinnupong",
        role_th="รองคณบดีฝ่ายกิจการนิสิตและศิษย์เก่าสัมพันธ์", role_en="Associate Dean for Student Affairs and Alumni Relations",
        dept_th="ภาควิชาบริหารธุรกิจ", dept_en="Department of Business Administration",
        email="phetcharat@g.swu.ac.th",
        edu=[
            "ศศ.บ. (การจัดการโรงแรมและการท่องเที่ยว) มหาวิทยาลัยศรีปทุม",
            "บธ.ม. (การจัดการ) มหาวิทยาลัยรามคำแหง",
            "บธ.ด. (การจัดการ) มหาวิทยาลัยรามคำแหง",
        ],
        expertise_th="การจัดการ การจัดการกลยุทธ์ การจัดการทรัพยากรมนุษย์",
        cv=CV_BASE + "05-CV-phetcharat_jinnupong.pdf",
        source="https://bas2.swu.ac.th/program/marketing/teacher/phetcharat",
    ),
    dict(
        slug="khomkrit-nantharojphong", group="assistant_dean",
        name_th="ผู้ช่วยศาสตราจารย์ ดร.คมกริช นันทะโรจพงศ์", name_en="Asst. Prof. Dr. Khomkrit Nantharojphong",
        role_th="ผู้ช่วยคณบดีฝ่ายวิจัย", role_en="Assistant Dean for Research",
        dept_th="ภาควิชาบริหารธุรกิจ", dept_en="Department of Business Administration",
        email="khomkrit@g.swu.ac.th",
        edu=[
            "บธ.บ. (ระบบสารสนเทศคอมพิวเตอร์) มหาวิทยาลัยรังสิต",
            "วท.ม. (เทคโนโลยีการบริหาร — การจัดการประยุกต์) สถาบันบัณฑิตพัฒนบริหารศาสตร์",
            "ปร.ด. (การจัดการ) มหาวิทยาลัยศิลปากร",
        ],
        expertise_th="การจัดการธุรกิจเพื่อสังคม การจัดการทุนมนุษย์ เทคโนโลยีการจัดการ พฤติกรรมและการพัฒนาองค์กร",
        cv=CV_BASE + "social_enterprise/06-CV-assistant_professor_dr_khomkrit_nantharojphong.pdf",
        source="https://bas2.swu.ac.th/program/social_enterprise/khomkrit",
    ),
    dict(
        slug="siam-prasertkul", group="assistant_dean",
        name_th="ดร.สยาม ประเสริฐกุล", name_en="Dr. Siam Prasertkul",
        role_th="ผู้ช่วยคณบดีฝ่ายวิเทศสัมพันธ์และสื่อสารองค์กร", role_en="Assistant Dean for International Relations and Corporate Communications",
        dept_th="ภาควิชาบริหารธุรกิจ", dept_en="Department of Business Administration",
        email="siamp@g.swu.ac.th",
        edu=[
            "วท.บ. (เทคโนโลยีชีวภาพ) สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง",
            "MBA (Marketing) Queensland University of Technology, Australia",
            "บธ.ด. (การจัดการ) มหาวิทยาลัยรามคำแหง",
        ],
        expertise_th="การจัดการและการบริหารธุรกิจ การตลาดและการบริหารงานขาย ภาษาอังกฤษธุรกิจ",
        cv=CV_BASE + "inter_global_business/04-CV-dr_siam_prasertkul.pdf",
        source="https://bas2.swu.ac.th/teacher/inter_program/siam",
    ),
    dict(
        slug="jirachai-muenlit", group="assistant_dean",
        name_th="ดร.จิรชัย หมื่นฤทธิ์", name_en="Dr. Jirachai Muenlit",
        role_th="ผู้ช่วยคณบดีฝ่ายพันธกิจสัมพันธ์เพื่อสังคม", role_en="Assistant Dean for Social Engagement",
        dept_th="ภาควิชาบริหารธุรกิจ", dept_en="Department of Business Administration",
        email="jirachai@g.swu.ac.th",
        edu=[
            "บธ.บ. (การจัดการการท่องเที่ยวและโรงแรม) มหาวิทยาลัยศรีนครินทรวิโรฒ",
            "ศศ.ม. (การจัดการการท่องเที่ยวและโรงแรม) มหาวิทยาลัยนเรศวร",
            "ปร.ด. (การจัดการกีฬาและนันทนาการ) มหาวิทยาลัยศรีนครินทรวิโรฒ",
        ],
        expertise_th="การจัดการธุรกิจโรงแรมและรีสอร์ท การบริการอาหารและเครื่องดื่ม การจัดกิจกรรมกีฬาและนันทนาการในธุรกิจที่พักแรม",
        cv=CV_BASE + "tourism_hotel/06-CV-dr_Jirachai_%20Muenlit.pdf",
        source="https://bas2.swu.ac.th/program/tourismandhotel/teacher/jirachai",
    ),
    dict(
        slug="rasita-sangboonnak", group="dept_head",
        name_th="ดร.รสิตา สังข์บุญนาค", name_en="Dr. Rasita Sangboonnak",
        role_th="หัวหน้าภาควิชาบัญชีและการเงิน", role_en="Head, Department of Accounting and Finance",
        dept_th="ภาควิชาบัญชีและการเงิน", dept_en="Department of Accounting and Finance",
        email="supaporns@g.swu.ac.th",
        edu=[
            "บธ.บ. (การบัญชีต้นทุน) สถาบันเทคโนโลยีราชมงคล วิทยาเขตพาณิชยการพระนคร",
            "บช.ม. จุฬาลงกรณ์มหาวิทยาลัย",
            "ปร.ด. (การบัญชี) มหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี",
        ],
        expertise_th="การบัญชี การบัญชีต้นทุน",
        cv=CV_BASE + "04-CV-rasita_sangboonnak.pdf",
        source="https://bas2.swu.ac.th/program/accountancy/teacher/rasita",
    ),
    dict(
        slug="kangwan-yodwisitsak", group="dept_head",
        name_th="ผู้ช่วยศาสตราจารย์ ดร.กังวาน ยอดวิศิษฎ์ศักดิ์", name_en="Asst. Prof. Dr. Kangwan Yodwisitsak",
        role_th="หัวหน้าภาควิชาการตลาดและการจัดการ", role_en="Head, Department of Marketing and Management",
        dept_th="ภาควิชาการตลาดและการจัดการ", dept_en="Department of Marketing and Management",
        email="kangwan@g.swu.ac.th",
        cert_th="ได้รับการรับรองคุณภาพการจัดการเรียนการสอนตามกรอบมาตรฐานวิชาชีพของสหราชอาณาจักร UKPSF ในระดับ Fellow (FHEA)",
        edu=[
            "บธ.บ. (การตลาด) มหาวิทยาลัยอัสสัมชัญ",
            "บธ.ม. (การเงินและการตลาด) สถาบันบัณฑิตบริหารธุรกิจศศินทร์แห่งจุฬาลงกรณ์มหาวิทยาลัย",
            "D.B.A. (Business Administration) The University of South Australia, Australia",
        ],
        expertise_th="บริหารธุรกิจ การตลาด การเงินและการตลาด",
        cv=CV_BASE + "06-CV-asst_prof_kangwan_yodwisitsak.pdf",
        source="https://bas2.swu.ac.th/teacher/mba/kangwan",
    ),
    dict(
        slug="wasan-sakulkijkarn", group="dept_head",
        name_th="รองศาสตราจารย์ ดร.วสันต์ สกุลกิจกาญจน์", name_en="Assoc. Prof. Dr. Wasan Sakulkijkarn",
        role_th="หัวหน้าภาควิชาบริหารธุรกิจ", role_en="Head, Department of Business Administration",
        dept_th="ภาควิชาบริหารธุรกิจ", dept_en="Department of Business Administration",
        email="wasan@g.swu.ac.th",
        edu=[
            "ศศ.บ. (ภาษาอังกฤษ) มหาวิทยาลัยรามคำแหง",
            "ร.บ. (การบริหารรัฐกิจ) มหาวิทยาลัยรามคำแหง",
            "บธ.ม. (การจัดการทั่วไป) มหาวิทยาลัยรามคำแหง",
            "รป.ด. (การจัดการภาครัฐและภาคเอกชน) สถาบันบัณฑิตพัฒนบริหารศาสตร์",
        ],
        expertise_th="ธุรกิจเพื่อสังคม การจัดการทรัพยากรมนุษย์ การจัดการกลยุทธ์ การจัดการธุรกิจขนาดกลางและขนาดย่อม",
        cv=CV_BASE + "social_enterprise/03-CV-associate_professor_dr_wasan_sakulkijkarn.pdf",
        source="https://bas2.swu.ac.th/program/social_enterprise/wasan",
    ),
]

# ชื่อที่สะกดผิดในต้นแบบรุ่นก่อน -> ชื่อที่ถูกต้องตามเว็บทางการ
NAME_FIXES = {
    "ผศ.ดร.จาริณี จารุเสน": "ผศ.ดร.จรินทร์ จารุเสน",
    "ผศ.ดร.พุฒิพงศ์ มีถาวรกุล": "ผศ.ดร.ภูธิป มีถาวรกุล",
    "ผศ.ดร.กัญญ์ฐิตา คีรีอังกูร": "ผศ.ดร.กัลยกิตติ์ กีรติอังกูร",
    "ผศ.ดร.เพชรรัตน์ จินตะนุพงศ์": "ผศ.ดร.เพชรรัตน์ จินต์นุพงศ์",
    "ดร.รสิตา แสงบุญนำ": "ดร.รสิตา สังข์บุญนาค",
    "ผศ.ดร.คมกฤช นันทะโรจพงศ์": "ผศ.ดร.คมกริช นันทะโรจพงศ์",
    "ดร.จิรชัย หมื่นลิต": "ดร.จิรชัย หมื่นฤทธิ์",
    "หัวหน้าภาควิชาการบัญชีและการเงิน": "หัวหน้าภาควิชาบัญชีและการเงิน",
}

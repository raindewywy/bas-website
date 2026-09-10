# -*- coding: utf-8 -*-
"""
เติมรูปในช่องที่ยังว่างทั้งหมด

  - การ์ดหลักสูตรในหน้าภาควิชา (9)      -> ไฟล์ในเครื่อง assets/media/program-*.jpg
  - การ์ดข่าวในหน้าข่าว (5) + ข่าวใน (1) -> ไฟล์ในเครื่อง
  - กิจกรรม/ชีวิตแคมปัสในหน้าชีวิตนิสิต (4)
  - รูปบุคคล 44 ช่อง                     -> URL ทางการของคณะจาก bas2.swu.ac.th
    เลือกใช้ URL เพราะชื่อไฟล์บนเว็บมีชื่อบุคคลกำกับ จึงจับคู่ชื่อ-รูปได้ถูกต้อง
    แน่นอน (ไฟล์ในโฟลเดอร์ dean/ ไม่มีชื่อกำกับ จับคู่เองจะเสี่ยงสลับคน)
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL = '<img class="media-img" src="assets/media/%s" alt="%s" loading="lazy" decoding="async">'
REMOTE = ('<img class="media-img" src="%s" alt="%s" loading="lazy" decoding="async" '
          'referrerpolicy="no-referrer">')

BASE = "https://bas2.swu.ac.th/Portals/64/BlockBuilderImages/20456/"
PEOPLE = {  # นามสกุล -> (ไฟล์รูปทางการ, ชื่อเต็มสำหรับ alt)
    "ฐานะจาโร": ("dr_natinee_thanajaro1.png", "ดร.ณัฐินี ฐานะจาโร"),
    "จารุเสน": ("021-jarin-sm.jpg", "ผู้ช่วยศาสตราจารย์ ดร.จรินทร์ จารุเสน"),
    "มีถาวรกุล": ("assistant_professor_dr_phutip_meethavornkul.png", "ผู้ช่วยศาสตราจารย์ ดร.ภูธิป มีถาวรกุล"),
    "กีรติอังกูร": ("assistant_professor_dr_kanyakit_keeratiangkoon.png", "ผู้ช่วยศาสตราจารย์ ดร.กัลยกิตติ์ กีรติอังกูร"),
    "จินต์นุพงศ์": ("051-phetcharat-sm.jpg", "ผู้ช่วยศาสตราจารย์ ดร.เพชรรัตน์ จินต์นุพงศ์"),
    "สังข์บุญนาค": ("dr_rasita_sangboonnak.png", "ดร.รสิตา สังข์บุญนาค"),
    "ยอดวิศิษฎ์ศักดิ์": ("assistant_professor_dr_kangwan_yodwisitsak.png", "ผู้ช่วยศาสตราจารย์ ดร.กังวาน ยอดวิศิษฎ์ศักดิ์"),
    "สกุลกิจกาญจน์": ("associate_professor_dr_wasan_sakulkijkarn.png", "รองศาสตราจารย์ ดร.วสันต์ สกุลกิจกาญจน์"),
    "นันทะโรจพงศ์": ("assistant_professor_dr_khomkrit_nantharojphong.png", "ผู้ช่วยศาสตราจารย์ ดร.คมกริช นันทะโรจพงศ์"),
    "ประเสริฐกุล": ("dr_siam_prasertkul.png", "ดร.สยาม ประเสริฐกุล"),
    "หมื่นฤทธิ์": ("dr_jirachai_muenlit.png", "ดร.จิรชัย หมื่นฤทธิ์"),
}

PROGRAM_ALT = {
    "accountancy": "หลักสูตรบัญชีบัณฑิต",
    "bba-marketing": "หลักสูตรบริหารธุรกิจบัณฑิต วิชาเอกการตลาด",
    "bba-finance": "หลักสูตรบริหารธุรกิจบัณฑิต วิชาเอกการเงิน",
    "bba-tourism-hotel": "หลักสูตรบริหารธุรกิจบัณฑิต สาขาวิชาการท่องเที่ยวและการโรงแรม",
    "bba-international-business": "หลักสูตรบริหารธุรกิจบัณฑิต วิชาเอกธุรกิจระหว่างประเทศ",
    "bba-social-enterprise": "หลักสูตรบริหารธุรกิจบัณฑิต สาขาวิชาธุรกิจเพื่อสังคม",
    "global-business-management": "หลักสูตรการจัดการธุรกิจโลก (นานาชาติ)",
    "mba": "หลักสูตรบริหารธุรกิจมหาบัณฑิต",
    "phd": "หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาบริหารธุรกิจเพื่อสังคม",
}
NEWS = {
    "mou-brokenshire-college": ("banner-mou.jpg", "พิธีลงนาม MOU"),
    "germany-exchange-opportunity": ("banner-exchange.jpg", "โอกาสแลกเปลี่ยนที่ประเทศเยอรมนี"),
    "frankfurt-school-exchange": ("banner-exchange.jpg", "โครงการแลกเปลี่ยน Frankfurt School"),
    "york-university-visit": ("banner-news.jpg", "ข่าวความร่วมมือทางวิชาการ"),
    "cross-cultural-branding-lecture": ("academic-research.jpg", "บรรยายพิเศษทางวิชาการ"),
}
ACTIVITY_BY_TEXT = [
    ("ปฐมนิเทศ", "banner-student-support.jpg", "ปฐมนิเทศนิสิตใหม่"),
    ("แข่งขัน", "activity-workshop.jpg", "การแข่งขันเคสธุรกิจ"),
    ("ชมรม", "activity-community.jpg", "งานชมรมและกิจกรรมนิสิต"),
]


def fill_program_cards(s):
    """<a ... href="program-detail.html?p=SLUG"> ... <span class="ph-label">ภาพประกอบหลักสูตร</span>"""
    def repl(m):
        blk, slug = m.group(0), m.group(1)
        if slug not in PROGRAM_ALT:
            return blk
        return blk.replace('<span class="ph-label">ภาพประกอบหลักสูตร</span>',
                           LOCAL % ("program-%s.jpg" % slug, PROGRAM_ALT[slug]), 1)
    return re.subn(r'<a class="card program-card[^"]*"[^>]*href="program-detail\.html\?p=([a-z0-9-]+)"[^>]*>.*?</a>',
                   repl, s, flags=re.S)


def fill_news_cards(s):
    def repl(m):
        blk, slug = m.group(0), m.group(1)
        f, alt = NEWS.get(slug, ("banner-news.jpg", "ภาพข่าว"))
        return blk.replace('<span class="ph-label">ภาพข่าว</span>', LOCAL % (f, alt), 1)
    return re.subn(r'<a class="card reveal"[^>]*href="news-detail\.html\?n=([a-z0-9-]+)"[^>]*>.*?</a>',
                   repl, s, flags=re.S)


def fill_staff_photos(s):
    """staff-card ที่มี ph-label 'ภาพถ่าย' -> ใส่รูปตามนามสกุลที่ปรากฏในการ์ดนั้น"""
    n = [0]

    def repl(m):
        blk = m.group(0)
        if '<span class="ph-label">ภาพถ่าย</span>' not in blk:
            return blk
        for surname, (fname, full) in PEOPLE.items():
            if surname in blk:
                n[0] += 1
                return blk.replace('<span class="ph-label">ภาพถ่าย</span>',
                                   REMOTE % (BASE + fname, full), 1)
        return blk

    s = re.sub(r'<div class="staff-card[^"]*">.*?</div></div>', repl, s, flags=re.S)
    return s, n[0]


def fill_leader_page(s, name):
    """หน้าประวัติรายบุคคล — ใช้ชื่อไฟล์บอกว่าเป็นใคร"""
    if '<span class="ph-label">ภาพถ่าย</span>' not in s:
        return s, 0
    for surname, (fname, full) in PEOPLE.items():
        if surname in s:
            return s.replace('<span class="ph-label">ภาพถ่าย</span>',
                             REMOTE % (BASE + fname, full), 1), 1
    return s, 0


def fill_misc(s, page):
    n = 0
    if page == "student-life.html":
        s, k = re.subn(r'(<span class="story-theme">สัมผัสประสบการณ์</span>)<span class="ph-label">[^<]*</span>',
                       r'\1' + LOCAL % ("campus-life.jpg", "บรรยากาศชีวิตในแคมปัส"), s); n += k
        for key, f, alt in ACTIVITY_BY_TEXT:
            m = re.search(r'<div class="card reveal"><div class="card-media"><span class="ph-label">ภาพกิจกรรม</span>'
                          r'</div><div class="card-body">.*?</div></div>', s, re.S)
            # แทนทีละใบตามลำดับ โดยดูคำสำคัญในเนื้อการ์ด
            for mm in re.finditer(r'<div class="card reveal"><div class="card-media">'
                                  r'<span class="ph-label">ภาพกิจกรรม</span></div>.*?</div></div>', s, re.S):
                if key in mm.group(0):
                    s = s.replace(mm.group(0),
                                  mm.group(0).replace('<span class="ph-label">ภาพกิจกรรม</span>',
                                                      LOCAL % (f, alt), 1), 1)
                    n += 1
                    break
    if page == "news-detail.html":
        s, k = re.subn(r'<span class="ph-label">ภาพประกอบข่าว</span>',
                       LOCAL % ("banner-news.jpg", "ภาพประกอบข่าว"), s); n += k
    s, k = re.subn(r'<span class="ph-label">ภาพข่าวเด่น</span>',
                   LOCAL % ("bas-news.jpg", "ข่าวเด่นของคณะ"), s); n += k
    return s, n


def main():
    tot = {"program": 0, "news": 0, "staff": 0, "misc": 0}
    for path in sorted(glob.glob(str(ROOT / "*.html"))):
        p = Path(path)
        s = orig = p.read_text(encoding="utf-8")
        s, a = fill_program_cards(s)
        s, b = fill_news_cards(s)
        if p.name.startswith("leader-"):
            s, c = fill_leader_page(s, p.name)
        else:
            s, c = fill_staff_photos(s)
        s, d = fill_misc(s, p.name)
        tot["staff"] += c; tot["misc"] += d
        if s != orig:
            p.write_text(s, encoding="utf-8")
    # นับจริงจากผลลัพธ์
    print(tot)


if __name__ == "__main__":
    main()

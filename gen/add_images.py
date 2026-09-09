# -*- coding: utf-8 -*-
"""
ใส่รูปจริงลงช่อง placeholder โดยอ้างอิงไฟล์จาก bas.swu.ac.th / bas2.swu.ac.th
ที่คณะดาวน์โหลดมาไว้แล้ว (ย่อ/บีบอัดเก็บใน assets/media/)

จับคู่เฉพาะจุดที่ยืนยันได้จากตัวภาพเอง (ภาพหลักสูตรมีชื่อหลักสูตรพิมพ์อยู่บนภาพ,
แบนเนอร์มีชื่อเรื่องกำกับ) ส่วนช่องที่ไม่มีภาพตรงเรื่องใช้ภาพกิจกรรมทั่วไปตามที่ตกลง
ภาพบุคคล (staff-photo) ยังไม่แตะ รอยืนยันการจับคู่ชื่อ-รูป
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

IMG = ('<img class="media-img" src="assets/media/%s" alt="%s" loading="lazy" decoding="async">')

# --------------------------------------------------------------- 1. หลักสูตร
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

CARD_RE = re.compile(r'<a class="card program-card[^"]*"[^>]*href="program-detail\.html\?p=([a-z0-9-]+)"[^>]*>.*?</a>', re.S)
MEDIA_RE = re.compile(r'<div class="card-media"[^>]*>\s*<span class="card-ph" aria-hidden="true"></span>')


def fix_program_cards(s):
    def repl(m):
        block, slug = m.group(0), m.group(1)
        if 'class="media-img"' in block or slug not in PROGRAM_ALT:
            return block
        new_media = ('<div class="card-media">'
                     + IMG % ("program-%s.jpg" % slug, PROGRAM_ALT[slug]))
        return MEDIA_RE.sub(new_media, block, count=1)
    return CARD_RE.subn(repl, s)


# ------------------------------------------------------- 2. story rows (ชีวิตนิสิต)
STORY = {
    "เรียนรู้": ("activity-workshop.jpg", "นิสิตทำงานกลุ่มในกิจกรรมของคณะ"),
    "เชื่อมโยง": ("activity-community.jpg", "นิสิตร่วมกิจกรรมของคณะ"),
    "เติบโต": ("activity-graduation.jpg", "บัณฑิตในพิธีรับปริญญา"),
}
STORY_RE = re.compile(
    r'(<div class="story-media"><span class="story-theme">(เรียนรู้|เชื่อมโยง|เติบโต)</span>)'
    r'<span class="ph-label">[^<]*</span>')


def fix_story(s):
    def repl(m):
        f, alt = STORY[m.group(2)]
        return m.group(1) + IMG % (f, alt)
    return STORY_RE.subn(repl, s)


# ----------------------------------------------------------- 3. การ์ดกิจกรรม (rail)
ACT = {
    "กิจกรรมนิสิต": ("activity-workshop.jpg", "กิจกรรมนิสิต BAS SWU"),
    "สิ่งอำนวยความสะดวก": ("campus-life.jpg", "บรรยากาศในและรอบแคมปัส"),
    "แลกเปลี่ยน &amp; นานาชาติ": ("banner-exchange.jpg", "โครงการแลกเปลี่ยนนานาชาติ"),
    "ความร่วมมือ": ("banner-mou.jpg", "พิธีลงนามความร่วมมือ"),
}
ACT_RE = re.compile(
    r'<span class="act-media" aria-hidden="true"><span class="card-ph"></span>'
    r'<span class="act-badge th-body">([^<]+)</span></span>')


def fix_act(s):
    def repl(m):
        cat = m.group(1)
        f, alt = ACT.get(cat, ("activity-community.jpg", "กิจกรรมของคณะ"))
        return ('<span class="act-media">' + IMG % (f, alt)
                + '<span class="act-badge th-body">%s</span></span>' % cat)
    return ACT_RE.subn(repl, s)


# ----------------------------------------------------------------- 4. ข่าว
NEWS = {
    "mou-brokenshire-college": ("banner-mou.jpg", "พิธีลงนาม MOU"),
    "germany-exchange-opportunity": ("banner-exchange.jpg", "โอกาสแลกเปลี่ยนที่ประเทศเยอรมนี"),
    "frankfurt-school-exchange": ("banner-exchange.jpg", "โครงการแลกเปลี่ยน Frankfurt School"),
    "york-university-visit": ("banner-news.jpg", "ข่าวความร่วมมือทางวิชาการ"),
    "cross-cultural-branding-lecture": ("academic-research.jpg", "บรรยายพิเศษทางวิชาการ"),
}
FEATURE_RE = re.compile(
    r'(<a class="news-feature reveal" href="news-detail\.html\?n=([a-z0-9-]+)">)'
    r'<div class="card-media"[^>]*><span class="card-ph" aria-hidden="true"></span></div>')
THUMB_RE = re.compile(
    r'<article class="news-row reveal"><span class="news-thumb" aria-hidden="true"></span>'
    r'(<div><span class="card-tag cat">[^<]*</span><h3><a href="news-detail\.html\?n=([a-z0-9-]+)")')


def fix_news(s):
    n = 0

    def rf(m):
        f, alt = NEWS.get(m.group(2), ("banner-news.jpg", "ภาพข่าว"))
        return m.group(1) + '<div class="card-media">' + IMG % (f, alt) + '</div>'
    s, k = FEATURE_RE.subn(rf, s); n += k

    def rt(m):
        f, alt = NEWS.get(m.group(2), ("banner-news.jpg", "ภาพข่าว"))
        return ('<article class="news-row reveal"><span class="news-thumb">'
                + IMG % (f, alt) + '</span>' + m.group(1))
    s, k = THUMB_RE.subn(rt, s); n += k
    return s, n


# ------------------------------------------------- 5. split-media (ภาพประกอบกว้าง)
SPLIT = {
    "index.html": ("campus-life.jpg", "บรรยากาศคณะบริหารธุรกิจเพื่อสังคม มศว"),
    "news-detail.html": ("banner-news.jpg", "ภาพประกอบข่าว"),
    "program-detail.html": ("banner-program.jpg", "ภาพประกอบหลักสูตร"),
}
SPLIT_RE = re.compile(r'<div class="split-media reveal"><span class="ph-label">[^<]*</span></div>')


def fix_split(s, name):
    if name not in SPLIT:
        return s, 0
    f, alt = SPLIT[name]
    return SPLIT_RE.subn('<div class="split-media reveal">' + IMG % (f, alt) + '</div>', s)


# ------------------------------------------------------------------- CSS
CSS_MARKER = "/* == v8 real images =="
CSS_BLOCK = """
/* == v8 real images ======================================================
   รูปจริงจาก bas.swu.ac.th / bas2.swu.ac.th แทนกล่อง placeholder
   ====================================================================== */
.media-img{
  position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; display:block; border-radius:inherit;
}
.card-media, .act-media, .story-media, .split-media, .news-thumb{position:relative; overflow:hidden;}
.act-media .act-badge{position:absolute;}
.card:hover .media-img, a:hover .media-img{transform:scale(1.04);}
.media-img{transition:transform 420ms cubic-bezier(.22,.61,.36,1);}
@media (prefers-reduced-motion: reduce){ .media-img{transition:none;} .card:hover .media-img{transform:none;} }
"""


def main():
    totals = {"program": 0, "story": 0, "act": 0, "news": 0, "split": 0}
    for path in sorted(glob.glob(str(ROOT / "*.html"))):
        p = Path(path)
        s = orig = p.read_text(encoding="utf-8")
        s, a = fix_program_cards(s); totals["program"] += a
        s, b = fix_story(s);         totals["story"] += b
        s, c = fix_act(s);           totals["act"] += c
        s, d = fix_news(s);          totals["news"] += d
        s, e = fix_split(s, p.name); totals["split"] += e
        if s != orig:
            p.write_text(s, encoding="utf-8")
    print(totals)

    css_path = ROOT / "assets" / "styles.css"
    css = css_path.read_text(encoding="utf-8")
    if CSS_MARKER not in css:
        css_path.write_text(css + CSS_BLOCK, encoding="utf-8")
        print("styles.css: added image CSS")


if __name__ == "__main__":
    main()

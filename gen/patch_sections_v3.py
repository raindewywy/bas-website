# -*- coding: utf-8 -*-
"""
patch_sections_v3 — นำ 4 ส่วนจากดราฟต์ดีไซน์ BAS มาแทนที่ของเดิมในเว็บชุดนี้

ส่วนที่แทนที่
  1) การ์ดหลักสูตร (index.html + programs.html)
  2) ส่วนข่าวและกิจกรรมบนหน้าแรก  (lead 1 + row 4)
  3) CTA band  (index.html + program-detail.html)  — จัดกึ่งกลางสีแดง → split สีเขียวเข้ม
  4) page-hero ทุกหน้า — พื้นอ่อน → พื้นเขียวเข้มแบรนด์ (แก้ที่ CSS จุดเดียว)

หลักการ: เอา "องค์ประกอบ + ลำดับสายตา + interaction" จากดราฟต์มา แต่ยังคงใช้
design token, ฟอนต์ และแพตเทิร์นสองภาษา (bi-heading) ของเว็บชุดนี้ เพื่อไม่ให้
กลายเป็นชิ้นส่วนแปลกปลอม  ข้อมูลทั้งหมดใช้ของจริงที่มีอยู่ในเว็บ ไม่มีการแต่งเพิ่ม

รันซ้ำได้ (idempotent) — ตรวจ marker ก่อนแก้ทุกครั้ง
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

# ---------------------------------------------------------------------------
# 1. CSS
# ---------------------------------------------------------------------------
CSS_MARKER = "/* == v3 sections =="
CSS_BLOCK = """
/* == v3 sections ========================================================
   page-hero เข้ม · CTA band แบบ split · การ์ดหลักสูตร · แถวข่าวหน้าแรก
   ทุกค่าอ้าง token เดิมของเว็บ ไม่มีสีลอย
   ===================================================================== */
:root{
  --deep-900:#04262C;   /* พื้นเข้มสายเดียวกับ #00B3C9 — ตัวอักษรขาวได้ 15.6:1 */
  --deep-800:#063C45;
  --brand-300:#7FE0EC;  /* eyebrow/ไอคอนบนพื้นเข้ม — 11.4:1 */
}

/* ---- 1. Page hero: พื้นเขียวเข้มแบรนด์ -------------------------------- */
.page-hero{
  background:var(--deep-900);
  border-bottom:0;
  color:#fff;
  position:relative;
  overflow:hidden;
  padding:var(--space-7) 0 var(--space-8);
}
.page-hero::after{
  content:""; position:absolute; right:-6%; top:-42%;
  width:46%; aspect-ratio:1; border-radius:50%; pointer-events:none;
  background:radial-gradient(circle at 34% 34%, rgba(0,179,201,.42), rgba(0,179,201,0) 68%);
}
.page-hero > .wrap, .page-hero > .wrap-narrow{position:relative; z-index:1;}
.page-hero h1{color:#fff; max-width:18ch;}
.page-hero .bi-en{color:rgba(255,255,255,.60);}
.page-hero .eyebrow{color:var(--brand-300);}
.page-hero .eyebrow::before{background:var(--brand-300);}
.page-hero .lede{color:rgba(255,255,255,.82); max-width:56ch;}
/* ทางออกสำหรับหน้าที่อยากได้พื้นอ่อนแบบเดิม: เพิ่มคลาส page-hero--light */
.page-hero--light{background:var(--paper-dim); color:var(--ink); border-bottom:1px solid var(--line);}
.page-hero--light::after{display:none;}
.page-hero--light h1{color:var(--ink);}
.page-hero--light .bi-en, .page-hero--light .lede{color:var(--muted);}
.page-hero--light .eyebrow{color:var(--teal-600);}
.page-hero--light .eyebrow::before{background:var(--teal-600);}
@media (max-width:760px){ .page-hero h1{max-width:none;} }

/* ---- 2. CTA band: split ข้อความซ้าย ปุ่มเรียงขวา ---------------------- */
.cta-band{
  background:var(--deep-900);
  color:#fff;
  border-radius:var(--radius-l);
  text-align:left;
  padding:clamp(2.2rem,3.4vw,3.6rem) clamp(1.5rem,3.4vw,3.6rem);
  position:relative; overflow:hidden;
  display:grid; grid-template-columns:minmax(0,1fr) minmax(220px,300px);
  gap:var(--space-5) var(--space-7); align-items:center;
}
.cta-band::after{
  content:""; position:absolute; left:-10%; bottom:-70%;
  width:44%; aspect-ratio:1; border-radius:50%; pointer-events:none;
  background:radial-gradient(circle at 50% 50%, rgba(0,179,201,.34), rgba(0,179,201,0) 70%);
}
.cta-band > *{position:relative; z-index:1;}
.cta-band .eyebrow{color:var(--brand-300);}
.cta-band .eyebrow::before{background:var(--brand-300);}
.cta-band h2{color:#fff; font-size:var(--step-h2); margin-top:var(--space-2);}
.cta-band p{color:rgba(255,255,255,.82); max-width:50ch; margin:var(--space-3) 0 0;}
.cta-actions{display:grid; gap:.7rem; margin-top:0; justify-content:stretch;}
.cta-actions .btn{width:100%; justify-content:center; text-align:center; gap:.5em; padding-inline:1.1rem;}
.cta-actions .btn svg{width:16px; height:16px; flex:none;}
@media (max-width:900px){
  .cta-band{grid-template-columns:1fr;}
  .cta-actions{margin-top:var(--space-4);}
}

/* ---- 3. การ์ดหลักสูตร ------------------------------------------------- */
.card-ph{
  position:absolute; inset:0; display:block;
  background:linear-gradient(135deg,#00525E 0%,#0098AC 48%,#43C9DA 100%);
  transition:transform 420ms cubic-bezier(.22,.61,.36,1);
}
.card-ph::after{
  content:""; position:absolute; inset:0;
  background-image:repeating-linear-gradient(115deg, rgba(255,255,255,.10) 0 1px, transparent 1px 9px);
}
.card:hover .card-ph, a:hover > .card-media > .card-ph{transform:scale(1.05);}
.program-card .level-badge{background:rgba(255,255,255,.94); color:var(--deep-900);}
.program-card .degree-code{
  font-family:var(--font-body);
  font-size:.78rem; font-weight:700; letter-spacing:.01em;
  color:var(--teal-600);
}
.program-card .career-list{display:flex; flex-wrap:wrap; gap:0 .5rem; margin-top:.15rem;}
.program-card .career-list span{
  background:none; padding:0; border-radius:0;
  font-size:.8rem; color:var(--muted);
}
.program-card .career-list span + span::before{
  content:"·"; margin-right:.5rem; color:var(--line-strong);
}
.card-cue{
  margin-top:auto; padding-top:.95rem;
  display:inline-flex; align-items:center; gap:.45em;
  font-weight:600; font-size:.92rem; color:var(--teal-600);
}
.card-cue svg{width:14px; height:14px; transition:transform var(--dur) cubic-bezier(.16,1,.3,1);}
.card:hover .card-cue svg{transform:translateX(4px);}

/* ---- 4. ข่าวหน้าแรก: เรื่องเด่น 1 + รายการ 4 --------------------------- */
.cat-chip.is-all{background:var(--ink); border-color:var(--ink); color:#fff;}
.cat-chip.is-all:hover{background:var(--deep-900); border-color:var(--deep-900); color:#fff;}
.news-lead{display:grid; grid-template-columns:minmax(0,7fr) minmax(0,5fr); gap:var(--space-6);}
.news-lead .news-feature{display:block; margin-bottom:0;}
.news-lead .news-feature .card-media{aspect-ratio:16/9; min-height:0; height:auto;}
.news-lead .news-feature .card-body{padding:var(--space-4);}
.news-rows{display:flex; flex-direction:column;}
.news-row{
  position:relative; display:grid; grid-template-columns:92px minmax(0,1fr);
  gap:var(--space-3); align-items:start;
  padding:var(--space-3) 0; border-top:1px solid var(--line);
}
.news-row:first-child{border-top:0; padding-top:0;}
.news-row .news-thumb{
  aspect-ratio:1; border-radius:var(--radius-s); overflow:hidden; position:relative;
  background:linear-gradient(135deg,#0B3B43 0%,#0E6D7B 55%,#5CC3D0 100%);
}
.news-row .news-thumb::after{
  content:""; position:absolute; inset:0;
  background-image:repeating-linear-gradient(115deg, rgba(255,255,255,.10) 0 1px, transparent 1px 9px);
}
.news-row h3{
  font-family:'Noto Sans Thai', var(--font-body);
  font-size:1rem; font-weight:600; line-height:1.45; margin-top:.4rem;
  transition:color var(--dur);
}
.news-row .card-meta{display:block; margin-top:.3rem;}
.news-row:hover h3{color:var(--teal-600);}
.news-row a::after{content:""; position:absolute; inset:0;}
@media (max-width:900px){
  .news-lead{grid-template-columns:1fr;}
}
@media (max-width:420px){
  .news-row{grid-template-columns:72px minmax(0,1fr);}
}
"""

# ---------------------------------------------------------------------------
# 2. การ์ดหลักสูตร
# ---------------------------------------------------------------------------
DEGREE_CODE = {
    "accountancy": "บช.บ. (Accountancy)",
    "bba-marketing": "บธ.บ. (การตลาด)",
    "bba-finance": "บธ.บ. (การเงิน)",
    "bba-tourism-hotel": "บธ.บ. (การท่องเที่ยวและการโรงแรม)",
    "bba-international-business": "บธ.บ. (ธุรกิจระหว่างประเทศ)",
    "bba-social-enterprise": "บธ.บ. (ธุรกิจเพื่อสังคม)",
    "global-business-management": "บธ.บ. (การจัดการธุรกิจโลก)",
    "mba": "บธ.ม. (M.B.A.)",
    "phd": "ปร.ด. (Ph.D.)",
}
CARD_CUE = ('<span class="card-cue">ดูรายละเอียดหลักสูตร ' + ARROW + "</span>")


def patch_program_card(card: str) -> str:
    if 'class="card-cue"' in card:
        return card                                    # แพตช์ไปแล้ว

    key = ""
    m = re.search(r'program-detail\.html\?p=([a-z0-9-]+)', card)
    if m:
        key = m.group(1)

    # -- ภาพ: กล่องเส้นประ → พื้นไล่สีแบรนด์ พร้อม aria-label แทนข้อความในภาพ
    card = re.sub(
        r'<div class="card-media">\s*(<span class="level-badge">.*?</span>)?\s*'
        r'<span class="ph-label">.*?</span>\s*</div>',
        lambda mm: (
            '<div class="card-media" role="img" aria-label="ภาพประกอบหลักสูตร (รอไฟล์ภาพจริงจากคณะ)">'
            '<span class="card-ph" aria-hidden="true"></span>'
            + (mm.group(1) or "")
            + "</div>"
        ),
        card,
        count=1,
        flags=re.S,
    )

    # -- ป้ายภาษาหลักสูตร: ย้ายจาก pill ในเนื้อการ์ด ไปต่อท้าย level-badge บนภาพ
    tag = re.search(r'<span class="card-tag">(.*?)</span>', card, re.S)
    if tag:
        curriculum = tag.group(1).strip()
        card = card.replace(tag.group(0),
                            '<span class="degree-code">%s</span>' % (DEGREE_CODE.get(key, curriculum)), 1)
        if curriculum and "level-badge" in card:
            card = re.sub(
                r'(<span class="level-badge">)(.*?)(</span>)',
                lambda mm: mm.group(1) + mm.group(2) + " · " + curriculum + mm.group(3),
                card, count=1, flags=re.S,
            )

    # -- ปุ่มบอกทางท้ายการ์ด
    card = card.replace("</div></a>", CARD_CUE + "</div></a>", 1)
    return card


def patch_program_cards(path: Path) -> int:
    s = path.read_text(encoding="utf-8")
    n = 0
    out, last = [], 0
    for m in re.finditer(r'<a class="card program-card.*?</a>', s, re.S):
        out.append(s[last:m.start()])
        new = patch_program_card(m.group(0))
        n += (new != m.group(0))
        out.append(new)
        last = m.end()
    out.append(s[last:])
    path.write_text("".join(out), encoding="utf-8")
    return n


# ---------------------------------------------------------------------------
# 3. ข่าวหน้าแรก
# ---------------------------------------------------------------------------
NEWS_ROWS = [
    ("cross-cultural-branding-lecture", "วิชาการและวิจัย", "4 กุมภาพันธ์ 2569",
     "บรรยายพิเศษ Cross-Cultural Branding"),
    ("mou-brokenshire-college", "ความร่วมมือและนานาชาติ", "รอยืนยันวันที่",
     "พิธีลงนาม MOU กับ Brokenshire College ประเทศฟิลิปปินส์"),
    ("germany-exchange-opportunity", "ความร่วมมือและนานาชาติ", "รอยืนยันวันที่",
     "โอกาสแลกเปลี่ยนที่ประเทศเยอรมนี"),
    ("frankfurt-school-exchange", "ความร่วมมือและนานาชาติ", "รอยืนยันวันที่",
     "โครงการแลกเปลี่ยน Frankfurt School of Finance &amp; Management"),
]

NEWS_FEATURE = (
    '<a class="news-feature reveal" href="news-detail.html?n=york-university-visit">'
    '<div class="card-media" role="img" aria-label="ภาพข่าวเด่น (รอไฟล์ภาพจริงจากคณะ)">'
    '<span class="card-ph" aria-hidden="true"></span></div>'
    '<div class="card-body">'
    '<span class="card-tag cat">ข่าวเด่น</span>'
    '<h3 class="card-title">ความร่วมมือทางวิชาการและเยี่ยมชมคณะ: ต้อนรับมหาวิทยาลัยยอร์ก</h3>'
    '<p class="card-desc">BAS SWU ต้อนรับคณะผู้แทนจากมหาวิทยาลัยยอร์ก (University of York) '
    'เพื่อหารือความร่วมมือทางวิชาการและเยี่ยมชมคณะ</p>'
    '<span class="card-meta">6 กุมภาพันธ์ 2569</span>'
    "</div></a>"
)


def news_row(slug, cat, date, title):
    return (
        '<article class="news-row reveal">'
        '<span class="news-thumb" aria-hidden="true"></span>'
        "<div>"
        '<span class="card-tag cat">%s</span>'
        '<h3><a href="news-detail.html?n=%s">%s</a></h3>'
        '<span class="card-meta">%s</span>'
        "</div></article>" % (cat, slug, title, date)
    )


NEWS_BLOCK = (
    '<div class="news-lead">'
    + NEWS_FEATURE
    + '<div class="news-rows">'
    + "".join(news_row(*r) for r in NEWS_ROWS)
    + "</div></div>"
)


def patch_home_news(path: Path) -> bool:
    s = path.read_text(encoding="utf-8")
    if 'class="news-lead"' in s:
        return False
    a = s.index('<a class="news-feature reveal"')
    b = s.index("</div>\n  </div>\n</section>", a)
    s = s[:a] + NEWS_BLOCK + "\n  " + s[b + len("</div>\n"):]
    # เพิ่มชิป "ทั้งหมด" หน้าแถบหมวดหมู่ ให้ตรงกับดราฟต์
    if 'cat-chip is-all' not in s:
        s = s.replace(
            '<div class="cat-bar"><a class="cat-chip th-body"',
            '<div class="cat-bar"><a class="cat-chip is-all th-body" href="news.html">ทั้งหมด</a>'
            '<a class="cat-chip th-body"',
            1,
        )
    path.write_text(s, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# 4. CTA band
# ---------------------------------------------------------------------------
def cta(eyebrow, heading, lede, actions):
    btns = "".join(
        '<a class="btn %s" href="%s"%s>%s</a>' % (cls, href, extra, label)
        for cls, href, label, extra in actions
    )
    return (
        '<div class="cta-band reveal">'
        '<div class="cta-copy">'
        '<p class="eyebrow th-body">%s</p>'
        '<h2 class="th-body">%s</h2>'
        '<p class="th-body">%s</p>'
        "</div>"
        '<div class="cta-actions">%s</div>'
        "</div>" % (eyebrow, heading, lede, btns)
    )


GFORM = ("https://docs.google.com/forms/d/e/1FAIpQLSczu8q5LQoaCWA3oLExVLoBTjLdo3XY9BMP3PT9XfZRPRxSug"
         "/viewform")

CTA_HOME = cta(
    "ก้าวต่อไปของคุณ",
    "พร้อมเริ่มต้นที่ BAS SWU แล้วหรือยัง",
    "ดูหลักสูตร เกณฑ์การรับสมัคร และช่องทางติดต่ออาจารย์ที่ปรึกษาของแต่ละหลักสูตรได้ในที่เดียว",
    [
        ("btn-on-deep", "admissions.html", "ขั้นตอนและปฏิทินการรับสมัคร " + ARROW, ""),
        ("btn-ghost-invert", "programs.html#advisors", "ปรึกษาอาจารย์ประจำหลักสูตร", ""),
        ("btn-ghost-invert", "contact.html", "ติดต่อสำนักงานคณะ", ""),
    ],
)

CTA_DETAIL = cta(
    "การรับสมัคร",
    "มีคำถามเกี่ยวกับหลักสูตรนี้?",
    "พูดคุยกับอาจารย์ประจำหลักสูตร หรือดูขั้นตอนการสมัครแบบละเอียดก่อนตัดสินใจ",
    [
        ("btn-on-deep", "admissions.html", "คู่มือการรับสมัคร " + ARROW, ""),
        ("btn-ghost-invert", "programs.html#advisors", "ปรึกษาอาจารย์ประจำหลักสูตร", ""),
        ("btn-ghost-invert", GFORM, "สมัครเรียนออนไลน์",
         ' target="_blank" rel="noopener"'),
    ],
)


def patch_cta(path: Path, new_block: str) -> bool:
    s = path.read_text(encoding="utf-8")
    if 'class="cta-copy"' in s:
        return False
    m = re.search(r'<div class="cta-band reveal">.*?</div>\s*</div>\s*(?=</div>\s*</section>)', s, re.S)
    if not m:
        m = re.search(r'<div class="cta-band reveal">.*?<div class="cta-actions">.*?</div>\s*</div>', s, re.S)
    assert m, "cta-band not found in %s" % path.name
    s = s[: m.start()] + new_block + s[m.end():]
    path.write_text(s, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
def main():
    css = CSS.read_text(encoding="utf-8")
    if CSS_MARKER not in css:
        # ปุ่มขาวบนพื้นเข้ม — เพิ่มเป็นคลาสจริงแทน inline style สีแดงเดิม
        css += (
            "\n.btn-on-deep{background:#fff; color:var(--deep-900); border-color:#fff;}"
            "\n.btn-on-deep:hover{background:#D7F3F7; border-color:#D7F3F7; color:var(--deep-900);}\n"
        )
        css += CSS_BLOCK
        CSS.write_text(css, encoding="utf-8")
        print("styles.css  : เพิ่มบล็อก v3")
    else:
        print("styles.css  : มีบล็อก v3 อยู่แล้ว ข้าม")

    for name in ("index.html", "programs.html"):
        n = patch_program_cards(ROOT / name)
        print("%-12s: การ์ดหลักสูตร %d ใบ" % (name, n))

    print("index.html  : ข่าวหน้าแรก %s" % ("แทนที่แล้ว" if patch_home_news(ROOT / "index.html") else "ข้าม"))
    print("index.html  : CTA band %s" % ("แทนที่แล้ว" if patch_cta(ROOT / "index.html", CTA_HOME) else "ข้าม"))
    print("program-detail.html : CTA band %s"
          % ("แทนที่แล้ว" if patch_cta(ROOT / "program-detail.html", CTA_DETAIL) else "ข้าม"))
    print("page-hero   : เปลี่ยนเป็นพื้นเข้มผ่าน CSS (มีผลทั้ง 14 หน้า)")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
patch_interactive_v4 — เพิ่ม interactive component 3 ตัวบนหน้าแรก
โดยถอดหลักการจาก swu.ac.th (reference เท่านั้น ไม่คัดลอก layout/asset/โค้ด/สี)

  1) Academic tiles   — แทน quick-band เดิม (4 ประตูทางเข้าเชิงวิชาการ)
  2) B · A · S strip  — แถบอัตลักษณ์แบบ tablist กดสลับเนื้อหาได้
  3) Activity rail    — คารูเซลกิจกรรม/ชีวิตนิสิต 7 การ์ด พร้อมลูกศร + dot pagination

สิ่งที่ "ไม่" เอามาจาก มศว:
  - สีแดงแบรนด์ มศว        → ใช้ #00B3C9 + ink ของ BAS แทน
  - เฟรมเวิร์ก LOVES ของ มศว → ใช้ B·A·S ซึ่งเป็นชื่อคณะเองแทน
  - เนื้อหา/ภาพ/มาร์กอัปใด ๆ → เนื้อหาทุกชิ้นดึงจากหน้าที่มีอยู่จริงในเว็บชุดนี้

รันซ้ำได้ (idempotent)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "index.html"
CSS = ROOT / "assets" / "styles.css"
JS = ROOT / "assets" / "script.js"

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

# ===========================================================================
# 1. ACADEMIC TILES  (แทน quick-band)
# ===========================================================================
TILE_ICONS = {
    "admission": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/><path d="M10 12h6M10 16h6"/>',
    "bachelor": '<path d="M12 4l9 4.5-9 4.5-9-4.5z"/><path d="M6.5 11v4.5c0 1.9 2.9 3.2 5.5 3.2s5.5-1.3 5.5-3.2V11"/>',
    "graduate": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H12v16H6.5A2.5 2.5 0 0 0 4 21.5z"/>'
                '<path d="M20 5.5A2.5 2.5 0 0 0 17.5 3H12v16h5.5A2.5 2.5 0 0 1 20 21.5z"/>',
    "inter": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>'
             '<path d="M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18z"/>',
}

TILES = [
    ("admission", "atile--deep", "การรับสมัคร", "Admission",
     "ข้อมูลการสมัครเข้าศึกษา คุณสมบัติ และขั้นตอนการสมัคร", "admissions.html"),
    ("bachelor", "atile--brand", "ปริญญาตรี", "Undergraduate Programme",
     "หลักสูตรระดับปริญญาตรีทั้งภาษาไทยและภาษาอังกฤษ",
     "programs.html?level=undergraduate"),
    ("graduate", "atile--ink", "บัณฑิตศึกษา", "Graduate Programme",
     "หลักสูตรปริญญาโทและปริญญาเอก เพื่อความเชี่ยวชาญเฉพาะทาง",
     "programs.html#graduate-entry"),
    ("inter", "atile--slate", "โอกาสระดับนานาชาติ", "International Opportunities",
     "หลักสูตรนานาชาติ โครงการแลกเปลี่ยน และปริญญาคู่ 3+1",
     "international.html"),
]


def academic_tiles():
    cards = []
    for key, variant, th, en, desc, href in TILES:
        cards.append(
            '<a class="atile %s reveal" href="%s">'
            '<span class="atile-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg></span>'
            '<span class="atile-title th-body">%s</span>'
            '<span class="atile-en">%s</span>'
            '<span class="atile-desc th-body">%s</span>'
            '<span class="atile-go" aria-hidden="true">%s</span>'
            "</a>" % (variant, href, TILE_ICONS[key], th, en, desc, ARROW)
        )
    return (
        '<section class="section academic-section" aria-labelledby="academic-h">\n'
        '  <div class="wrap">\n'
        '    <div class="academic-head reveal">\n'
        '      <h2 id="academic-h" class="academic-title">Academic</h2>\n'
        '      <p class="th-body">ค้นหาเส้นทางการศึกษาที่เหมาะกับคุณ '
        'ที่คณะบริหารธุรกิจเพื่อสังคม มศว</p>\n'
        "    </div>\n"
        '    <div class="atiles">' + "".join(cards) + "</div>\n"
        "  </div>\n"
        "</section>"
    )


# ===========================================================================
# 2. B · A · S IDENTITY STRIP (tablist)
# ===========================================================================
BAS = [
    ("b", "B", "Business", "ธุรกิจที่เข้าใจจริง",
     "องค์ความรู้ด้านบัญชี การเงิน การตลาด การจัดการ และธุรกิจระหว่างประเทศ "
     "ที่สอนผ่านโจทย์จริงของภาคธุรกิจ ไม่ใช่กรณีศึกษาสำเร็จรูป"),
    ("a", "A", "Administration", "บริหารอย่างมืออาชีพ",
     "ทักษะการตัดสินใจ การวางแผน และการนำองค์กร ที่นิสิตได้ฝึกจริงผ่านโครงงาน "
     "การแข่งขันเคส และการฝึกงานกับองค์กรพันธมิตร"),
    ("s", "S", "Society", "เพื่อสังคมที่ดีกว่า",
     "คำว่า “เพื่อสังคม” อยู่ในชื่อคณะ ไม่ใช่กิจกรรมเสริม — ทุกหลักสูตรวัดความสำเร็จ "
     "ทั้งผลประกอบการและผลกระทบที่เกิดกับผู้คนและชุมชน"),
]


def identity_strip():
    tabs, panels = [], []
    for i, (key, letter, en, th, body) in enumerate(BAS):
        first = i == 0
        tabs.append(
            '<button class="id-card" role="tab" id="idtab-%s" aria-controls="idpanel-%s" '
            'aria-selected="%s" tabindex="%s">'
            '<span class="id-letter" aria-hidden="true">%s</span>'
            '<span class="id-text"><span class="id-en">%s</span>'
            '<span class="id-th th-body">%s</span></span>'
            "</button>" % (key, key, "true" if first else "false",
                           "0" if first else "-1", letter, en, th)
        )
        panels.append(
            '<div class="id-panel" role="tabpanel" id="idpanel-%s" aria-labelledby="idtab-%s"%s>'
            '<p class="th-body">%s</p></div>' % (key, key, "" if first else " hidden", body)
        )
    return (
        '<section class="section-tight identity-section" aria-labelledby="identity-h">\n'
        '  <div class="wrap">\n'
        '    <div class="section-head reveal"><div>\n'
        '      <p class="eyebrow">อัตลักษณ์คณะ</p>\n'
        '      <h2 id="identity-h" class="bi-heading"><span class="bi-th th-body">B · A · S</span>'
        '<span class="bi-en">Business Administration for Society</span></h2>\n'
        "    </div></div>\n"
        '    <div class="id-strip reveal" data-identity>\n'
        '      <div class="id-tabs" role="tablist" aria-label="อัตลักษณ์ B A S">'
        + "".join(tabs) + "</div>\n"
        '      <div class="id-panels">' + "".join(panels) + "</div>\n"
        "    </div>\n"
        '    <p class="caption-note th-body">ถ้อยคำอธิบายอัตลักษณ์เป็นข้อเสนอ '
        "รอยืนยันจากคณะก่อนเผยแพร่จริง</p>\n"
        "  </div>\n"
        "</section>"
    )


# ===========================================================================
# 3. ACTIVITY RAIL (carousel)
# ===========================================================================
ACTIVITIES = [
    ("กิจกรรมนิสิต", "การแข่งขันเคสและโปรเจกต์ประยุกต์",
     "นิสิตจากทั้งสามภาควิชานำทฤษฎีไปใช้กับโจทย์ธุรกิจจริง การแข่งขันแผนธุรกิจ และแล็บประจำภาควิชา",
     "student-life.html#activities"),
    ("กิจกรรมนิสิต", "ชมรมและสโมสรนิสิต",
     "องค์กรที่บริหารโดยนิสิตเปิดพื้นที่ให้ทุกคนได้เป็นผู้นำ — ตั้งแต่การจัดงานอีเวนต์ไปจนถึงการเป็นพี่เลี้ยงรุ่นน้อง",
     "student-life.html#activities"),
    ("กิจกรรมนิสิต", "ปฐมนิเทศและสัปดาห์ต้อนรับ",
     "ปฐมนิเทศนิสิตใหม่ ครอบคลุมทุกภาควิชา ก่อนเปิดภาคการศึกษาต้น",
     "student-life.html#activities"),
    ("สิ่งอำนวยความสะดวก", "ชีวิตในและรอบแคมปัส",
     "จากพื้นที่ทำงานร่วมกันในอาคารนวัตกรรม ไปจนถึงย่านสุขุมวิทโดยรอบ ชีวิตแคมปัสขยายไกลกว่าประตูห้องเรียน",
     "student-life.html#facilities"),
    ("แลกเปลี่ยน &amp; นานาชาติ", "โอกาสแลกเปลี่ยนที่ประเทศเยอรมนี",
     "พันธมิตรแลกเปลี่ยนที่สนับสนุนการศึกษาหนึ่งภาคการศึกษาในประเทศเยอรมนี",
     "student-life.html#exchange"),
    ("แลกเปลี่ยน &amp; นานาชาติ", "Frankfurt School of Finance &amp; Management",
     "โครงการแลกเปลี่ยนเฉพาะกับ Frankfurt School of Finance &amp; Management ประเทศเยอรมนี",
     "student-life.html#exchange"),
    ("ความร่วมมือ", "Brokenshire College ประเทศฟิลิปปินส์",
     "บันทึกข้อตกลงความร่วมมือระหว่าง มศว และ Brokenshire College สนับสนุนความร่วมมือและการแลกเปลี่ยน",
     "student-life.html#exchange"),
]

CIRCLE_ARROW = ('<span class="circle-arrow" aria-hidden="true">'
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
                'stroke-linecap="round" stroke-linejoin="round">'
                '<path d="M5 12h13M12 6l6 6-6 6"/></svg></span>')

RAIL_BTN = ('<button class="rail-btn rail-%s" type="button" data-rail-%s aria-label="%s">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M%s"/></svg></button>')


def activity_rail():
    items = []
    for i, (cat, title, desc, href) in enumerate(ACTIVITIES):
        items.append(
            '<article class="rail-item act-card">'
            '<span class="act-media" aria-hidden="true">'
            '<span class="card-ph"></span>'
            '<span class="act-badge th-body">%s</span></span>'
            '<div class="act-body">'
            '<h3 class="act-title th-body"><a href="%s">%s</a></h3>'
            '<p class="act-desc th-body">%s</p>'
            '<span class="act-more th-body">อ่านเพิ่มเติม %s</span>'
            "</div></article>" % (cat, href, title, desc, CIRCLE_ARROW)
        )
    dots = "".join(
        '<button class="rail-dot" type="button" data-rail-dot="%d" '
        'aria-label="ไปยังชุดที่ %d"%s></button>' % (i, i + 1, ' aria-current="true"' if i == 0 else "")
        for i in range(len(ACTIVITIES))
    )
    return (
        '<section class="section rail-section" aria-labelledby="rail-h">\n'
        '  <div class="wrap">\n'
        '    <div class="section-head reveal"><div>\n'
        '      <p class="eyebrow">กิจกรรม</p>\n'
        '      <h2 id="rail-h" class="bi-heading"><span class="bi-th th-body">กิจกรรมและชีวิตนิสิต</span>'
        '<span class="bi-en">Activities &amp; Student Life</span></h2>\n'
        "    </div>\n"
        '    <a class="link-arrow" href="student-life.html">ดูทั้งหมด %s</a>\n'
        "    </div>\n"
        '    <div class="rail reveal" data-rail role="group" aria-roledescription="คารูเซล" '
        'aria-label="กิจกรรมและชีวิตนิสิต">\n'
        '      %s\n'
        '      <div class="rail-viewport" data-rail-viewport tabindex="0" role="region" '
        'aria-label="รายการกิจกรรม เลื่อนด้วยปุ่มลูกศรซ้ายขวา">\n'
        '        <div class="rail-track">%s</div>\n'
        "      </div>\n"
        '      %s\n'
        "    </div>\n"
        '    <div class="rail-dots" role="group" aria-label="เลือกชุดรายการ">%s</div>\n'
        '    <p class="sr-only" aria-live="polite" data-rail-status></p>\n'
        "  </div>\n"
        "</section>"
        % (ARROW,
           RAIL_BTN % ("prev", "prev", "เลื่อนไปรายการก่อนหน้า", "15 6l-6 6 6 6"),
           "".join(items),
           RAIL_BTN % ("next", "next", "เลื่อนไปรายการถัดไป", "9 6l6 6-6 6"),
           dots)
    )


# ===========================================================================
# CSS
# ===========================================================================
CSS_MARKER = "/* == v4 interactive =="
CSS_BLOCK = """
/* == v4 interactive ======================================================
   Academic tiles · B·A·S strip · Activity rail
   ถอดหลักการจาก swu.ac.th แต่ใช้ token/สี/เนื้อหาของ BAS ทั้งหมด
   ====================================================================== */

.caption-note{margin-top:var(--space-3); font-size:var(--step-caption); color:var(--muted);}
.sr-only{position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden;
  clip:rect(0 0 0 0); white-space:nowrap; border:0;}

/* ---- 1. Academic tiles ------------------------------------------------ */
.academic-head{text-align:center; max-width:60ch; margin:0 auto var(--space-6);}
.academic-title{
  font-size:var(--step-h2); display:inline-block; position:relative; padding-bottom:.3em;
}
.academic-title::after{
  content:""; position:absolute; left:50%; bottom:0; transform:translateX(-50%);
  width:2.4em; height:3px; background:var(--teal-400); border-radius:2px;
}
.academic-head p{margin-top:var(--space-3); color:var(--muted);}

.atiles{display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:var(--space-4);}
.atile{
  position:relative; display:flex; flex-direction:column; align-items:center; text-align:center;
  gap:.55rem; padding:var(--space-6) var(--space-4) var(--space-5);
  border-radius:var(--radius-l); color:#fff; overflow:hidden; min-height:300px;
  transition:transform var(--dur), box-shadow var(--dur);
}
.atile::after{
  content:""; position:absolute; inset:0; background:rgba(255,255,255,0);
  transition:background var(--dur); pointer-events:none;
}
.atile:hover{transform:translateY(-4px); box-shadow:var(--shadow-m);}
.atile:hover::after{background:rgba(255,255,255,.07);}
.atile--deep{background:var(--teal-700);}
.atile--brand{background:var(--teal-400); color:#04262C;}   /* ตัวอักษรเข้มบนสีแบรนด์ = 6.3:1 */
.atile--ink{background:var(--ink);}
.atile--slate{background:#4C5A60;}
.atile-ico{
  width:74px; height:74px; border-radius:50%; display:grid; place-items:center;
  background:rgba(255,255,255,.16); margin-bottom:.4rem; flex:none;
  transition:transform var(--dur), background var(--dur);
}
.atile--brand .atile-ico{background:rgba(4,38,44,.14);}
.atile:hover .atile-ico{transform:scale(1.06); background:rgba(255,255,255,.26);}
.atile--brand:hover .atile-ico{background:rgba(4,38,44,.2);}
.atile-ico svg{width:32px; height:32px;}
.atile-title{font-family:var(--font-display); font-size:1.22rem; font-weight:600; line-height:1.3;}
.atile-en{font-size:.8rem; font-weight:600; opacity:.82;}
.atile-desc{font-size:.86rem; opacity:.88; max-width:24ch; margin:.15rem 0 var(--space-4);}
.atile-go{
  margin-top:auto; width:42px; height:42px; flex:none; box-sizing:border-box;
  border-radius:50%; border:1.5px solid currentColor;
  display:grid; place-items:center;
  transition:transform var(--dur);
}
.atile-go svg{width:17px; height:17px;}
.atile:hover .atile-go{transform:translateX(4px);}
@media (max-width:1024px){ .atiles{grid-template-columns:repeat(2,minmax(0,1fr));} }
@media (max-width:560px){
  .atiles{grid-template-columns:1fr;}
  .atile{min-height:0; padding:var(--space-5) var(--space-4);}
}

/* ---- 2. B · A · S strip ----------------------------------------------- */
.identity-section{background:linear-gradient(180deg,var(--paper) 0%,var(--paper-dim) 100%);}
.id-tabs{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:var(--space-3);}
.id-card{
  display:flex; align-items:center; gap:var(--space-3); text-align:left;
  padding:var(--space-4); background:var(--surface);
  border:1.5px solid var(--line); border-radius:var(--radius-l);
  transition:border-color var(--dur), box-shadow var(--dur), transform var(--dur);
  min-height:96px;
}
.id-card:hover{border-color:var(--teal-600); transform:translateY(-2px);}
.id-card[aria-selected="true"]{border-color:var(--teal-600); box-shadow:0 0 0 3px rgba(0,118,133,.18);}
.id-letter{
  width:62px; height:62px; flex:none; border-radius:50%;
  background:var(--teal-400); color:#04262C;
  display:grid; place-items:center;
  font-family:var(--font-display); font-size:1.9rem; font-weight:700; line-height:1;
  transition:background var(--dur), color var(--dur);
}
.id-card[aria-selected="true"] .id-letter{background:var(--teal-700); color:#fff;}
.id-text{display:flex; flex-direction:column; gap:.15rem; min-width:0;}
.id-en{font-family:var(--font-display); font-weight:600; font-size:1.05rem; color:var(--ink);}
.id-th{font-size:.88rem; color:var(--muted);}
.id-panels{margin-top:var(--space-4);}
.id-panel{
  background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--teal-400);
  border-radius:0 var(--radius-m) var(--radius-m) 0; padding:var(--space-4) var(--space-5);
  max-width:78ch; animation:idFade var(--dur) ease-out;
}
.id-panel[hidden]{display:none;}
@keyframes idFade{from{opacity:0; transform:translateY(4px);} to{opacity:1; transform:none;}}
@media (max-width:760px){
  .id-tabs{grid-template-columns:1fr;}
  .id-card{min-height:0;}
  .id-letter{width:52px; height:52px; font-size:1.55rem;}
}

/* ---- 3. Activity rail (carousel) -------------------------------------- */
.rail{position:relative;}
.rail-viewport{
  overflow-x:auto; overflow-y:hidden; scroll-snap-type:x mandatory;
  scroll-behavior:smooth; -webkit-overflow-scrolling:touch;
  scrollbar-width:none; padding:4px 4px var(--space-2);
}
.rail-viewport::-webkit-scrollbar{display:none;}
.rail-track{display:flex; align-items:stretch; gap:var(--space-4); width:max-content;}
.rail-item{flex:0 0 clamp(260px, 24vw, 330px); scroll-snap-align:start;}
.rail-btn{
  position:absolute; top:38%; z-index:3; width:46px; height:46px; border-radius:50%;
  background:var(--surface); border:1px solid #7E868A; color:var(--ink);
  display:grid; place-items:center; box-shadow:var(--shadow-m);
  transition:background var(--dur), color var(--dur), border-color var(--dur), opacity var(--dur);
}
.rail-btn svg{width:20px; height:20px;}
.rail-btn:hover{background:var(--teal-400); border-color:var(--teal-400); color:#04262C;}
.rail-btn[disabled]{opacity:.32; pointer-events:none;}
.rail-prev{left:-22px;}
.rail-next{right:-22px;}
@media (max-width:1340px){ .rail-prev{left:4px;} .rail-next{right:4px;} }

.rail-dots{display:flex; justify-content:center; gap:.5rem; margin-top:var(--space-4);}
.rail-dot{
  width:12px; height:12px; border-radius:99px; padding:0;
  background:transparent; border:2px solid #7E868A;
  transition:background var(--dur), border-color var(--dur), width var(--dur);
}
.rail-dot:hover{border-color:var(--teal-600); background:var(--teal-400);}
.rail-dot[aria-current="true"]{background:var(--teal-600); border-color:var(--teal-600); width:32px;}

.act-card{
  display:flex; flex-direction:column; position:relative;
  background:var(--surface); border:1px solid var(--line); border-radius:var(--radius-m);
  overflow:hidden; transition:box-shadow var(--dur), transform var(--dur), border-color var(--dur);
}
.act-card:hover{box-shadow:var(--shadow-m); transform:translateY(-3px); border-color:var(--line-strong);}
.act-card:focus-within{border-color:var(--teal-400); box-shadow:0 0 0 3px rgba(0,179,201,.18);}
.act-media{position:relative; display:block; aspect-ratio:16/10; overflow:hidden;}
.act-badge{
  position:absolute; top:.65rem; right:.65rem; z-index:2;
  background:var(--teal-700); color:#fff; font-size:.72rem; font-weight:700;
  padding:.35em .85em; border-radius:99px; letter-spacing:.01em;
}
.act-body{display:flex; flex-direction:column; gap:.5rem; padding:var(--space-4); flex:1;}
.act-title{font-family:var(--font-display); font-size:1.08rem; font-weight:600; line-height:1.35;}
.act-title a{text-decoration:none;}
.act-title a::after{content:""; position:absolute; inset:0;}
.act-card:hover .act-title{color:var(--teal-600);}
.act-desc{font-size:.88rem; color:var(--muted); flex:1;}
.act-more{
  margin-top:auto; padding-top:.6rem; display:flex; align-items:center; justify-content:space-between;
  gap:var(--space-3); font-weight:600; font-size:.9rem; color:var(--teal-600);
}
.circle-arrow{
  width:34px; height:34px; border-radius:50%; flex:none;
  background:var(--teal-400); color:#04262C; display:grid; place-items:center;
  transition:transform var(--dur), background var(--dur);
}
.circle-arrow svg{width:16px; height:16px;}
.act-card:hover .circle-arrow{transform:translateX(3px); background:var(--teal-600); color:#fff;}

@media (prefers-reduced-motion: reduce){
  .rail-viewport{scroll-behavior:auto;}
  .atile:hover, .act-card:hover, .id-card:hover{transform:none;}
  .atile:hover .atile-ico, .act-card:hover .circle-arrow, .atile:hover .atile-go{transform:none;}
}
"""

# ===========================================================================
# JS
# ===========================================================================
JS_MARKER = "/* == v4 interactive =="
JS_BLOCK = r"""

/* == v4 interactive ======================================================
   Activity rail (carousel) + B·A·S tablist
   progressive enhancement: ถ้า JS ไม่ทำงาน rail ยังเลื่อนด้วยนิ้ว/เทรกแพดได้
   และ panel แรกของ B·A·S ยังแสดงอยู่
   ====================================================================== */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Activity rail ------------------------------------------- */
  document.querySelectorAll('[data-rail]').forEach(function (rail) {
    var vp = rail.querySelector('[data-rail-viewport]');
    var prev = rail.querySelector('[data-rail-prev]');
    var next = rail.querySelector('[data-rail-next]');
    var wrap = rail.parentElement;
    var dots = Array.prototype.slice.call(wrap.querySelectorAll('[data-rail-dot]'));
    var status = wrap.querySelector('[data-rail-status]');
    var items = Array.prototype.slice.call(rail.querySelectorAll('.rail-item'));
    if (!vp || !items.length) return;

    function step() {
      var r = items[0].getBoundingClientRect();
      var gap = parseFloat(getComputedStyle(vp.firstElementChild).columnGap || 16);
      return r.width + gap;
    }
    function perPage() {
      return Math.max(1, Math.round(vp.clientWidth / step()));
    }
    function pageCount() {
      return Math.max(1, Math.ceil(items.length / perPage()));
    }
    function currentPage() {
      return Math.round(vp.scrollLeft / (step() * perPage()));
    }
    function go(page) {
      var max = vp.scrollWidth - vp.clientWidth;
      var target = Math.min(page * step() * perPage(), max);
      vp.scrollTo({ left: target, behavior: reduce ? 'auto' : 'smooth' });
    }

    function sync() {
      var max = vp.scrollWidth - vp.clientWidth - 8;
      if (prev) prev.disabled = vp.scrollLeft <= 8;
      if (next) next.disabled = vp.scrollLeft >= max;
      var pc = pageCount();
      var cur = vp.scrollLeft >= max ? pc - 1 : Math.min(currentPage(), pc - 1);
      dots.forEach(function (d, i) {
        d.hidden = i >= pc;
        if (i < pc) d.setAttribute('aria-current', i === cur ? 'true' : 'false');
      });
      if (status) status.textContent = 'ชุดที่ ' + (cur + 1) + ' จาก ' + pc;
    }

    if (prev) prev.addEventListener('click', function () { go(Math.max(0, currentPage() - 1)); });
    if (next) next.addEventListener('click', function () { go(Math.min(pageCount() - 1, currentPage() + 1)); });
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });

    vp.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(Math.min(pageCount() - 1, currentPage() + 1)); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(Math.max(0, currentPage() - 1)); }
      if (e.key === 'Home') { e.preventDefault(); go(0); }
      if (e.key === 'End') { e.preventDefault(); go(pageCount() - 1); }
    });

    var t;
    vp.addEventListener('scroll', function () {
      clearTimeout(t);
      t = setTimeout(sync, 90);
    }, { passive: true });
    window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(sync, 150); });
    sync();
  });

  /* ---------- B · A · S tablist --------------------------------------- */
  document.querySelectorAll('[data-identity]').forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
      tab.focus();
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(tab); });
      tab.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === 'Home') n = tabs[0];
        if (e.key === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n); }
      });
    });
  });
})();
"""


# ===========================================================================
def main():
    css = CSS.read_text(encoding="utf-8")
    if CSS_MARKER not in css:
        CSS.write_text(css + CSS_BLOCK, encoding="utf-8")
        print("styles.css : เพิ่มบล็อก v4")
    else:
        print("styles.css : มีบล็อก v4 แล้ว ข้าม")

    js = JS.read_text(encoding="utf-8")
    if JS_MARKER not in js:
        JS.write_text(js + JS_BLOCK, encoding="utf-8")
        print("script.js  : เพิ่มบล็อก v4")
    else:
        print("script.js  : มีบล็อก v4 แล้ว ข้าม")

    s = IDX.read_text(encoding="utf-8")

    # 1) Academic tiles แทน quick-band
    if 'class="atiles"' not in s:
        a = s.index('<section class="quick-band">')
        b = s.index("</section>", a) + len("</section>")
        s = s[:a] + academic_tiles() + s[b:]
        print("index.html : quick-band → Academic tiles")
    else:
        print("index.html : Academic tiles มีแล้ว ข้าม")

    # 2) B·A·S strip ก่อนหัวข้อ "ทำไมต้อง BAS SWU"
    if "data-identity" not in s:
        i = s.index('<p class="eyebrow">จุดเด่น</p>')
        a = s.rindex("<section", 0, i)
        s = s[:a] + identity_strip() + "\n\n" + s[a:]
        print("index.html : เพิ่มแถบ B · A · S")
    else:
        print("index.html : แถบ B · A · S มีแล้ว ข้าม")

    # 3) Activity rail ต่อท้ายส่วนชีวิตนิสิต
    if "data-rail" not in s:
        i = s.index('<p class="eyebrow">ชีวิตนิสิต</p>')
        b = s.index("</section>", i) + len("</section>")
        s = s[:b] + "\n\n" + activity_rail() + s[b:]
        print("index.html : เพิ่มคารูเซลกิจกรรม")
    else:
        print("index.html : คารูเซลมีแล้ว ข้าม")

    IDX.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main()

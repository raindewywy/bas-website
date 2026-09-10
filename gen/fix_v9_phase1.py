#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v9_phase1.py — REQUIREMENTS v9 · เฟส 1–4
  REQ-C1/C2 : ยุบ :root สองชุดเป็นชุดเดียว (brand scale anchored #00B3C9) + กวาด hex hardcode
  REQ-M1–M3: พื้นหลังกรอบรูปเป็นกลาง · ปิดลายตารางเมื่อมีรูปจริง · ตัด CSS ซ้ำ
  REQ-H1    : เพิ่ม variant .page-hero--image
  REQ-H2    : แทรก <img class="hero-bg"> ในทุกหน้าที่กำหนด

รันซ้ำได้ (idempotent) — ใช้ marker กันการ patch ซ้ำ
    python gen/fix_v9_phase1.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"
MARK = "/* == v9 phase 1 =="

changed = []


def log(msg):
    print(f"  {msg}")


# ---------------------------------------------------------------- REQ-C1 ----
NEW_TOKENS = """  /* ---- Brand scale — anchored on #00B3C9 (v9) ------------------------- */
  --brand-50 :#EAF8FB;   /* wash อ่อนสุด */
  --brand-100:#CDEEF6;   /* wash */
  --brand-300:#7CDDF0;   /* eyebrow / ไอคอนบนพื้นเข้ม */
  --brand-400:#00CBEB;   /* accent สว่าง / hover / underline */
  --brand-500:#00B3C9;   /* PRIMARY — fill, rule, ไอคอนขนาดใหญ่ */
  --brand-600:#0091AD;   /* border, icon เล็ก (AA non-text) */
  --brand-700:#00718C;   /* TEXT/LINK บนพื้นขาว (AA) */
  --brand-800:#0A4E6B;   /* พื้นเข้มรอง */
  --brand-900:#0B3A57;   /* พื้นเข้มหลัก: page-hero, cta-band */

  /* ---- Aliases เดิม — ให้ rule เก่าทำงานต่อโดยไม่ต้องไล่แก้ ---- */
  --brand:      var(--brand-500);
  --brand-ink:  var(--brand-700);   /* แก้บั๊ก contrast 1.87:1 -> 5.6:1 */
  --brand-deep: var(--brand-900);
  --brand-tint: var(--brand-50);
  --brand-tint-2:var(--brand-100);
  --teal-400:   var(--brand-500);
  --teal-600:   var(--brand-700);
  --teal-700:   var(--brand-900);
  --deep-900:   var(--brand-900);
  --deep-800:   var(--brand-800);
"""

OLD_TOKENS_RE = re.compile(
    r"  /\* ---- Brand color system.*?--teal-700:var\(--brand-deep\);\n",
    re.S,
)

# ลบ :root block ชุดที่สอง (v3 sections) — ย้ายค่าขึ้นไปรวมข้างบนแล้ว
SECOND_ROOT_RE = re.compile(
    r":root\{\n  --deep-900:.*?\n  --brand-300:[^\n]*\n\}\n", re.S
)

# ---------------------------------------------------------------- REQ-C2 ----
HEX_MAP = {
    # เขียวอมฟ้าเข้ม -> น้ำเงินเข้มหลัก
    "#00505c": "var(--brand-900)",
    "#00525e": "var(--brand-900)",
    "#005a66": "var(--brand-900)",
    # เขียวอมเทาเข้ม -> น้ำเงินเข้มรอง
    "#063c45": "var(--brand-800)",
    "#062a31": "var(--brand-800)",
    "#0a2c32": "var(--brand-800)",
    "#0b3b43": "var(--brand-800)",
    "#18242a": "var(--brand-800)",
    # เขียวอมฟ้ากลาง -> ฟ้าเข้มสำหรับตัวอักษร
    "#087783": "var(--brand-700)",
    "#0e6d7b": "var(--brand-700)",
    "#007685": "var(--brand-700)",
    "#006775": "var(--brand-700)",
    "#0098ac": "var(--brand-600)",
    # accent สว่างเดิม
    "#06d0eb": "var(--brand-500)",
    "#7fe0ec": "var(--brand-300)",
    "#5cc3d0": "var(--brand-300)",
    "#43c9da": "var(--brand-300)",
    # wash
    "#d7f3f7": "var(--brand-100)",
    "#bfeff2": "var(--brand-100)",
    "#e8f7fa": "var(--brand-50)",
    "#e9f8fa": "var(--brand-50)",
    "#cdedf3": "var(--brand-100)",
}

RGBA_MAP = {
    "rgba(6,38,44,.55)": "rgba(11,58,87,.55)",
    "rgba(0,88,102,.32)": "rgba(11,58,87,.28)",
    "rgba(0,88,102,.22)": "rgba(11,58,87,.22)",
    "rgba(0,44,51,.45)": "rgba(11,58,87,.45)",
    "rgba(0,88,102,.35)": "rgba(11,58,87,.35)",
}

# จุดที่ตัวอักษรเป็นสีขาวทับพื้น -> ต้องใช้ brand-700 ไม่ใช่ brand-500 (AA)
WHITE_ON_BRAND = [
    (".card-tag.cat{background:var(--brand-500); color:#fff;}",
     ".card-tag.cat{background:var(--brand-700); color:#fff;}"),
    (".card-tag{background:var(--brand-500); color:#fff; border-radius:2px;}",
     ".card-tag{background:var(--brand-700); color:#fff; border-radius:2px;}"),
    # ปุ่มหลัก — ขาวบน brand-500 = 2.53:1 ตก AA
    (".btn-primary{background:var(--brand-500); color:#fff;}",
     ".btn-primary{background:var(--brand-700); color:#fff;}"),
    # ปุ่มลอยสายตรงคณบดี — ตัวอักษรขาวตัวเล็กหนา
    ("  background:var(--brand-500); color:#fff; text-shadow:0 1px 2px rgba(11,58,87,.45); border-radius:99px;",
     "  background:var(--brand-700); color:#fff; text-shadow:0 1px 2px rgba(11,58,87,.45); border-radius:99px;"),
    # ไอคอนขาวในวงกลม — ต้อง >= 3:1 (non-text AA)
    ("  background:var(--brand-500); color:#fff;\n  display:flex; align-items:center; justify-content:center;",
     "  background:var(--brand-600); color:#fff;\n  display:flex; align-items:center; justify-content:center;"),
    # เมนู mega / drawer ตอน hover — ตัวอักษรขาว
    (".mega a:hover, .mega a:focus-visible{background:var(--brand-500); color:#fff; border-left-color:var(--brand-500);}",
     ".mega a:hover, .mega a:focus-visible{background:var(--brand-700); color:#fff; border-left-color:var(--brand-700);}"),
    (".drawer-sub a:hover, .drawer-sub a:focus-visible{background:var(--brand-500); color:#fff;}",
     ".drawer-sub a:hover, .drawer-sub a:focus-visible{background:var(--brand-700); color:#fff;}"),
    ("background:var(--brand-500); color:#fff; text-shadow:0 1px 2px rgba(11,58,87,.45);\n  border-color:var(--brand-500);",
     "background:var(--brand-700); color:#fff; text-shadow:0 1px 2px rgba(11,58,87,.45);\n  border-color:var(--brand-700);"),
]

# ---------------------------------------------------------------- REQ-M -----
MEDIA_FIXES = [
    # .hero-media — เขียวเข้ม -> ไล่เฉดน้ำเงินแบรนด์
    ("background:linear-gradient(135deg,#0A4650,#123B44);",
     "background:linear-gradient(135deg,var(--brand-800),var(--brand-900));"),
    # REQ-M3 — .card-media ประกาศซ้ำที่บรรทัด ~614 (โดน rule ที่ 1533 ทับอยู่แล้ว)
    (".card-media{aspect-ratio:16/10; position:relative; background:linear-gradient(135deg,var(--paper-dim),var(--line));}",
     ".card-media{aspect-ratio:16/10; position:relative;}"),
    # REQ-M3 — .story-media ประกาศซ้ำที่บรรทัด ~647
    (".story-media{aspect-ratio:4/3; border-radius:var(--radius-l); overflow:hidden; background:linear-gradient(135deg,var(--paper-dim),var(--line)); position:relative;}",
     ".story-media{aspect-ratio:4/3; border-radius:var(--radius-l); overflow:hidden; position:relative;}"),
    # REQ-M1 — พื้นหลังกรอบรูป = เทากลาง
    (".card-media{background:var(--surface-2); border-bottom:1px solid var(--line);}",
     ".card-media{background:#EDEFF1; border-bottom:1px solid var(--line);}"),
    (""".story-media{
  border-radius:var(--radius-s); border:1px solid var(--line);
  background:linear-gradient(180deg,var(--surface),var(--surface-2));
}""",
     """.story-media{
  border-radius:var(--radius-s); border:1px solid var(--line);
  background:#EDEFF1;
}"""),
]

# ------------------------------------------------------- REQ-M1 / H1 CSS ----
V9_CSS = """

/* == v9 phase 1 == REQ-M1 · REQ-H1 ======================================
   พื้นหลังกรอบรูปเป็นกลาง (ไม่มี hue) + page-hero ที่มีรูป banner
   ===================================================================== */

/* ---- REQ-M1: neutral placeholder ระหว่างรูปโหลด ---------------------- */
.story-media, .card-media, .act-media, .split-media, .news-thumb, .staff-photo{
  background:#EDEFF1;
}
/* ปิดลายตารางตกแต่งเมื่อมีรูปจริงแล้ว */
.story-media:has(> .media-img)::after,
.card-media:has(> .media-img)::after,
.story-media:has(> picture)::after,
.card-media:has(> picture)::after{ display:none; }

/* ---- REQ-H1: page-hero variant ที่มีรูป banner ----------------------- */
.page-hero--image{ position:relative; isolation:isolate; }
.page-hero--image > .hero-bg{
  position:absolute; inset:0; z-index:-2;
  width:100%; height:100%; object-fit:cover; object-position:center;
}
.page-hero--image::before{               /* scrim ให้ตัวอักษรอ่านออก */
  content:""; position:absolute; inset:0; z-index:-1;
  background:linear-gradient(90deg,
    rgba(11,58,87,.92) 0%, rgba(11,58,87,.78) 45%, rgba(11,58,87,.42) 100%);
}
.page-hero--image::after{ display:none; }  /* ปิดวงกลม radial เดิม */
@media (max-width:760px){
  .page-hero--image::before{ background:rgba(11,58,87,.86); }
  .page-hero--image > .hero-bg{ object-position:50% 35%; }
}
"""

# ---------------------------------------------------------------- REQ-H2 ----
HERO_IMAGES = {
    "about.html": ("assets/media/hero-banner.jpg", "บรรยากาศคณะบริหารธุรกิจเพื่อสังคม"),
    "programs.html": ("assets/media/banner-program.jpg", "หลักสูตรของคณะ"),
    "student-life.html": ("assets/media/campus-life.jpg", "ชีวิตนิสิตในแคมปัส"),
    "leadership.html": ("assets/media/banner-news.jpg", "ผู้บริหารคณะ"),
    "departments.html": ("assets/media/banner-showcase.jpg", "ภาควิชาของคณะ"),
    "news.html": ("assets/media/bas-news.jpg", "ข่าวและกิจกรรมของคณะ"),
    "faculty.html": ("assets/media/academic-research.jpg", "คณาจารย์และงานวิจัย"),
    "admissions.html": ("assets/media/banner-admissions.jpg", "การรับสมัคร"),
    "international.html": ("assets/media/banner-exchange.jpg", "โครงการนานาชาติและแลกเปลี่ยน"),
    "honours.html": ("assets/media/banner-ukpsf.jpg", "รางวัลและความสำเร็จของคณะ"),
    "contact.html": ("assets/media/banner-inmotion.jpg", "ติดต่อคณะ"),
    # green-award.html รอไฟล์ banner-greenoffice.jpg (REQ-E1 เฟสถัดไป)
}

HERO_TPL = (
    '<section class="page-hero page-hero--image">'
    '<img class="hero-bg" src="{src}" alt="" aria-hidden="true" '
    'loading="eager" decoding="async" fetchpriority="high">'
)


def patch_css():
    src = CSS.read_text(encoding="utf-8")
    orig = src

    if MARK in src:
        log("styles.css: มี marker v9 อยู่แล้ว — ข้าม")
        return

    # REQ-C1
    src, n = OLD_TOKENS_RE.subn(NEW_TOKENS, src, count=1)
    if not n:
        sys.exit("!! หา brand token block เดิมไม่เจอ — หยุดก่อนเพื่อความปลอดภัย")
    src = src.replace("  --focus:#00505C;", "  --focus:var(--brand-700);", 1)

    src, n2 = SECOND_ROOT_RE.subn(
        "/* :root ชุดที่สองถูกยุบเข้าชุดหลักด้านบนแล้ว (REQ-C1 v9) */\n", src, count=1
    )
    if not n2:
        sys.exit("!! หา :root ชุดที่สองไม่เจอ")
    log("REQ-C1: ยุบ token 2 ชุด -> ชุดเดียว")

    # REQ-M (ทำก่อนกวาด hex เพราะ pattern อ้าง hex เดิม)
    for old, new in MEDIA_FIXES:
        if old not in src:
            sys.exit(f"!! หา pattern REQ-M ไม่เจอ: {old[:60]}")
        src = src.replace(old, new)
    log("REQ-M1/M3: พื้นกรอบรูปเป็นกลาง + ตัด rule ซ้ำ")

    # REQ-C2
    def sweep(text):
        def repl(m):
            return HEX_MAP.get(m.group(0).lower(), m.group(0))
        return re.sub(r"#[0-9a-fA-F]{6}\b", repl, text)

    src = sweep(src)
    for old, new in RGBA_MAP.items():
        src = src.replace(old, new)
    for old, new in WHITE_ON_BRAND:
        src = src.replace(old, new)
    log("REQ-C2: กวาด hex hardcode -> var()")

    # REQ-H1 + REQ-M1 block
    src = src.rstrip("\n") + "\n" + V9_CSS
    CSS.write_text(src, encoding="utf-8")
    changed.append(str(CSS.relative_to(ROOT)))
    log(f"เขียน styles.css ({len(orig)} -> {len(src)} bytes)")


def patch_pages():
    for name, (src_img, alt_note) in HERO_IMAGES.items():
        p = ROOT / name
        if not p.exists():
            log(f"!! ไม่พบ {name}")
            continue
        html = p.read_text(encoding="utf-8")
        if "page-hero--image" in html:
            log(f"{name}: มี hero image แล้ว — ข้าม")
            continue
        if '<section class="page-hero">' not in html:
            log(f"!! {name}: หา <section class=\"page-hero\"> ไม่เจอ")
            continue
        html = html.replace(
            '<section class="page-hero">',
            HERO_TPL.format(src=src_img),
            1,
        )
        p.write_text(html, encoding="utf-8")
        changed.append(name)
        log(f"{name}: hero -> {src_img}  ({alt_note})")


if __name__ == "__main__":
    print("REQ-C1/C2 · REQ-M · REQ-H1/H2")
    patch_css()
    patch_pages()
    print(f"\nแก้ไขแล้ว {len(changed)} ไฟล์")

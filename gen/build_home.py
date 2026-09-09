# -*- coding: utf-8 -*-
"""หน้าแรก: hero เต็มแบนเนอร์ (วิดีโอ) · ตัวเลขวิ่งชุดใหม่ · สายตรงคณบดี · หมวดหมู่ข่าว"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "index.html"
s = IDX.read_text(encoding="utf-8")

# ---------------------------------------------------------------- 1. HERO ----
HERO = """<section class="home-hero hero-full" id="hero">
  <div class="hero-video">
    <video id="hero-video" autoplay muted loop playsinline preload="none"
           poster="assets/media/hero-poster.jpg"
           data-poster-desktop="assets/media/hero-poster.jpg"
           data-poster-mobile="assets/media/hero-poster-mobile.jpg"
           data-src-desktop="assets/media/hero.mp4"
           data-src-mobile="assets/media/hero-mobile.mp4"></video>
  </div>
  <div class="hero-scrim"></div>
  <div class="wrap">
    <div class="hero-inner">
      <p class="eyebrow th-body">มหาวิทยาลัยศรีนครินทรวิโรฒ</p>
      <h1 class="bi-heading"><span class="bi-th th-body">บริหารธุรกิจ เพื่อสังคมที่ดีกว่า</span><span class="bi-en" style="font-size:.4em;">Business Education for a Better Society</span></h1>
      <p class="lede th-body">คณะบริหารธุรกิจเพื่อสังคม มศว บ่มเพาะผู้นำธุรกิจที่มีความสามารถและยึดมั่นในจริยธรรม โดยให้ความสำคัญกับผู้คนและสังคมควบคู่ไปกับผลกำไร</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="admissions.html">สมัครเรียนตอนนี้</a>
        <a class="btn btn-ghost-invert" href="programs.html">สำรวจหลักสูตร</a>
      </div>
    </div>
  </div>
  <div class="hero-controls">
    <span class="hero-caption-chip th-body">วิดีโอแนะนำคณะ — รอไฟล์จริง (แสดงภาพนิ่งแทน)</span>
    <button type="button" class="hero-toggle" id="hero-toggle" aria-pressed="false" aria-label="หยุดวิดีโอพื้นหลัง">
      <svg class="ico-pause" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>
      <svg class="ico-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5l12 7-12 7z"/></svg>
    </button>
  </div>
</section>"""

a = s.index('<section class="home-hero">')
b = s.index('<section class="quick-band">')
s = s[:a] + HERO + "\n\n" + s[b:]

# --------------------------------------------------- 2. ตัวเลขวิ่งชุดใหม่ ----
ICONS = {
    "students": '<path d="M4 9l8-4 8 4-8 4z"/><path d="M6 11v4c0 1.7 2.7 3 6 3s6-1.3 6-3v-4"/>',
    "bachelor": '<path d="M12 4l8 4-8 4-8-4z"/><path d="M20 8v6"/>',
    "master": '<path d="M6 20V9l6-4 6 4v11"/><path d="M10 20v-5h4v5"/>',
    "phd": '<circle cx="12" cy="9" r="4"/><path d="M9 13l-1 7 4-2 4 2-1-7"/>',
    "faculty": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3 2.7-5 6-5s6 2 6 5"/><path d="M16 8h5M16 12h5M16 16h5"/>',
    "programs": '<path d="M4 5h7v14H4z"/><path d="M13 5h7v14h-7z"/>',
}
STATS = [
    ("students", "3,776", "นิสิตทั้งหมด", "Total students"),
    ("bachelor", "3,420", "ระดับปริญญาตรี", "Bachelor's degree"),
    ("master", "339", "ระดับปริญญาโท", "Master's degree"),
    ("phd", "17", "ระดับปริญญาเอก", "Doctoral"),
    ("faculty", "38", "อาจารย์ประจำ", "Faculty members"),
    ("programs", "9", "หลักสูตร", "Degree programs"),
]


def stat_tile(key, value, th, en):
    return (
        '<div class="stat-tile-v2 reveal">'
        '<span class="stat-ico" aria-hidden="true"><svg viewBox="0 0 24 24" stroke-linecap="round" '
        'stroke-linejoin="round">%s</svg></span>'
        '<div class="value" data-count-to="%s">%s</div>'
        '<div class="label th-body">%s<span class="en">%s</span></div>'
        "</div>" % (ICONS[key], value, value, th, en)
    )


NEW_STATS = (
    '<div class="mt-6"><div class="stat-band-v2 reveal"><div class="stat-grid-v2">'
    + "".join(stat_tile(*x) for x in STATS)
    + '</div><p class="stat-source th-body">ข้อมูลจากเว็บไซต์คณะ · ต้องยืนยันปีการศึกษาที่อ้างอิงกับงานทะเบียนก่อนเผยแพร่</p>'
    + "</div></div>"
)
old_stats = re.search(r'<div class="mt-6"><div class="stat-band reveal">.*?</div></div></div>', s, re.S)
assert old_stats, "stat band not found"
s = s[: old_stats.start()] + NEW_STATS + s[old_stats.end():]

# ------------------------------------------- 3. หมวดหมู่ข่าวบนหน้าแรก ----
CATS = [
    ("pr", "ข่าวประชาสัมพันธ์"),
    ("campus", "รอบรั้ว BAS"),
    ("academic", "วิชาการและวิจัย"),
    ("inter", "ความร่วมมือและนานาชาติ"),
    ("scholarship", "ทุนการศึกษา"),
    ("job", "รับสมัครงาน / จัดซื้อจัดจ้าง"),
]
cat_bar = (
    '<div class="cat-bar">'
    + "".join('<a class="cat-chip th-body" href="news.html?cat=%s">%s</a>' % (k, v) for k, v in CATS)
    + "</div>"
)
marker = '<a class="news-feature reveal" href="news-detail.html?n=york-university-visit">'
i = s.index(marker, s.index('<p class="eyebrow">ข่าวและกิจกรรม</p>'))
s = s[:i] + cat_bar + "\n    " + s[i:]

# ----------------------------------------------------- 4. สายตรงคณบดี ----
DEAN = """
<div class="dean-direct-wrap">
  <a class="dean-direct" id="dean-direct" href="contact.html#dean-direct">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z"/></svg>
    <span class="label th-body">สายตรงคณบดี</span>
    <button type="button" class="dean-direct-close" id="dean-direct-close" aria-label="ปิดปุ่มสายตรงคณบดี">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
  </a>
</div>
"""
s = s.replace("</main>", DEAN + "</main>", 1)

IDX.write_text(s, encoding="utf-8")
print("index.html rebuilt: hero / stats / cat-bar / dean-direct")

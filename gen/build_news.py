# -*- coding: utf-8 -*-
"""
หน้าข่าว: จัดระบบหมวดหมู่ใหม่ (อ้างอิงชุดหมวดหมู่จาก swu.ac.th แล้วปรับให้เข้ากับคณะ)
+ deep link ?cat=<slug> จากหน้าแรก + empty state เมื่อหมวดยังไม่มีข่าว
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATS = [
    ("all", "ทั้งหมด"),
    ("pr", "ข่าวประชาสัมพันธ์"),
    ("campus", "รอบรั้ว BAS"),
    ("academic", "วิชาการและวิจัย"),
    ("inter", "ความร่วมมือและนานาชาติ"),
    ("scholarship", "ทุนการศึกษา"),
    ("job", "รับสมัครงาน / จัดซื้อจัดจ้าง"),
]

# จัดหมวดข่าวจริง 5 ชิ้นที่มีอยู่ (ไม่แต่งข่าวเพิ่ม)
MAP = {
    "york-university-visit": "inter",
    "mou-brokenshire-college": "inter",
    "germany-exchange-opportunity": "inter",
    "frankfurt-school-exchange": "inter",
    "cross-cultural-branding-lecture": "academic",
}
LABEL = dict(CATS)

p = ROOT / "news.html"
s = p.read_text(encoding="utf-8")

# ---- 1. แถบหมวดหมู่ใหม่ ----
bar = (
    '<div class="filter-bar" data-filter-group data-filter-target="[data-filter]" id="news-cats">'
    + "".join(
        '<button class="filter-chip th-body" aria-pressed="%s" data-filter-value="%s">%s</button>'
        % ("true" if k == "all" else "false", k, v)
        for k, v in CATS
    )
    + "</div>"
)
s = re.sub(r'<div class="filter-bar".*?</div>', lambda _: bar, s, count=1, flags=re.S)

# ---- 2. ใส่หมวดให้การ์ดแต่ละใบ + ป้ายหมวดบนการ์ด ----
for slug, cat in MAP.items():
    s = re.sub(
        r'(<a class="card[^"]*")([^>]*?)(href="news-detail\.html\?n=%s")' % re.escape(slug),
        lambda m: m.group(1) + ' data-filter="%s"' % cat + m.group(3),
        s,
    )
# ลบ data-filter เดิม (news/event) ที่ตกค้าง
s = re.sub(r'\sdata-filter="(news|event)"', "", s)

# ป้ายหมวดบนการ์ด: แทน "กิจกรรม"/"ข่าว" เดิม
for slug, cat in MAP.items():
    i = s.find('href="news-detail.html?n=%s"' % slug)
    while i != -1:
        j = s.find('<span class="card-tag', i)
        if j != -1 and j - i < 900:
            k = s.index("</span>", j)
            s = s[:j] + '<span class="card-tag cat">%s' % LABEL[cat] + s[k:]
        i = s.find('href="news-detail.html?n=%s"' % slug, i + 1)

# ---- 3. empty state ----
if "news-empty" not in s:
    empty = (
        '<p class="notice th-body" id="news-empty" hidden style="margin-top:var(--space-5);">'
        "<span>ยังไม่มีข่าวในหมวดนี้ — ข่าวเดิมบนเว็บไซต์ปัจจุบันยังไม่ได้ย้ายเข้ามาในต้นแบบ "
        "ต้นแบบนี้แสดงเฉพาะข่าวที่ยืนยันได้จากเว็บไซต์ทางการ 5 ชิ้นเท่านั้น</span></p>"
    )
    s = s.replace("</main>", empty + "\n</main>", 1)

# ---- 4. หมายเหตุชุดหมวดหมู่ ----
if "cat-note" not in s:
    note = (
        '<p class="notice th-body" id="cat-note" style="margin-bottom:var(--space-4);">'
        "<span>ชุดหมวดหมู่นี้อ้างอิงโครงจากเว็บไซต์ มศว (swu.ac.th) แล้วปรับให้เข้ากับระดับคณะ "
        "— <strong>รอคณะยืนยันชื่อหมวดหมู่ที่ต้องการใช้จริง</strong> ก่อนนำไปผูกกับระบบหลังบ้าน</span></p>"
    )
    s = s.replace(bar, note + bar, 1)

p.write_text(s, encoding="utf-8")
print("news.html: categories applied")

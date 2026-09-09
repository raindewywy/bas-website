# -*- coding: utf-8 -*-
"""
remove_podcast — ลบแถบ "BAS SWU Podcast" ออกจากเว็บทั้งชุด

ลบ 3 อย่าง เพื่อไม่ให้เหลือลิงก์ตายหรือ CSS กำพร้า:
  1) <section id="podcast"> … </section>   ในทุกไฟล์ HTML (อยู่ในเชลล์ร่วม จึงมีทุกหน้า)
  2) <li><a href="#podcast">BAS SWU Podcast</a></li>  ในฟุตเตอร์ทุกหน้า
  3) บล็อก CSS .podcast-* ใน assets/styles.css

รันซ้ำได้ — ถ้าไม่เจอก็ข้าม
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECTION_RE = re.compile(
    r'\n*<section class="section-tight" id="podcast">.*?</section>\n*', re.S
)
FOOTER_LI_RE = re.compile(
    r'\s*<li><a href="#podcast">[^<]*</a></li>', re.S
)


def strip_html(path: Path) -> tuple:
    s = path.read_text(encoding="utf-8")
    before = s
    s, n_sec = SECTION_RE.subn("\n\n", s)
    s, n_li = FOOTER_LI_RE.subn("", s)
    if s != before:
        path.write_text(s, encoding="utf-8")
    return n_sec, n_li


def strip_css(path: Path) -> int:
    s = path.read_text(encoding="utf-8")
    out, removed = [], 0
    for line in s.splitlines(keepends=True):
        if re.match(r'\s*\.podcast[-\w]*\b', line) or ".podcast-" in line.split("{")[0]:
            removed += 1
            continue
        out.append(line)
    new = "".join(out)
    # เก็บกวาดบรรทัดคอมเมนต์หัวข้อที่เหลือลอย
    new = re.sub(r'\n/\*[^*]*[Pp]odcast[^*]*\*/\n', "\n", new)
    if new != s:
        path.write_text(new, encoding="utf-8")
    return removed


def main():
    tot_sec = tot_li = 0
    for f in sorted(ROOT.glob("*.html")):
        a, b = strip_html(f)
        tot_sec += a
        tot_li += b
        if a or b:
            print("%-38s section:%d  footer-link:%d" % (f.name, a, b))
    print("---")
    print("รวม: ลบ section %d บล็อก · ลิงก์ฟุตเตอร์ %d รายการ" % (tot_sec, tot_li))
    n = strip_css(ROOT / "assets" / "styles.css")
    print("styles.css: ลบกฎ .podcast-* %d บรรทัด" % n)


if __name__ == "__main__":
    main()

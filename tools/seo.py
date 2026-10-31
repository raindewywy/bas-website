"""สร้าง SEO ของทั้งเว็บจากที่เดียว — รันซ้ำได้ทุกครั้งที่เพิ่ม/แก้หน้า

    python tools/seo.py                      ใช้ SITE_URL ด้านล่าง
    python tools/seo.py https://example.com  ใช้โดเมนอื่น (เช่นตอนย้าย host)

ทำ 3 อย่าง:
  1. แทรก canonical + Open Graph + Twitter card ลงทุกหน้า ระหว่าง
     <!-- seo:start --> ... <!-- seo:end --> (ใต้ <meta name="description">)
     ค่า og:title / og:description ดึงจาก <title> และ <meta name="description"> ของหน้านั้นเอง
     → อยากแก้ข้อความ ให้แก้ที่ <title>/<meta description> แล้วรันสคริปต์นี้ใหม่ อย่าแก้ในบล็อก seo
  2. เขียน sitemap.xml — หน้าปกติ + หน้า dynamic ทุกรายการใน assets/data.js
     (program-detail.html?p=, profile.html?p=, news-detail.html?n=)
  3. เขียน robots.txt

หน้าที่ข้าม: หน้า redirect (meta refresh) · หน้า noindex (admin, 404)
"""
import json
import re
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

SITE_URL = "https://raindewywy.github.io/bas-website"
SITE_NAME = "BAS SWU — คณะบริหารธุรกิจเพื่อสังคม มศว"
DEFAULT_IMAGE = "assets/media/hero-banner.jpg"

# ภาพแชร์เฉพาะหน้า (ไม่อยู่ในนี้ → DEFAULT_IMAGE) · ควรเป็นภาพแนวนอนราว 1200×630
PAGE_IMAGE = {
    "about.html": "assets/media/bas-building.jpg",
    "admissions.html": "assets/media/banner-admissions.jpg",
    "programs.html": "assets/media/banner-program.jpg",
    "program-detail.html": "assets/media/program-detail.jpg",
    "faculty.html": "assets/media/hero-faculty.jpg",
    "leadership.html": "assets/media/leadership-hero.jpg",
    "staff-deans-office.html": "assets/media/hero-deans-office.jpg",
    "news.html": "assets/media/banner-news.jpg",
    "news-detail.html": "assets/media/news-detail-default.jpg",
    "international.html": "assets/media/banner-exchange.jpg",
    "sustainability.html": "assets/media/banner-greenoffice.jpg",
    "green-office-2568.html": "assets/media/banner-greenoffice.jpg",
    "student-life.html": "assets/media/campus-life.jpg",
    "student-services.html": "assets/media/banner-student-support.jpg",
    "academic-calendar.html": "assets/media/calendar-hero.jpg",
}

# หน้าเดียวแต่เนื้อหาเปลี่ยนตาม query string — ไม่ใส่ canonical/og:url (จะชี้ผิดรายการ)
# ค่า: (ชื่อตัวแปรใน data.js, field ที่เป็น id, ชื่อ query param)
DYNAMIC_PAGES = {
    "program-detail.html": ("BAS_PROGRAMS", "slug", "p"),
    "profile.html": ("BAS_PEOPLE", "id", "p"),
    "news-detail.html": ("BAS_NEWS", "slug", "n"),
}

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- seo:start -->", "<!-- seo:end -->"
BLOCK_RE = re.compile(r"\n?" + re.escape(START) + r".*?" + re.escape(END), re.S)


def attr(text):
    return escape(text, {'"': "&quot;"})


def head_value(html, pattern):
    m = re.search(pattern, html, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def is_indexable(html):
    return 'http-equiv="refresh"' not in html and not re.search(r'name="robots"[^>]*noindex', html)


def seo_block(page, html, site):
    title = head_value(html, r"<title>(.*?)</title>")
    desc = head_value(html, r'<meta name="description" content="([^"]*)"')
    image = f"{site}/{PAGE_IMAGE.get(page, DEFAULT_IMAGE)}"
    url = site + "/" if page == "index.html" else f"{site}/{page}"
    tags = []
    if page not in DYNAMIC_PAGES:
        tags.append(f'<link rel="canonical" href="{url}">')
    tags += [
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{attr(SITE_NAME)}">',
        '<meta property="og:locale" content="th_TH">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
    ]
    if page not in DYNAMIC_PAGES:
        tags.append(f'<meta property="og:url" content="{url}">')
    tags += [
        f'<meta property="og:image" content="{image}">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    return "\n".join([START, *tags, END])


def update_pages(site):
    pages = []
    for path in sorted(ROOT.glob("*.html")):
        html = path.read_bytes().decode("utf-8")  # คง line ending เดิมของไฟล์
        if not is_indexable(html):
            continue
        cleaned = BLOCK_RE.sub("", html)
        anchor = re.search(r'<meta name="description"[^>]*>', cleaned)
        if not anchor:
            print(f"ข้าม {path.name}: ไม่มี <meta name=\"description\">")
            continue
        block = seo_block(path.name, cleaned, site)
        new = cleaned[: anchor.end()] + "\n" + block + cleaned[anchor.end():]
        if new != html:
            path.write_bytes(new.encode("utf-8"))
        pages.append(path.name)
    return pages


def load_data():
    """อ่าน window.BAS_* ที่เป็น JSON บรรทัดเดียวจาก assets/data.js (ตัวที่เขียนหลายบรรทัดจะถูกข้าม)"""
    data = {}
    src = (ROOT / "assets" / "data.js").read_text(encoding="utf-8")
    for name, body in re.findall(r"^window\.(BAS_\w+)\s*=\s*(.+?);?\s*$", src, re.M):
        try:
            data[name] = json.loads(body)
        except json.JSONDecodeError:
            pass
    return data


def last_modified(page):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", page],
                         cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip()


def write_sitemap(pages, site):
    data = load_data()
    urls = []
    for page in pages:
        lastmod = last_modified(page)
        if page in DYNAMIC_PAGES:
            var, key, param = DYNAMIC_PAGES[page]
            urls += [(f"{site}/{page}?{param}={item[key]}", lastmod) for item in data.get(var, [])]
        else:
            urls.append((site + "/" if page == "index.html" else f"{site}/{page}", lastmod))
    rows = []
    for loc, lastmod in urls:
        mod = f"<lastmod>{lastmod}</lastmod>" if lastmod else ""
        rows.append(f"  <url><loc>{escape(loc)}</loc>{mod}</url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")
    return len(urls)


def write_robots(site):
    (ROOT / "robots.txt").write_text(
        "User-agent: *\n"
        "Disallow: /admin.html\n"
        f"\nSitemap: {site}/sitemap.xml\n",
        encoding="utf-8", newline="\n")


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows (cp1252) พิมพ์ภาษาไทยไม่ได้
    site = (sys.argv[1] if len(sys.argv) > 1 else SITE_URL).rstrip("/")
    pages = update_pages(site)
    count = write_sitemap(pages, site)
    write_robots(site)
    print(f"SEO: {len(pages)} หน้า · sitemap {count} URL · โดเมน {site}")


if __name__ == "__main__":
    main()

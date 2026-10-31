# BAS SWU — เว็บไซต์คณะบริหารธุรกิจเพื่อสังคม มศว

Static site · ไม่มี build step · ไม่มี runtime บนเซิร์ฟเวอร์ · deploy ทั้งโฟลเดอร์ root ได้ตรง ๆ

---

## โครงสร้าง

```
*.html                    หน้าเว็บทั้งหมด — ไฟล์ live แก้ตรงนี้ได้เลย
  leader-*.html, mou.html,  หน้า redirect (meta refresh) จาก URL เก่า → อย่าลบ ลิงก์ภายนอกยังชี้มาอยู่
  green-award.html
  404.html, admin.html      noindex — ไม่อยู่ใน sitemap
partials/
  nav.html                header + เมนู + mobile drawer + admin modal — ใช้ร่วมกันทุกหน้า
  footer.html             footer — ใช้ร่วมกันทุกหน้า
assets/
  include.js              โหลด partials/*.html มาแทรกในหน้าตอนเปิด
  styles.css              design system — token สี typography spacing + ทุก component
  data.js                 ข้อมูลทั้งเว็บ (ดูตารางด้านล่าง)
  greenoffice-data.js     รายการเอกสาร Green Office 2568 ทั้ง 6 หมวด
  script.js               พฤติกรรมทั้งหมด — nav, carousel, render หน้าจาก data.js
  media/                  รูปภาพ (people/, faculty/, leaders/, partners/, news/ …)
  cv/                     CV อาจารย์ (<id>.pdf ตรงกับ id ใน BAS_PEOPLE)
  docs/greenoffice/<1-6>/ เอกสารหลักฐาน Green Office แยกตามหมวด
tools/seo.py              สร้าง Open Graph · sitemap.xml · robots.txt (ดูหัวข้อ SEO)
sitemap.xml, robots.txt   ไฟล์ที่ tools/seo.py สร้าง — อย่าแก้มือ
requirement.docx/.pdf     ข้อกำหนดรอบปรับปรุงล่าสุด (R1–R7)
```

โฟลเดอร์ที่ **ไม่ใช่ส่วนของเว็บ** (ไม่ต้อง deploy): `_backup-*` (สำเนาก่อนแก้ครั้งใหญ่),
`export/` (แพ็กส่งออก อยู่ใน `.gitignore`), `.claude/`, `.hallmark/`, `.vscode/`

## แก้อะไร ที่ไหน

| ต้องการแก้ | แก้ที่ | หลังแก้ |
|---|---|---|
| เนื้อหาเฉพาะหน้า | `<หน้า>.html` | refresh |
| เมนู / mobile drawer | `partials/nav.html` (ทั้ง `.nav-list` และ `.drawer-body`) | refresh — ทุกหน้าเห็นผล |
| footer | `partials/footer.html` | refresh — ทุกหน้าเห็นผล |
| หลักสูตร ข่าว อาจารย์ บุคลากร ชมรม | `assets/data.js` | refresh |
| title / description ของหน้า | `<title>` และ `<meta name="description">` | รัน `python tools/seo.py` |
| เพิ่ม/ลบหน้า | สร้างไฟล์ + เพิ่มลิงก์ใน `partials/nav.html` | รัน `python tools/seo.py` |

### ข้อมูลใน `assets/data.js`

| ตัวแปร | ใช้ที่ | หมายเหตุ |
|---|---|---|
| `BAS_PROGRAMS` | programs, program-detail | `slug` ต้องมีรูป `assets/media/program-<slug>.jpg` |
| `BAS_PROGRAM_DEPT` | program-detail | slug → ภาควิชา |
| `BAS_NEWS`, `BAS_NEWS_CATS` | news, news-detail | `url` ว่าง = ไม่มีปุ่มไปข่าวต้นทาง |
| `BAS_PEOPLE` | profile, program-detail | `id` = ชื่อไฟล์ CV ใน `assets/cv/` · field ที่ว่างจะไม่แสดง |
| `BAS_DIRECTORY`, `BAS_DEPTS` | faculty | `id` ต้องตรงกับ `BAS_PEOPLE` |
| `BAS_DEPT_HEADS`, `BAS_LEADERSHIP` | program-detail | กล่องหัวหน้าภาควิชา (จับคู่ด้วยอีเมล) |
| `BAS_STAFF`, `BAS_STAFF_UNITS` | staff-deans-office | |
| `BAS_PARTNERS` | index | แผนที่พันธมิตรหน้าแรก |
| `BAS_CLUBS` | student-life `#clubs` | `desc`/`img`/`href` ว่าง = แสดง "รอข้อมูลจากคณะ" |

หน้า dynamic อ่านรายการจาก query string: `program-detail.html?p=<slug>` · `profile.html?p=<id>` · `news-detail.html?n=<slug>`

---

## nav/footer ทำงานยังไง

แต่ละหน้ามี placeholder แทน nav กับ footer:

```html
<body data-nav="about">
<div data-include="partials/nav.html"></div>
...
<div data-include="partials/footer.html"></div>
<script src="assets/data.js"></script>
<script src="assets/script.js"></script>
<script src="assets/include.js"></script>
```

`include.js` ดึง partials มาแทรก → ใส่คลาส `current` ให้เมนูที่ตรงกับ `data-nav` → เรียกฟังก์ชัน nav ใน `script.js`

**ต้องเปิดผ่าน http(s) เสมอ** — ดับเบิลคลิกเปิดไฟล์ (`file://`) nav/footer จะไม่ขึ้น เพราะเบราว์เซอร์บล็อก `fetch()` ไฟล์ local

## รันในเครื่อง

```bash
python -m http.server 8000
```

แล้วเปิด http://localhost:8000 (หรือ Live Server ใน VS Code ที่ root ของโปรเจกต์)

## SEO — `tools/seo.py`

```bash
python tools/seo.py
```

- แทรก canonical + Open Graph + Twitter card ลงทุกหน้าระหว่าง `<!-- seo:start -->` … `<!-- seo:end -->`
  โดยดึงข้อความจาก `<title>` และ `<meta name="description">` ของหน้านั้น — **อย่าแก้ในบล็อกนี้ด้วยมือ**
- เขียน `sitemap.xml` (หน้าปกติ + ทุกหลักสูตร/อาจารย์/ข่าวใน `data.js`) และ `robots.txt`
- รันซ้ำกี่ครั้งก็ได้ ผลเหมือนเดิม
- โดเมนตั้งที่ `SITE_URL` บนสุดของสคริปต์ ย้าย host: `python tools/seo.py https://โดเมนใหม่`
- ภาพแชร์เฉพาะหน้าตั้งใน `PAGE_IMAGE` (ไม่ระบุ = `hero-banner.jpg`)

> `robots.txt` มีผลเฉพาะเมื่ออยู่ที่ root ของโดเมน — ถ้า deploy ใต้ path (เช่น `github.io/bas-website/`)
> crawler จะไม่อ่านไฟล์นี้ ให้ส่ง `sitemap.xml` ผ่าน Google Search Console แทน

## Deploy

ทั้งเว็บอยู่ที่ root ของ repo — ไม่ต้อง build

| | Build command | Publish directory |
|---|---|---|
| GitHub Pages | — | Settings → Pages → Deploy from a branch → `main` / `(root)` |
| Vercel / Netlify | ปล่อยว่าง | `.` |

---

## หมายเหตุด้านเทคนิค

- **ไม่มี framework ฝั่ง client** — Tailwind ผ่าน CDN ใช้เฉพาะ utility layout ส่วน component อยู่ใน `assets/styles.css`
- **ไอคอนใช้ FontAwesome** ที่โหลดอยู่แล้ว — อย่าเพิ่ม icon library ใหม่
- **สีทั้งหมดอ้าง CSS custom property** ใน `:root` ชุดเดียว สีหลักคือ `#37CBCB` ห้าม hardcode hex ในไฟล์อื่น
- **ตัวอักษรสีขาวห้ามวางบน `--brand-500`** (contrast 1.99:1) ใช้ `--brand-700` ขึ้นไป
- เพิ่มหน้าใหม่: copy หน้าที่ใกล้เคียงที่สุด ตั้ง `<title>` / `<meta description>` / `data-nav` ใหม่ แล้วรัน `tools/seo.py`
- path รูป/CSS/JS เขียนแบบ relative (`assets/...`) เสมอ

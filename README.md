# BAS SWU — เว็บไซต์คณะบริหารธุรกิจเพื่อสังคม มศว

Static site · ไม่มี build step · ไม่มี runtime บนเซิร์ฟเวอร์ · deploy กับ Vercel / Netlify / GitHub Pages ได้ตรง ๆ

---

## โครงสร้าง

```
public/                  ทั้งเว็บอยู่ที่นี่ที่เดียว — โฟลเดอร์เดียวที่ต้อง deploy และเปิดด้วย Live Server
  *.html                 33 หน้า — ไฟล์ live แก้ตรงนี้ได้เลย ไม่มีไฟล์ต้นทางแยกที่อื่น
  partials/
    nav.html              header + เมนู + mobile drawer + admin modal — ใช้ร่วมกันทุกหน้า
    footer.html           footer — ใช้ร่วมกันทุกหน้า
  assets/
    include.js            โหลด partials/*.html มาแทรกในหน้าตอนเปิด (ดูหัวข้อ "nav/footer ทำงานยังไง")
    styles.css             Design system — token สี typography spacing + ทุก component
    data.js                Model ฝั่ง client — หลักสูตร ข่าว ภาควิชา ผู้บริหาร (โหลด runtime)
    script.js               พฤติกรรม — nav drawer, rail carousel, scroll reveal, marquee
    media/                  รูปภาพทั้งหมด
docs/                    REQUIREMENTS-v9.md · CHANGELOG-v9.md — ประวัติ/ข้อกำหนดรอบก่อน
gen/                      สคริปต์เตรียมรูป Green Office ที่ยังไม่ได้รัน (ดู gen/README.md)
```

**แก้ที่ไหน** — ไม่มี "ไฟล์ต้นทาง" กับ "ไฟล์ build" แยกกันอีกแล้ว แก้ที่เห็นได้เลย:

| ต้องการแก้ | แก้ที่ | ต้องรันอะไรไหม |
|---|---|---|
| เนื้อหาเฉพาะหน้า | `public/<หน้า>.html` | ไม่ต้อง |
| nav / เมนู / mobile drawer | `public/partials/nav.html` | ไม่ต้อง — ทุกหน้าเห็นผลทันที |
| footer | `public/partials/footer.html` | ไม่ต้อง — ทุกหน้าเห็นผลทันที |
| title / description ต่อหน้า | `<title>` และ `<meta name="description">` ใน `public/<หน้า>.html` | ไม่ต้อง |
| CSS · JS · รูปภาพ | `public/assets/` | ไม่ต้อง |

---

## nav/footer ทำงานยังไง (ไม่มี build step)

แต่ละหน้าใน `public/*.html` มี placeholder แทนที่ nav กับ footer:

```html
<body data-nav="about">
<div data-include="partials/nav.html"></div>
...
<div data-include="partials/footer.html"></div>
<script src="assets/data.js"></script>
<script src="assets/script.js"></script>
<script src="assets/include.js"></script>
```

`include.js` โหลดตอนเปิดหน้า → ดึง `partials/nav.html` และ `partials/footer.html` มาแทรกแทน placeholder
→ ใส่คลาส `current` ให้เมนูที่ตรงกับ `data-nav` บน `<body>` → เรียกฟังก์ชัน nav ใน `script.js`
(เปิด/ปิดเมนู มือถือ, ค้นหา, mega menu, admin modal) ให้ทำงานกับ nav ที่เพิ่งแทรกเข้ามา

**ข้อจำกัดเดียว: ต้องเปิดผ่าน http(s) เสมอ** — Live Server, `python -m http.server`,
Vercel/Netlify/GitHub Pages ใช้ได้หมด แต่ดับเบิลคลิกเปิดไฟล์ตรง ๆ (`file://`) ใช้ไม่ได้
เพราะเบราว์เซอร์บล็อก `fetch()` ของไฟล์ local ด้วย CORS — nav/footer จะไม่ขึ้น

## วิธีใช้

เปิดโฟลเดอร์ `public/` ด้วย Live Server (คลิกขวาที่ `public/index.html` → "Open with Live Server")
หรือ

```bash
python -m http.server 8000 --directory public
```

ไม่มีขั้นตอน build ใด ๆ — แก้ไฟล์ใน `public/` แล้ว refresh ดูผลได้ทันที

## Deploy

โฟลเดอร์ `public/` คือทั้งเว็บ — deploy โฟลเดอร์นี้ตรง ๆ ไม่ต้อง build command ใด ๆ

| | Build command | Publish / Output directory |
|---|---|---|
| Vercel | ปล่อยว่าง | `public` |
| Netlify | ปล่อยว่าง | `public` |
| GitHub Pages | โหมด "Deploy from a branch" รับแค่ root หรือ `/docs` — ต้องเปลี่ยน source เป็น **GitHub Actions** แล้วอัป `public/` เป็น Pages artifact (ดู `.github/workflows/deploy-pages.yml`) | n/a (Actions artifact) |

---

## หมายเหตุด้านเทคนิค

- **ไม่มี framework ฝั่ง client** — Tailwind ใช้ผ่าน CDN เฉพาะ utility layout ส่วน component ทั้งหมดอยู่ใน `public/assets/styles.css`
- **ไอคอนใช้ FontAwesome** ที่โหลดอยู่แล้ว — อย่าเพิ่ม icon library ใหม่
- **สีทั้งหมดอ้าง CSS custom property** ใน `:root` ชุดเดียว สีหลักคือ `#37CBCB` ห้าม hardcode hex ในไฟล์อื่น
- **ตัวอักษรสีขาวห้ามวางบน `--brand-500`** (contrast 1.99:1) ใช้ `--brand-700` ขึ้นไป
- เพิ่มหน้าใหม่: copy หน้าที่ใกล้เคียงที่สุด ตั้ง `<title>`/`<meta description>`/`data-nav` ใหม่
  แล้วเพิ่มลิงก์ในเมนูที่ `public/partials/nav.html` (ทั้ง `.nav-list` และ `.drawer-body`)
- path รูป/CSS/JS เขียนแบบ relative (`assets/...`) เพราะหน้าเว็บถูก serve จาก `public/` เสมอ

## เอกสารอื่น

- `docs/REQUIREMENTS-v9.md` — ข้อกำหนดรอบปรับปรุง v9
- `docs/CHANGELOG-v9.md` — สรุปสิ่งที่แก้ในรอบ v9 + ผลตรวจ acceptance
- `gen/README.md` — สคริปต์เตรียมรูป Green Office ที่เหลืออยู่ + ประวัติโครงสร้างเก่า

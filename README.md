# BAS SWU — เว็บไซต์คณะบริหารธุรกิจเพื่อสังคม มศว

Static site · ไม่มี runtime บนเซิร์ฟเวอร์ · deploy กับ Vercel / Netlify / GitHub Pages ได้ตรง ๆ

---

## โครงสร้าง

```
build.py                Controller — ประกอบ template + data ออกมาเป็น .html
data/
  pages.json            Model — metadata ของแต่ละหน้า (title, description, เมนูที่ active)
templates/
  base.html             View — โครงหน้าเดียวของทั้งเว็บ: <head> · header/nav · footer · script
  pages/*.html           View — เนื้อหาเฉพาะหน้า (เฉพาะส่วนใน <main>)
assets/
  styles.css            Design system — token สี typography spacing + ทุก component
  data.js               Model ฝั่ง client — หลักสูตร ข่าว ภาควิชา ผู้บริหาร
  script.js             พฤติกรรม — nav drawer, rail carousel, scroll reveal, marquee
  media/                รูปภาพทั้งหมด
*.html                  ผลลัพธ์ที่ build ออกมา — คอมมิตไว้เพื่อให้ deploy ได้ทันที
gen/                    สคริปต์ช่วยงานเฉพาะกิจ (ดู gen/README.md)
```

**กฎเดียวที่ต้องจำ: อย่าแก้ `.html` ที่ root โดยตรง** — ไฟล์พวกนี้ถูก `build.py` เขียนทับ
ให้แก้ที่ `templates/pages/<หน้า>.html` (เนื้อหา) หรือ `templates/base.html` (nav / footer / head)

---

## วิธีใช้

```bash
pip install -r requirements.txt

python build.py            # สร้าง .html ทั้ง 26 หน้าใหม่จาก template
python build.py --check    # ตรวจว่าไฟล์ที่คอมมิตไว้ตรงกับ template ไหม (ใช้ใน CI ได้)
```

ดูผลระหว่างพัฒนา: เปิดไฟล์ `.html` ตรง ๆ หรือ

```bash
python -m http.server 8000
```

## Deploy

ไฟล์ที่ต้องอัปคือ root ของ repo (`.html` + `assets/`) ทั้งสามเจ้าตั้งค่าเหมือนกัน:

| | Build command | Publish directory |
|---|---|---|
| Vercel / Netlify | `pip install -r requirements.txt && python build.py` | `.` |
| GitHub Pages | ไม่ต้อง build (คอมมิต `.html` ไว้แล้ว) | root branch |

ถ้าไม่อยากให้ CI รัน Python ก็ปล่อยว่างได้เลย เพราะ `.html` ถูกคอมมิตไว้ครบ

---

## หมายเหตุด้านเทคนิค

- **ไม่มี framework ฝั่ง client** — Tailwind ใช้ผ่าน CDN เฉพาะ utility layout ส่วน component ทั้งหมดอยู่ใน `assets/styles.css`
- **ไอคอนใช้ FontAwesome** ที่โหลดอยู่แล้ว — อย่าเพิ่ม icon library ใหม่
- **สีทั้งหมดอ้าง CSS custom property** ใน `:root` ชุดเดียว (`styles.css:8`) สีหลักคือ `#37CBCB` ห้าม hardcode hex ในไฟล์อื่น
- **ตัวอักษรสีขาวห้ามวางบน `--brand-500`** (contrast 1.99:1) ใช้ `--brand-700` ขึ้นไป
- `templates/base.html` มีตัวแปรแค่ 3 ตัว: `page.title` · `page.description` · `page.nav` (คีย์เมนูที่ต้อง active)

## เอกสารอื่น

- `REQUIREMENTS-v9.md` — ข้อกำหนดรอบปรับปรุง v9
- `CHANGELOG-v9.md` — สรุปสิ่งที่แก้ในรอบ v9 + ผลตรวจ acceptance
- `gen/README.md` — สคริปต์ใน `gen/` ตัวไหนยังใช้ ตัวไหนเลิกใช้แล้ว

# BAS SWU — เว็บไซต์คณะบริหารธุรกิจเพื่อสังคม มศว

Static site · ไม่มี runtime บนเซิร์ฟเวอร์ · deploy กับ Vercel / Netlify / GitHub Pages ได้ตรง ๆ

---

## โครงสร้าง (MVC)

```
build.py                 entry point — เรียก Controller (รันด้วย `python build.py`)
app/
  models/
    pages.py             Model — โหลด pages.json (load_pages())
    pages.json           Model — title, description, เมนูที่ active ของแต่ละหน้า
  views/
    base.html            View — โครงหน้าเดียวของทั้งเว็บ: <head> · header/nav · footer · script
    pages/*.html         View — เนื้อหาเฉพาะหน้า (เฉพาะส่วนใน <main>) · 33 หน้า
    partials/*.html      View — ชิ้นส่วนที่ใช้ร่วมกันหลายหน้า
  controllers/
    build_controller.py  Controller — render View ด้วย Jinja2 แล้วเขียน .html ลง public/
public/                  โฟลเดอร์ deploy — โฟลเดอร์เดียวที่ต้องขึ้น host
  *.html                 ผลลัพธ์ build (ห้ามแก้ — build.py เขียนทับ)
  assets/
    styles.css           Design system — token สี typography spacing + ทุก component
    data.js              Model ฝั่ง client — หลักสูตร ข่าว ภาควิชา ผู้บริหาร (โหลด runtime)
    script.js            พฤติกรรม — nav drawer, rail carousel, scroll reveal, marquee
    media/               รูปภาพทั้งหมด
docs/                    REQUIREMENTS-v9.md · CHANGELOG-v9.md
gen/                     สคริปต์เตรียมรูป Green Office ที่ยังไม่ได้รัน (ดู gen/README.md)
```

**แก้ที่ไหน**

| ต้องการแก้ | แก้ที่ |
|---|---|
| เนื้อหาหน้า | `app/views/pages/<หน้า>.html` |
| nav / footer / head | `app/views/base.html` |
| title / description / เมนูที่ active | `app/models/pages.json` |
| CSS · JS · รูปภาพ | `public/assets/` |

**กฎเดียวที่ต้องจำ: `public/*.html` เป็นไฟล์ที่ build ออกมา อย่าแก้ตรงนั้น**
แก้ที่ `app/views/` แล้วรัน `python build.py`

> `public/assets/` ต่างจาก `public/*.html` — เป็น **ต้นฉบับ** ที่แก้ได้ตรง ๆ
> `build.py` ไม่แตะโฟลเดอร์นี้เลย จึงไม่มีสำเนาซ้ำที่อื่น

---

## วิธีใช้

```bash
pip install -r requirements.txt

python build.py            # สร้าง .html ทั้ง 33 หน้าใหม่ใน public/
python build.py --check    # ตรวจว่าไฟล์ที่คอมมิตไว้ตรงกับ template ไหม (ใช้ใน CI ได้)
```

ดูผลระหว่างพัฒนา — เปิด `public/index.html` ด้วย Live Server หรือ

```bash
python -m http.server 8000 --directory public
```

> อย่าเปิด `app/views/pages/*.html` ด้วย Live Server — เป็น Jinja2 template ไม่ใช่ HTML ที่สมบูรณ์
> จะเห็นเป็นข้อความ `{% extends %}` และไม่มี CSS

## Deploy

ขึ้น host เฉพาะโฟลเดอร์ `public/` — คอมมิตไว้แล้ว ไม่ต้อง build ก็ deploy ได้ทันที

| | Build command | Publish / Output directory |
|---|---|---|
| Vercel | ปล่อยว่าง (หรือ `pip install -r requirements.txt && python build.py`) | `public` |
| Netlify | เหมือนกัน | `public` |
| GitHub Pages | โหมด "Deploy from a branch" รับแค่ root หรือ `/docs` — ต้องเปลี่ยน source เป็น **GitHub Actions** แล้วอัป `public/` เป็น Pages artifact | n/a (Actions artifact) |

---

## หมายเหตุด้านเทคนิค

- **ไม่มี framework ฝั่ง client** — Tailwind ใช้ผ่าน CDN เฉพาะ utility layout ส่วน component ทั้งหมดอยู่ใน `public/assets/styles.css`
- **ไอคอนใช้ FontAwesome** ที่โหลดอยู่แล้ว — อย่าเพิ่ม icon library ใหม่
- **สีทั้งหมดอ้าง CSS custom property** ใน `:root` ชุดเดียว สีหลักคือ `#37CBCB` ห้าม hardcode hex ในไฟล์อื่น
- **ตัวอักษรสีขาวห้ามวางบน `--brand-500`** (contrast 1.99:1) ใช้ `--brand-700` ขึ้นไป
- `app/views/base.html` มีตัวแปรแค่ 3 ตัว: `page.title` · `page.description` · `page.nav`
- path รูป/CSS/JS ใน template เขียนแบบ relative (`assets/...`) เพราะหน้าเว็บถูก serve จาก `public/`

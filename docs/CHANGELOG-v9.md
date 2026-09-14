# CHANGELOG — รอบปรับปรุง v9

อ้างอิง `REQUIREMENTS-v9.md` · โปรเจกต์ static multi-page HTML ไม่มี build step
ทุกการแก้ทำผ่านสคริปต์ใน `gen/` ที่ **รันซ้ำได้ (idempotent)** เพื่อไม่ให้ generator รอบถัดไปทับกลับ

---

## ลำดับรัน generator

```
python gen/build_*.py            # (ถ้าจำเป็นต้อง regenerate หน้า)
python gen/fix_v9_phase1.py      # REQ-C1/C2 · REQ-M1/M3 · REQ-H1/H2
python gen/fix_v9_phase5.py      # REQ-C-DEAN2 · REQ-F1/F2
python gen/fix_v9_phase6.py      # REQ-A2 · B2 · B3 · C-DEAN1 · D2 · D3
python gen/fix_v9_phase7.py      # REQ-C3
python gen/fix_v9_partners.py    # REQ-A4
python gen/fix_v9_media_clean.py # REQ-M1/M2 (เก็บตก .news-thumb)
python gen/fix_v9_palette_37cbcb.py
python gen/fix_v9_tweaks.py
python gen/fix_v9_greenoffice.py # REQ-E1/E2
```

สคริปต์ที่รันครั้งเดียวแล้วไม่ต้องรันอีก (แก้ไฟล์รูป ไม่ใช่โค้ด):

```
python gen/fetch_bas2_media.py     # ดึงรูปจาก bas2 (ต้องมีเน็ต) — ยังไม่ได้รัน
python gen/fix_v9_detint_media.py  # ลบโทนฟ้าที่อาบมาในไฟล์ banner — รันแล้ว
```

---

## 1. ระบบสี (REQ-C1 / REQ-C2 / REQ-C3)

- ยุบ `:root` 2 ชุด (`styles.css:8` และ `:955`) เหลือชุดเดียว
- แก้บั๊ก contrast: `--brand-ink` เดิม `#06D0EB` = **1.87:1** บนพื้นขาว (ตก WCAG AA) → ชี้ไป `--brand-700` = **5.63:1**
- กวาด hex เขียวอมฟ้า hardcode ออกหมด (`#00505C` `#063C45` `#0A4650` `#123B44` `#087783` `#005A66` `#06D0EB` ฯลฯ) → เหลือ **0 จุด** นอก `:root`
- **สีหลักปัจจุบัน `#37CBCB`** (เปลี่ยนจาก `#00B3C9` ตามที่ผู้ใช้ระบุภายหลัง)

| token | ค่า | ขาวบนพื้นนี้ |
|---|---|---|
| `--brand-50 / 100 / 300 / 400` | `#EFFBFB` `#CDF3F3` `#86EAEA` `#58E4E4` | — |
| `--brand-500` **(PRIMARY)** | `#37CBCB` | 1.99:1 — ห้ามใช้เป็นพื้นตัวอักษรขาว |
| `--brand-600` | `#13939C` | 3.70:1 (non-text / ตัวใหญ่) |
| `--brand-650` | `#0F8198` | 4.55:1 |
| `--brand-700` | `#087090` | 5.63:1 |
| `--brand-800` | `#0B4E6B` | 9.07:1 |
| `--brand-900` | `#0E3A54` | 11.99:1 |

alias เดิม (`--brand` `--teal-*` `--deep-*` `--focus` `--info`) ชี้เข้าสเกลใหม่ จึงไม่ต้องไล่แก้ rule เก่า

**ต่างจากเอกสาร (ตั้งใจ):**

- 6 จุดที่เอกสารให้ map `#06D0EB → brand-500` เป็น **ตัวอักษร/ไอคอนสีขาวทับพื้นนั้น** ซึ่งได้แค่ 1.99:1 จึงส่งไป `--brand-700` แทน (`.btn-primary` `.card-tag` `.card-tag.cat` `.dean-direct` `.mega a:hover` `.drawer-sub a:hover`) และไอคอนวงกลม stat ใช้ `--brand-600`
- การ์ด Academic ใบที่ 4 ใช้ `--brand-650` แทน `--brand-600` เพราะข้อความในการ์ดเป็นตัวเล็ก (14px / 15.7px) ต้องการ ≥ 4.5:1
- สีการ์ด Academic ย้ายจาก Tailwind arbitrary value ใน `index.html` เข้า `styles.css` เป็น `.programme-card--tone-1..4` (คอมโพเนนต์ทั้งตัวอยู่ใน CSS อยู่แล้ว และ arbitrary value พึ่ง JIT ของ CDN)

ไล่เฉด 4 ระดับต่อเนื่อง: **11.99 → 9.07 → 5.63 → 4.55** ผ่าน AA ทุกใบ

## 2. รูปภาพ (REQ-M1 / M2 / M3)

- พื้นหลังกรอบรูป (`.story-media` `.card-media` `.act-media` `.split-media` `.news-thumb` `.staff-photo`) = `#EDEFF1` เทากลาง ไม่มี hue
- `.hero-media` เดิม `linear-gradient(135deg,#0A4650,#123B44)` (เขียวเข้ม) → ไล่เฉด `--brand-800` → `--brand-900`
- ปิดลายตาราง/ลายเส้นทแยงเมื่อมีรูปจริง ผ่าน `:has(> .media-img)`
- ยุบ rule ซ้ำ: `.story-media` (2 ที่) และ `.card-media` (2 ที่)
- **`.news-row .news-thumb` เก็บตกรอบสอง** — ยังเหลือ gradient ฟ้า + `::after` ลายเส้นทแยงทับรูปจริง (rule เดิม specificity สูงกว่า)

### โทนฟ้าที่ "อาบมาในไฟล์รูป" — ไม่ใช่ CSS

ตรวจพบว่าไฟล์ `banner-*.jpg` ถูกอาบสีฟ้ามาตั้งแต่ต้นฉบับ (ค่าเฉลี่ย R≈55 / G≈178 / B≈192) ยืนยันโดยเทียบกับ PNG ต้นฉบับใน `Downloads\bas` ที่ฟ้าเหมือนกัน → **CSS ลบไม่ได้**

แก้ด้วย per-channel levels stretch **11 ไฟล์** (cast 122–134 → −27…+9) สำรองต้นฉบับไว้ที่ `assets/media/_original-tinted/`

ไม่แตะ `exchange-3plus1.jpg` `poster-3plus1.jpg` `tcas69-quota.jpg` — โทนฟ้าเป็นงานออกแบบของโปสเตอร์เอง (อยู่ใน `SKIP` ของสคริปต์)

## 3. page-hero ใส่รูป banner (REQ-H1 / H2)

เพิ่ม variant `.page-hero--image` (รูป + scrim gradient + override ที่ ≤760px) แล้วแทรก `<img class="hero-bg">` ใน **11 หน้า**: about · programs · student-life · leadership · departments · news · faculty · admissions · international · honours · contact

`green-award.html` รอไฟล์ `banner-greenoffice.jpg`

## 4. กล่องทั้งใบคลิกได้ (REQ-A2 / B2 / B3 / C-DEAN1 / D2 / D3)

ใช้ stretched-link เดิมของโปรเจกต์ทั้งหมด ไม่สร้างกลไกใหม่ · ใช้ `<a href>` จริง ไม่มี `onClick` navigation

| ID | สิ่งที่แก้ |
|---|---|
| REQ-A2 | **ต้นเหตุจริง:** `.story-row .link-arrow` เป็น `position:relative` ทำให้ `::after{inset:0}` คลุมแค่ตัวลิงก์ ไม่ใช่ทั้งแถว → เปลี่ยนเป็น `position:static` + `isolation:isolate` บน `.story-row` |
| REQ-B2 | การ์ดผู้บริหาร 11/11 ใบ เพิ่ม `leader-card` + `<a class="leader-link">` |
| REQ-B3 | การ์ดภาควิชา 3 ใบ → anchor รายภาควิชา + ครอบ `card-title` ด้วย `<a>` |
| REQ-C-DEAN1 | กล่องคณบดีคลิกได้ทั้งกล่อง ปุ่ม "ดูประวัติ" / CV ยังกดแยกได้ (`z-index:2`) |
| REQ-D2 | `.story-row` 3 แถวใน student-life เพิ่ม `.link-arrow` |
| REQ-D3 | การ์ดกิจกรรม + แลกเปลี่ยน 6 ใบ `<div>` → `<a>` |

**ต่างจากเอกสาร:** anchor `#accounting-finance` `#marketing-management` `#business-administration` **มีอยู่แล้ว** ใน `departments.html` (บรรทัด 104 / 116 / 128) ไม่ต้องเพิ่ม

## 5. ย้าย "สายตรงคณบดี" (REQ-C-DEAN2 / F1 / F2)

- ย้าย section `#dean-direct` จาก `contact.html` → ท้าย `leadership.html`
- `contact.html` เหลือลิงก์ redirect 1 บรรทัด **คง `id="dean-direct"`** กัน bookmark เดิมพัง
- ปุ่มลอยหน้าแรก → `leadership.html#dean-direct`
- แก้ generator คู่กัน: `build_leadership.py` `build_contact.py` `build_home.py`

**ต่างจากเอกสาร:** เอกสารคาดว่าต้องไล่แก้ footer 20 ไฟล์ + mega menu — ตรวจจริงแล้ว **ไม่มีลิงก์ `contact.html#dean-direct` ใน footer หรือ nav เลย** มีแค่ปุ่มลอยใน `index.html` จุดเดียว

## 6. เครือข่ายพันธมิตร (REQ-A4)

- โลโก้จริง **20 องค์กร** จาก `Downloads\bas\mou` → `assets/media/partners/` ชื่อไฟล์ ASCII พร้อม `alt` ชื่อองค์กรจริงทุกตัว
- หัวข้อ section เปลี่ยนจาก "เครือข่ายด้านอาชีพและอุตสาหกรรม" → **"เครือข่ายความร่วมมือ (MOU)"** เพราะเนื้อหาจริงมีทั้งมหาวิทยาลัย โรงเรียน หน่วยงานรัฐ และบริษัทเอกชน
- ใส่โลโก้ **ชุดเดียว** ไม่ใช่ 2 ชุด เพราะ `script.js → initMarqueeClone()` โคลนให้เองอยู่แล้ว
- ใช้ `<span>` ไม่ใช่ `<a>` ครอบโลโก้ เพราะยังไม่มี URL ปลายทางของแต่ละองค์กร
- **ตัดออก 4 โลโก้** (`06` `09` `20` `22`) เพราะไฟล์ต้นฉบับความละเอียดต่ำเกินกว่าจะอ่านชื่อองค์กรออกได้แน่นอน — ไฟล์ยังอยู่ใน `Downloads\bas\mou`

## 7. Green Award (REQ-E1 / E2)

เนื้อหาจาก `bas2.swu.ac.th/greenoffice`: นิยาม Green Office · แนวทางดำเนินการ · สิ่งที่ทำได้ทันที · ชื่อเกณฑ์ 6 หมวดตามต้นฉบับ (ของเดิมเรียบเรียงใหม่ ไม่ตรงชื่อทางการ)

เจอ `<h2>Green Office</h2>` ซ้ำ 2 ที่ → เปลี่ยนอันล่างเป็น "เกณฑ์ประเมิน 6 หมวด"

**ค้าง:** hero banner + แกลเลอรี `.grid-3` — โค้ดพร้อมแล้ว เปิดอัตโนมัติเมื่อมีไฟล์รูป

## 8. อื่น ๆ

- `.programme-accent` (เส้น interact ท้ายการ์ด Academic) → `display:none` ตามที่ผู้ใช้สั่ง ไม่กระทบ hover/focus อื่น
- `index.html` มี `<h1>` สองตัว (eyebrow ถูกทำเป็น `h1`) → เปลี่ยนเป็น `<p>`

---

## ผลตรวจ (Acceptance §8)

| หัวข้อ | ผล |
|---|---|
| `:root` เหลือชุดเดียว | ✅ 1 block |
| `--brand-ink` ≥ 4.5:1 | ✅ 5.63:1 (เดิม 1.87:1) |
| hex เขียวอมฟ้านอก `:root` | ✅ 0 จุด |
| การ์ด Academic ไล่เฉด 4 ระดับ ผ่าน AA | ✅ 11.99 / 9.07 / 5.63 / 4.55 |
| `filter` / `mix-blend` / overlay ทับรูป | ✅ 0 จุด |
| `contact.html#dean-direct` เหลืออยู่ | ✅ 0 |
| `onClick` navigation ใหม่ | ✅ 0 |
| `<a>` ซ้อน `<a>` / `<a>` ไม่มี href | ✅ 0 / 0 |
| `<img>` ไม่มี `alt` | ✅ 0 |
| hash ที่ชี้ id ที่ไม่มีจริง | ✅ 0 |
| ลิงก์ไปไฟล์ที่ไม่มีในโปรเจกต์ | ✅ 0 |
| `h1` หนึ่งตัวต่อหน้า | ✅ ทุกหน้า |
| horizontal scroll @ 360 / 768 / 1440 | ✅ ไม่มี ทั้ง 26 ไฟล์ |

ตรวจ hit-area ด้วย `elementFromPoint` กลางรูปจริง: `.story-row` หน้าแรก 3/3 · ชีวิตนิสิต 3/3 · การ์ดกิจกรรม · กล่องคณบดี · การ์ดผู้บริหาร · การ์ดภาควิชา → ชี้ `<a>` ปลายทางถูกทุกจุด และปุ่ม CV ยังชี้ PDF ของตัวเอง

---

## ค้างอยู่

1. **รูปจาก bas2** — รัน `python gen/fetch_bas2_media.py` (ต้องมีเน็ต) จะได้ banner Green Office + แกลเลอรี + รูปผู้บริหาร 11 ใบ แล้ว src จะเปลี่ยนเป็น path ในเครื่องอัตโนมัติ (จบ hotlink 44 จุด) จากนั้นรัน `fix_v9_greenoffice.py` ซ้ำเพื่อเปิด hero + แกลเลอรี
2. **ชื่อองค์กรของโลโก้** `06` (ตราช้างวงกลมส้ม/เทา) · `09` (สวส.) · `20` (FLORA) · `22` (ห่วงทองสองวง)
3. **CSS ที่ตายแล้ว** — สแกนพบ 54 class ที่ไม่ถูกใช้ใน HTML/JS เลย (ชุดใหญ่คือ `.atile*` 11 ตัว ~110 บรรทัด ซึ่งเป็นการ์ด Academic รุ่นเก่า, `.card-ph`, `.prog-route*`, `.quick-*`, `.stat-*` รุ่นเก่า, hero รุ่นเก่า) ยังไม่ลบ รอตัดสินใจเรื่องโครงสร้างโปรเจกต์ก่อน

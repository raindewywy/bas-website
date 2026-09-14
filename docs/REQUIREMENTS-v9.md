# BAS SWU — Requirements Document (รอบปรับปรุง v9)

> เอกสารนี้เกิดจากการตรวจโค้ดจริงใน `C:\bas-website` (commit ล่าสุดบน `main`)
> ทุกข้อมี **หลักฐานอ้างอิงไฟล์:บรรทัด** และระบุว่าเป็น **shared fix** หรือ **page fix**
> ผู้ implement ควรทำตามลำดับใน §7 (Implementation Order)

---

## 0. สรุปสถาปัตยกรรมที่ตรวจพบ

| หัวข้อ | สิ่งที่พบ |
|---|---|
| ประเภทโปรเจกต์ | **Static multi-page HTML** (ไม่มี framework, ไม่มี build step, ไม่มี package.json) |
| หน้าเว็บ | 20 ไฟล์ `.html` ที่ root — nav/footer ถูก **inline ซ้ำในทุกไฟล์** |
| Styling | `assets/styles.css` (95 KB, ~1,960 บรรทัด) + Tailwind CDN (ใช้เฉพาะ utility layout) |
| Tokens | CSS custom properties ใน `:root` — `styles.css:8–66` และ block ที่สอง `styles.css:955–960` |
| Data | `assets/data.js` → `window.BAS_PROGRAMS`, `BAS_NEWS`, `BAS_DEPARTMENTS`, `BAS_LEADERSHIP` |
| Behaviour | `assets/script.js` (rail carousel, drawer, reveal, admin modal) |
| Generator | สคริปต์ Python ใน `gen/` เป็นตัวสร้าง/patch HTML — **ถ้าแก้ HTML ตรง ๆ ต้องอัปเดต generator ด้วย มิฉะนั้นรอบถัดไปจะทับกลับ** |
| ไอคอน | FontAwesome (ใช้อยู่แล้วทุกหน้า) — ห้ามเพิ่ม icon library ใหม่ |

### ⚠️ ข้อควรรู้ก่อนแก้ (สำคัญที่สุด)

1. **`page-hero`, `story-row`, `staff-card`, `card`, `programme-card`, `marquee-item` เป็น shared component** — แก้ที่ CSS/generator ครั้งเดียว มีผลทุกหน้า **ห้ามไล่แก้ทีละหน้า**
2. **มี token block ซ้อนกัน 2 ชุด** (`:root` บรรทัด 8 และบรรทัด ~955) ทำให้ค่าสีทับกันเอง → ข้อ REQ-C1 ให้ยุบเหลือชุดเดียว
3. ทุกหน้ามี `<section class="page-hero">` อยู่ที่บรรทัด **96** เหมือนกันหมด (faculty.html = 93) → patch ด้วย generator ได้ตรง ๆ

---

## 1. REQ-C — ระบบสี (Global / Shared)

### 1.1 ปัญหาที่ตรวจพบ

| ที่มา | ค่าปัจจุบัน | อาการ |
|---|---|---|
| `styles.css:10` `--brand` | `#06D0EB` | ฟ้าสว่างจัด |
| `styles.css:11` `--brand-ink` | `#06D0EB` | **contrast 1.87:1 บนพื้นขาว — ตก WCAG AA (ต้อง ≥ 4.5:1)** ใช้เป็นสีตัวอักษร/ไอคอนอยู่หลายจุด |
| `styles.css:12` `--brand-deep` | `#00505C` | H188 — **นี่คือ "ฟ้าเขียว" ที่ต้องการตัดออก** |
| `styles.css:957` `--deep-900` | `#00505C` | ใช้เป็นพื้น `page-hero` + `cta-band` |
| `styles.css:958` `--deep-800` | `#063C45` | เขียวอมเทาเข้ม |
| `styles.css:554` `.hero-media` | `linear-gradient(135deg,#0A4650,#123B44)` | พื้นหลังกรอบรูป = เขียวเข้ม |
| `index.html:149,173` | `bg-[#005A66]`, `bg-[#087783]` | การ์ด Academic hardcode สีเขียวอมฟ้า |

### 1.2 REQ-C1 — Palette ใหม่ (บังคับ)

ยึด **#00B3C9** (สีที่ผู้ใช้ระบุ) เป็น brand หลัก และ **#00CBEB** เป็นสีสว่าง/hover
เฉดเข้มทั้งหมดต้องเลื่อน hue ไปทาง **น้ำเงิน (H197–205)** เพื่อตัดความรู้สึก "เขียว"

แทนที่ token block ทั้ง 2 ชุดด้วยชุดเดียวนี้ใน `assets/styles.css:8`:

```css
:root{
  /* ---- Brand scale — anchored on #00B3C9 ---- */
  --brand-50 :#EAF8FB;   /* wash อ่อนสุด */
  --brand-100:#CDEEF6;   /* wash */
  --brand-300:#7CDDF0;   /* eyebrow / ไอคอนบนพื้นเข้ม — 8.9:1 บน brand-900 */
  --brand-400:#00CBEB;   /* accent สว่าง / hover / underline */
  --brand-500:#00B3C9;   /* PRIMARY — fill, rule, ไอคอนขนาดใหญ่ */
  --brand-600:#0091AD;   /* border, icon เล็ก (3.7:1 — ผ่าน AA non-text) */
  --brand-700:#00718C;   /* TEXT/LINK บนพื้นขาว (5.6:1 — ผ่าน AA) */
  --brand-800:#0A4E6B;   /* พื้นเข้มรอง (9.1:1 กับตัวอักษรขาว) */
  --brand-900:#0B3A57;   /* พื้นเข้มหลัก: page-hero, cta-band (12:1) */

  /* ---- Aliases เดิม — ให้ rule เก่าทำงานต่อโดยไม่ต้องไล่แก้ ---- */
  --brand:      var(--brand-500);
  --brand-ink:  var(--brand-700);   /* ← แก้บั๊ก contrast */
  --brand-deep: var(--brand-900);
  --brand-tint: var(--brand-50);
  --brand-tint-2:var(--brand-100);
  --teal-400:   var(--brand-500);
  --teal-600:   var(--brand-700);
  --teal-700:   var(--brand-900);
  --deep-900:   var(--brand-900);
  --deep-800:   var(--brand-800);
  --focus:      var(--brand-700);
  --info:       var(--brand-700);
}
```

**ลบ** `:root` block ที่สอง (`styles.css:955–960`) ทิ้ง — ย้ายค่าขึ้นมารวมข้างบนแล้ว

### 1.3 REQ-C2 — กวาดค่าสี hardcode ออก

ต้องไม่เหลือ hex เขียวอมฟ้าใน CSS/HTML แทนที่ตามตารางนี้:

| เดิม | ใหม่ | ที่อยู่ |
|---|---|---|
| `#00505C`, `#00525E`, `#005a66`, `#005A66` | `var(--brand-900)` | `styles.css` หลายจุด, `index.html:149` |
| `#063C45`, `#062A31`, `#0A2C32`, `#0B3B43` | `var(--brand-800)` | `styles.css` |
| `#0A4650`, `#123B44` | `linear-gradient(135deg,var(--brand-800),var(--brand-900))` | `styles.css:554` `.hero-media` |
| `#087783`, `#0E6D7B`, `#007685` | `var(--brand-700)` | `index.html:173`, `styles.css` |
| `#06d0eb`, `#06D0EB` | `var(--brand-500)` | `styles.css` (13 จุด) |
| `#7FE0EC`, `#5CC3D0`, `#43C9DA` | `var(--brand-300)` | `styles.css:1526` ฯลฯ |
| `#D7F3F7`, `#BFEFF2`, `#e8f7fa`, `#e9f8fa` | `var(--brand-50)` / `var(--brand-100)` | `styles.css` |
| `rgba(0,179,201,.42)` | `rgba(0,179,201,.42)` — คงไว้ (ตรงกับ brand-500 อยู่แล้ว) | `styles.css:974` |
| `rgba(6,38,44,.55)` | `rgba(11,58,87,.55)` | `styles.css:848,849` |
| `rgba(0,88,102,.32)` | `rgba(11,58,87,.28)` | `styles.css:1941` |

**Acceptance:** `grep -oE '#[0-9a-fA-F]{6}' assets/styles.css` ต้องไม่เหลือค่าที่มี hue 180–195 และ L < 30% นอกจากใน `:root`

### 1.4 REQ-C3 — Academic component (หน้า main ข้อ 1)

`index.html:149, 173, 197, 221` — การ์ด `.programme-card` ใช้ `bg-[#...]` แบบ arbitrary value

```
เดิม → ใหม่
bg-[#005A66]  →  bg-[var(--brand-900)]   (การรับสมัคร)
bg-[#087783]  →  bg-[var(--brand-700)]   (ปริญญาตรี)
bg-[#18242A]  →  bg-[var(--brand-800)]   (บัณฑิตศึกษา)
bg-[#53616A]  →  bg-[var(--brand-600)]   (โอกาสระดับนานาชาติ)
```

- ต้องได้ **ไล่เฉดฟ้า 4 ระดับต่อเนื่อง** ไม่ใช่ฟ้า 2 ใบ + เทา 2 ใบอย่างปัจจุบัน
- ตัวอักษรขาวบนทั้ง 4 ใบต้องผ่าน AA (brand-600 = 3.7:1 ⇒ ใช้ได้เฉพาะหัวข้อ ≥ 24px bold; ถ้าตัวเล็กให้ใช้ `--brand-700` แทน)
- `.programme-accent` (`styles.css`) ให้ใช้ `var(--brand-400)` เป็นเส้นเน้น

---

## 2. REQ-H — page-hero ใส่รูป banner (Global / Shared)

### 2.1 สถานะปัจจุบัน

`styles.css:963–989` — `.page-hero` เป็น **พื้นสีทึบ + วงกลม radial ที่มุมขวาบน** ไม่มีรูปเลย
โครงสร้าง markup เหมือนกันทุกหน้า:

```html
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow th-body">…</p>
    <h1 class="bi-heading">…</h1>
    <p class="lede th-body">…</p>
  </div>
</section>
```

### 2.2 REQ-H1 — เพิ่ม variant `page-hero--image` (แก้ CSS ครั้งเดียว)

```css
.page-hero--image{ position:relative; isolation:isolate; }
.page-hero--image > .hero-bg{
  position:absolute; inset:0; z-index:-2;
  width:100%; height:100%; object-fit:cover; object-position:center;
}
.page-hero--image::before{               /* scrim อ่านตัวอักษรได้ */
  content:""; position:absolute; inset:0; z-index:-1;
  background:linear-gradient(90deg,
    rgba(11,58,87,.92) 0%, rgba(11,58,87,.78) 45%, rgba(11,58,87,.42) 100%);
}
.page-hero--image::after{ display:none; }  /* ปิดวงกลม radial เดิม */
@media (max-width:760px){
  .page-hero--image::before{ background:rgba(11,58,87,.86); }
}
```

Markup ต่อหน้า (แทรก `<img class="hero-bg">` เป็นลูกตัวแรก):

```html
<section class="page-hero page-hero--image">
  <img class="hero-bg" src="assets/media/banner-xxx.jpg" alt="" aria-hidden="true"
       loading="eager" decoding="async">
  <div class="wrap"> … เนื้อหาเดิม ไม่ต้องแก้ … </div>
</section>
```

### 2.3 REQ-H2 — จับคู่รูปต่อหน้า

| หน้า | ไฟล์ | สถานะรูป |
|---|---|---|
| `about.html` (หน้าเกี่ยวกับคณะ ข้อ 1) | `assets/media/hero-banner.jpg` | ✅ มีแล้ว |
| `programs.html` (หลักสูตรทั้งหมด ข้อ 1) | `assets/media/banner-program.jpg` | ✅ มีแล้ว |
| `green-award.html` (Green Award ข้อ 2) | `assets/media/banner-greenoffice.jpg` | ❌ **ต้องเพิ่ม** (ดู §5) |
| `student-life.html` | `assets/media/campus-life.jpg` | ✅ มีแล้ว |
| `leadership.html` | `assets/media/banner-news.jpg` หรือ `dean/banner-news.png` | ✅ มีแล้ว |
| `departments.html` | `assets/media/banner-showcase.jpg` | ✅ มีแล้ว |
| `contact.html`, `news.html`, `faculty.html`, `admissions.html`, `international.html`, `honours.html` | (ใช้รูปที่มีให้ครบ เพื่อความสม่ำเสมอ) | ✅ |

**หมายเหตุ responsive:** `.page-hero` ปัจจุบัน padding `var(--space-7) 0 var(--space-8)` — ต้องตรวจว่าที่ 360px รูปไม่ทำให้ `h1` ล้น และ `object-position` ยังเห็นจุดสำคัญของภาพ

---

## 3. REQ-M — Component รูปภาพ: ปรับสีให้เป็น "สีปกติ" (หน้า main ข้อ 3)

### 3.1 สถานะปัจจุบัน — สิ่งที่ทำให้รูป "ติดโทนฟ้า"

| จุด | โค้ด | ผล |
|---|---|---|
| `styles.css:1558–1560` | `.story-media{background:linear-gradient(180deg,var(--surface),var(--surface-2))}` | พื้นหลังฟ้าจาง (`--surface-2:#F7FAFB`) |
| `styles.css:1562–1567` | `.story-media::after` = ตาราง grid สีฟ้า opacity .5 | ลายเส้นฟ้าซ้อนบนกรอบรูป |
| `styles.css:614` | `.card-media{background:linear-gradient(135deg,var(--paper-dim),var(--line))}` | เทาอมฟ้า |
| `styles.css:1533` | `.card-media{background:var(--surface-2)}` | ฟ้าจาง |
| `styles.css:554` | `.hero-media{background:linear-gradient(135deg,#0A4650,#123B44)}` | **เขียวเข้ม** |
| `styles.css:647` | `.story-media{background:linear-gradient(135deg,var(--paper-dim),var(--line))}` | ซ้ำซ้อนกับ 1558 |

> ลาย grid + gradient เหล่านี้ถูกออกแบบไว้สมัยยังเป็น **placeholder box** ตอนนี้มีรูปจริงแล้ว (`styles.css:1946` "v8 real images") จึงเหลือเป็นสีที่ "เลอะ" ขอบรูปและเห็นชัดตอนรูปกำลังโหลด

### 3.2 REQ-M1 — ทำให้พื้นหลังกรอบรูปเป็นกลาง

```css
/* พื้นหลังกรอบรูป = เทากลาง ไม่มี hue */
.story-media, .card-media, .act-media, .split-media, .news-thumb, .staff-photo{
  background:#EDEFF1;            /* neutral placeholder ระหว่างโหลด */
}
.hero-media{
  background:linear-gradient(135deg,var(--brand-800),var(--brand-900));
}
/* ปิดลายตารางเมื่อมีรูปจริง */
.story-media:has(> .media-img)::after,
.card-media:has(> .media-img)::after{ display:none; }
```

### 3.3 REQ-M2 — ห้ามใส่ tint/overlay ทับรูปถ่าย

- ห้ามใช้ `filter: hue-rotate/sepia/saturate`, `mix-blend-mode`, หรือ overlay สีแบรนด์ทับ `.media-img` ทุกกรณี
- ยกเว้น **scrim ดำ/น้ำเงินโปร่งใสเพื่อความอ่านออกของตัวอักษร** (page-hero, hero-full) เท่านั้น
- `.story-theme` chip (`styles.css:1554`) ให้คงพื้นทึบเดิม (`var(--ink)`) — ผ่าน contrast แล้ว

### 3.4 REQ-M3 — ตัด CSS ซ้ำ

`.story-media` ถูกประกาศ 2 ที่ (`647` และ `1558`) และ `.card-media` 2 ที่ (`614` และ `1533`)
ให้ยุบเหลือที่เดียว เพื่อไม่ให้แก้แล้วสีไม่เปลี่ยนเพราะโดน rule ทีหลังทับ

---

## 4. REQ-L — รูปแบบ "กล่องทั้งใบคลิกได้" (Global / Shared)

### 4.1 Pattern มาตรฐาน (มีอยู่แล้วในโปรเจกต์ — ใช้ซ้ำ ห้ามสร้างใหม่)

`styles.css:791–798` และ `921–929` ใช้ **stretched-link** อยู่แล้ว:

```css
.X{ position:relative; }
.X a.primary-link::after{ content:""; position:absolute; inset:0; }  /* คลุมทั้งกล่อง */
.X:focus-within{ outline:2px solid var(--focus); outline-offset:2px; }
.X a.primary-link:focus-visible{ outline:none; }
```

**กติกา:** ใช้ `<a href>` จริงเสมอ — **ห้ามใช้ `onClick` navigation** (ตามข้อกำหนดโปรเจกต์)
ปุ่ม/ลิงก์รองภายในกล่องต้องมี `position:relative; z-index:1;` เพื่อไม่ถูก overlay กิน

### 4.2 ตารางสถานะ component ที่ต้องคลิกได้

| Component | ไฟล์ | สถานะ | ต้องทำ |
|---|---|---|---|
| `.leader-card` (หน้า leadership) | `styles.css:791–798` | ✅ มี stretched-link แล้ว | — |
| `.card-linked` (การ์ดภาควิชา) | `styles.css:921–929` | ⚠️ กลไกมี แต่ **href ชี้ `departments.html` เฉย ๆ ทุกใบ** | REQ-A3 |
| `.staff-card.staff-name-a` (หน้า about) | `about.html:152` | ❌ **ไม่มีลิงก์เลย** | REQ-A2 |
| `.leader-dean` (กล่องคณบดี) | `leadership.html:103` / `styles.css:800` | ❌ ไม่มี stretched-link | REQ-B1 |
| `.story-row` (หน้า main) | `styles.css:642–646` | ✅ มี (ผ่าน `.link-arrow::after`) | — |
| `.story-row` (หน้า student-life) | `student-life.html:106–111` | ❌ **ไม่มี `.link-arrow` เลย → คลิกไม่ได้** | REQ-D2 |
| `.card` กิจกรรมนิสิต | `student-life.html:127–129` | ❌ เป็น `<div>` ไม่ใช่ลิงก์ | REQ-D3 |
| `.card` โครงการแลกเปลี่ยน | `student-life.html:160–162` | ❌ เป็น `<div>` | REQ-D3 |
| `.marquee-item` | `index.html:353` | ❌ เป็น `<span>` ข้อความ placeholder | REQ-A4 |

---

## 5. Requirements รายหน้า

### 5.1 หน้าแรก — `index.html`

| ID | ข้อกำหนด | หลักฐาน |
|---|---|---|
| **REQ-A1** | **Academic component เปลี่ยนโทนเขียว → ฟ้า** — ดู REQ-C3 | `index.html:149,173,197,221` |
| **REQ-A2** | **ชีวิตนิสิต: รูปกดแล้วลิงก์ไปหน้าถัดไป** — `.story-row` ทั้ง 3 แถวมี `.link-arrow` อยู่แล้ว (`student-life.html`, `#activities`, `#exchange`) และ CSS `.story-row .link-arrow::after{inset:0}` คลุมทั้งแถวแล้ว **แต่ `.story-media` มี `position:relative` + `z-index` ของ `.media-img` ทำให้ hit-area ทับ** → ต้องเพิ่ม `.story-row .story-media{pointer-events:none}` หรือย้าย `::after` ไปที่ `.story-row` เอง เพื่อให้ **คลิกที่ตัวรูปแล้วไปหน้าถัดไปได้จริง** และเพิ่ม `cursor:pointer` + hover ยกรูป | `index.html:293–302`, `styles.css:642–647` |
| **REQ-A3** | **Component รูปทั้งหมดที่ติดโทนฟ้า → สีปกติ** — ดู REQ-M ทั้งหมวด | `styles.css:614,647,1533,1558–1567` |
| **REQ-A4** | **เครือข่ายด้านอาชีพและอุตสาหกรรม: เอาโลโก้แทนกล่องข้อความ** — ปัจจุบันเป็น `<span class="marquee-item">องค์กรพันธมิตร 01…08</span>` (placeholder ล้วน) ต้องแทนด้วย `<a><img class="partner-logo" src="assets/media/partners/xxx.svg" alt="ชื่อองค์กร"></a>` | `index.html:352–354`, `styles.css:670–675` |

**REQ-A4 — spec ของ `.partner-logo` (เพิ่มใหม่ใน CSS):**

```css
.marquee-item{ padding:0 var(--space-4); border:0; background:none; opacity:1; }
.partner-logo{
  height:44px; width:auto; max-width:160px; object-fit:contain;
  filter:grayscale(1); opacity:.62;
  transition:filter var(--dur), opacity var(--dur);
}
.marquee-item:hover .partner-logo,
.marquee-item:focus-visible .partner-logo{ filter:none; opacity:1; }
@media (max-width:600px){ .partner-logo{ height:34px; max-width:120px; } }
```

- ต้องมี `alt` เป็นชื่อองค์กรจริงทุกโลโก้ (ห้าม `alt=""`)
- ถ้ายังไม่มีโลโก้จริง → **ห้ามใส่กล่องข้อความ placeholder** ให้ซ่อนทั้ง section ไปก่อน (`hidden`) แล้วค่อยเปิดเมื่อมีไฟล์
- ต้องทำซ้ำ track 2 ชุดเพื่อให้ marquee วนไม่มีรอยต่อ

---

### 5.2 หน้าเกี่ยวกับคณะ — `about.html`

| ID | ข้อกำหนด | หลักฐาน |
|---|---|---|
| **REQ-B1** | **page-hero ใส่รูปจาก banner** — ใช้ `assets/media/hero-banner.jpg` ตาม REQ-H1/H2 | `about.html:96` |
| **REQ-B2** | **การ์ดรูปผู้บริหารกดลิงก์ไปหน้าข้อมูลได้** — `.staff-card.staff-name-a` ปัจจุบันเป็น `<div>` ล้วน ไม่มี `<a>` เลย ต้องเพิ่ม `class="staff-card leader-card"` แล้วครอบชื่อด้วย `<a class="leader-link" href="leader-{slug}.html">` เพื่อ **reuse stretched-link ที่มีอยู่แล้ว** (`styles.css:791–798`) ไม่ต้องเขียน CSS ใหม่ | `about.html:152` |
| **REQ-B3** | **การ์ดภาควิชา คลิกได้ทั้งข้อความ "ดูภาควิชา" และทั้งกล่อง** — `.card-linked` มี stretched-link แล้ว แต่ **`href` ของทั้ง 3 ใบชี้ `departments.html` เหมือนกันหมด** ต้องแก้เป็น anchor รายภาควิชา และครอบ `card-title` ด้วย `<a>` เพื่อให้ hover cue ทำงาน | `about.html` (section ภาควิชา) |

**REQ-B2 — mapping ชื่อ → ไฟล์ (ตรวจแล้วมีครบ 11 ไฟล์):**

| ชื่อ | ไฟล์ |
|---|---|
| ดร.ณัฐินี ฐานะจาโร | `leader-natinee-thanajaro.html` |
| ผศ.ดร.จรินทร์ จารุเสน | `leader-jarin-jarusen.html` |
| ผศ.ดร.ภูธิป มีถาวรกุล | `leader-phutip-meethavornkul.html` |
| ผศ.ดร.กัลยกิตติ์ กีรติอังกูร | `leader-kanyakit-keeratiangkoon.html` |
| ผศ.ดร.เพชรรัตน์ จินต์นุพงศ์ | `leader-phetcharat-jinnupong.html` |
| ดร.รสิตา สังข์บุญนาค | `leader-rasita-sangboonnak.html` |
| ผศ.ดร.กังวาน ยอดวิศิษฎ์ศักดิ์ | `leader-kangwan-yodwisitsak.html` |
| รศ.ดร.วสันต์ สกุลกิจกาญจน์ | `leader-wasan-sakulkijkarn.html` |
| ผศ.ดร.คมกริช นันทะโรจพงศ์ | `leader-khomkrit-nantharojphong.html` |
| ดร.สยาม ประเสริฐกุล | `leader-siam-prasertkul.html` |
| ดร.จิรชัย หมื่นฤทธิ์ | `leader-jirachai-muenlit.html` |

> แนะนำเพิ่ม field `page` ลงใน `window.BAS_LEADERSHIP` (`assets/data.js:4`) แทนการ hardcode ใน HTML — เป็น single source of truth ตามข้อกำหนดโปรเจกต์

**REQ-B3 — mapping ภาควิชา (จาก `data.js:3`):**

| ภาควิชา | href ที่ต้องใช้ |
|---|---|
| ภาควิชาการบัญชีและการเงิน | `departments.html#accounting-finance` |
| ภาควิชาการตลาดและการจัดการ | `departments.html#marketing-management` |
| ภาควิชาบริหารธุรกิจ | `departments.html#business-administration` |

→ ต้องเพิ่ม `id` ที่ตรงกันใน `departments.html` (บรรทัด 109, 121, 133) ด้วย มิฉะนั้น anchor ตาย

---

### 5.3 หน้าผู้บริหารคณะ — `leadership.html`

| ID | ข้อกำหนด | หลักฐาน |
|---|---|---|
| **REQ-C-DEAN1** | **กล่องคณบดีกดลิงก์ผ่านกล่องได้เลย** — `.leader-dean` (`leadership.html:103`) ไม่มี stretched-link ต้องเพิ่ม `position:relative` (มีแล้วใน `styles.css:800` ต้องเช็ค) + ครอบชื่อ `<h3>` ด้วย `<a href="leader-natinee-thanajaro.html">` แล้วใส่ `::after{inset:0}` ปุ่ม "ดูประวัติฉบับเต็ม" / "CV" / อีเมล ที่อยู่ในกล่องต้องมี `position:relative; z-index:1` เพื่อยังกดแยกได้ | `leadership.html:103–110` |
| **REQ-C-DEAN2** | **ย้าย "สายตรงคณบดี" มาไว้หน้านี้** — ปัจจุบัน section `#dean-direct` อยู่ที่ `contact.html` ต้องย้ายทั้ง block มาต่อท้าย `leadership.html` โดยคง `id="dean-direct"` เดิม | `contact.html` (section `#dean-direct`) |

**REQ-C-DEAN2 — งานที่ต้องตามแก้พร้อมกัน (ไม่งั้นลิงก์ตาย):**

| จุด | เดิม | ใหม่ |
|---|---|---|
| ปุ่มลอย `.dean-direct` | `index.html:360` → `href="contact.html#dean-direct"` | `href="leadership.html#dean-direct"` |
| Footer ทุกหน้า (20 ไฟล์) | ลิงก์ที่ชี้ `contact.html#dean-direct` | เปลี่ยนเป็น `leadership.html#dean-direct` |
| Mega menu / drawer | รายการ "สายตรงคณบดี" ใต้ "ติดต่อ" | ย้ายไปใต้ "เกี่ยวกับคณะ → ผู้บริหาร" |
| `contact.html` | ลบ section `#dean-direct` | เหลือลิงก์ข้อความสั้น 1 บรรทัดชี้ไป `leadership.html#dean-direct` (กัน bookmark เดิมพัง) |

> ⚠️ `gen/build_contact.py` และ `gen/build_leadership.py` ต้องแก้คู่กัน มิฉะนั้น generate รอบหน้าจะย้อนกลับ

---

### 5.4 หน้า Green Award — `green-award.html`

**สถานะปัจจุบัน: หน้านี้แทบว่าง** — มีแค่ `page-hero` + หัวข้อ + ย่อหน้าเดียว + ลิงก์ออกนอกเว็บ (`green-award.html:96–102`)

| ID | ข้อกำหนด |
|---|---|
| **REQ-E1** | **page-hero ใส่รูปจาก banner** — ใช้ `GreenOffice1600x6003.jpg` จาก bas2 (ดู §6) บันทึกเป็น `assets/media/banner-greenoffice.jpg` |
| **REQ-E2** | **ใส่เนื้อหา Green Office ฉบับเต็มจาก `bas2.swu.ac.th/greenoffice`** พร้อมรูป |

**REQ-E2 — โครงเนื้อหาที่ต้องมี (ดึงจาก bas2 แล้ว):**

1. **นิยาม Green Office** — "สำนักงานและกิจกรรมต่าง ๆ ที่ส่งผลกระทบต่อสิ่งแวดล้อมน้อยที่สุด" ผ่านการจัดการทรัพยากรและพลังงานอย่างรู้คุณค่า และการจัดการของเสียอย่างมีประสิทธิภาพ
2. **แนวทางดำเนินการ** — ตั้งแต่ขั้นออกแบบ/ก่อสร้าง → การเลือกอุปกรณ์ที่ประหยัดพลังงานและเป็นมิตรต่อสิ่งแวดล้อม → พฤติกรรมของบุคลากร
3. **สิ่งที่ทำได้ทันที** — ปิดไฟเมื่อเลิกใช้ / สร้างนิสัยปิดอุปกรณ์ / จัดซื้อวัสดุสำนักงานที่เป็นมิตรต่อสิ่งแวดล้อม
4. **เกณฑ์ประเมิน 6 หมวด** — แสดงเป็น `grid-3` การ์ด 6 ใบ (reuse `.card` เดิม ห้ามสร้าง component ใหม่):

   | หมวด | ชื่อ |
   |---|---|
   | 1 | นโยบายและการวางแผนพัฒนาอย่างต่อเนื่อง |
   | 2 | การสื่อสารและสร้างจิตสำนึก |
   | 3 | การใช้ทรัพยากรและพลังงาน |
   | 4 | การจัดการของเสีย |
   | 5 | สภาพแวดล้อมและความปลอดภัย |
   | 6 | การจัดซื้อจัดจ้างที่เป็นมิตรกับสิ่งแวดล้อม |

5. **แกลเลอรีรูปกิจกรรม** — reuse `.grid-3` + `.card-media` (ตาม REQ-M ต้องไม่มี tint ฟ้า)
6. คงลิงก์ external เดิมไว้ท้ายหน้า

**รูปที่ต้องดาวน์โหลดจาก bas2 (§6)** — ห้าม hotlink; ให้ save ลง `assets/media/`

---

### 5.5 หน้าติดต่อคณะ — `contact.html`

| ID | ข้อกำหนด |
|---|---|
| **REQ-F1** | **ย้าย "สายตรงคณบดี" ออกไปหน้าผู้บริหารคณะ** — ดู REQ-C-DEAN2 |
| **REQ-F2** | เหลือลิงก์ redirect 1 บรรทัดในหมวดติดต่อ: "ต้องการติดต่อคณบดีโดยตรง → สายตรงคณบดี" ชี้ `leadership.html#dean-direct` |
| **REQ-F3** | ตรวจว่า `advisor-card` (ที่ปรึกษาแต่ละฝ่าย) และ Google Maps ยังทำงานปกติหลังย้าย section |

---

### 5.6 หน้าหลักสูตรทั้งหมด — `programs.html`

| ID | ข้อกำหนด |
|---|---|
| **REQ-G1** | **page-hero ใส่รูปจาก banner** — `assets/media/banner-program.jpg` ตาม REQ-H1/H2 |
| **REQ-G2** | ตรวจว่า filter `?level=undergraduate` / `?level=graduate` และ `#graduate-entry` ยังทำงานหลังแก้ hero |

---

### 5.7 หน้าชีวิตนิสิต — `student-life.html`

| ID | ข้อกำหนด | หลักฐาน |
|---|---|---|
| **REQ-D1** | **ปรับโทนสีให้กลมกลืน** — หน้านี้ใช้ `.story-media` + `.card-media` ที่มีลายตารางฟ้า และ `.page-hero` เขียวเข้ม → หลัง REQ-C + REQ-M จะหายไปเอง แต่ต้องตรวจเพิ่ม: `.facility-item`, `.story-theme` chip, และพื้น `var(--paper-dim)` สลับ section ให้เป็นจังหวะเดียวกับหน้าอื่น | `student-life.html:96–165` |
| **REQ-D2** | **Component รูปลิงก์ได้** — `.story-row` 3 แถว (บรรทัด 106–111) **ไม่มีลิงก์เลย** ต้องเพิ่ม `.link-arrow` ในแต่ละ `.story-copy` แล้วอาศัย stretched-link เดิม | `student-life.html:106–111` |
| **REQ-D3** | **กิจกรรมนิสิต กด link จาก component** — การ์ด 3 ใบใน `#activities` (บรรทัด 127–129) เป็น `<div class="card">` ต้องเปลี่ยนเป็น `<a class="card" href="…">` ทั้งใบ | `student-life.html:127–129` |

**REQ-D2 — ปลายทางที่แนะนำ:**

| แถว | หัวข้อ | href |
|---|---|---|
| 1 | การแข่งขันเคสและโปรเจกต์ประยุกต์ | `student-life.html#activities` |
| 2 | ชมรมและสโมสรนิสิต | `student-life.html#activities` |
| 3 | ชีวิตในและรอบแคมปัส | `student-life.html#facilities` |

**REQ-D3 — ปลายทางที่แนะนำ:**

| การ์ด | href |
|---|---|
| ปฐมนิเทศและสัปดาห์ต้อนรับ | `news.html?cat=campus` |
| การแข่งขันเคสธุรกิจ | `news.html?cat=academic` |
| งานชมรมและสมัครสมาชิก | `news.html?cat=campus` |

> การ์ด "โครงการแลกเปลี่ยน" (บรรทัด 160–162) ก็เป็น `<div>` เช่นกัน — แนะนำลิงก์ไป `international.html` เพื่อความสม่ำเสมอ

---

## 6. Assets ที่ต้องเตรียมเพิ่ม

| ไฟล์ปลายทาง | ที่มา | ใช้ที่ |
|---|---|---|
| `assets/media/banner-greenoffice.jpg` | `bas2.swu.ac.th/Portals/64/BlockBuilderImages/23855/GreenOffice1600x6003.jpg` | REQ-E1 |
| `assets/media/greenoffice-logo.png` | `…/23856/logo-150x150.png` | REQ-E2 |
| `assets/media/greenoffice-01.jpg` … `-06.jpg` | `…/23856/02-9.jpg`, `…/25323/หมวด2-1.jpg`, `…/24195/Picture2-removebg-preview{1,2,3}.png` | REQ-E2 แกลเลอรี |
| `assets/media/partners/*.svg|png` | **ยังไม่มี — ต้องขอจากคณะ** | REQ-A4 |
| `assets/media/banner-about.jpg` | `Downloads\bas\banner_basswu-s01.jpg` หรือใช้ `hero-banner.jpg` เดิม | REQ-B1 |

**ข้อกำหนดไฟล์รูป:**
- แปลงเป็น `.jpg` คุณภาพ ~78, กว้างสูงสุด 1600px, ขนาดไม่เกิน ~250 KB/ไฟล์ (ให้สอดคล้องกับ `assets/media/` เดิมที่อยู่ในช่วง 26–240 KB)
- ตั้งชื่อไฟล์เป็น ASCII ตัวพิมพ์เล็กเท่านั้น (`หมวด2-1.jpg` ต้องเปลี่ยนชื่อ)
- ห้าม hotlink รูปจาก `bas2.swu.ac.th` ในหน้าใหม่ (หน้าเดิมยัง hotlink รูปผู้บริหารอยู่ — เป็นหนี้เทคนิคที่ควรเก็บกวาดรอบถัดไป)

---

## 7. Implementation Order (ทำตามลำดับนี้)

1. **REQ-C1 / C2** — ยุบ token 2 ชุดเป็นชุดเดียว + กวาด hex hardcode → มีผลทุกหน้าทันที
2. **REQ-M1–M3** — ทำพื้นหลังกรอบรูปเป็นกลาง + ตัด CSS ซ้ำ
3. **REQ-H1** — เพิ่ม `.page-hero--image` ใน CSS (ครั้งเดียว)
4. **REQ-H2** — แทรก `<img class="hero-bg">` ทีละหน้า (patch ผ่าน `gen/`)
5. **REQ-C-DEAN2 / F1 / F2** — ย้าย `#dean-direct` + แก้ลิงก์ทั้งไซต์ (nav, footer, ปุ่มลอย)
6. **REQ-B2 / B3 / C-DEAN1 / D2 / D3 / A2** — งาน clickable component ทั้งหมด
7. **REQ-C3 / A4** — Academic tiles + partner logos
8. **REQ-E1 / E2** — เติมเนื้อหา Green Award
9. อัปเดตสคริปต์ใน `gen/` ให้ตรงกับ HTML ที่แก้
10. Validate (§8)

---

## 8. Acceptance Criteria / Validation

### 8.1 สี
- [ ] `:root` มีชุดเดียวใน `styles.css` — ไม่มี block ซ้ำที่บรรทัด ~955
- [ ] `--brand-ink` = `#00718C` → contrast บนพื้นขาว **≥ 4.5:1** (ปัจจุบัน 1.87:1 ตก AA)
- [ ] ไม่เหลือ hex เขียวอมฟ้า (`#00505C`, `#063C45`, `#0A4650`, `#123B44`, `#087783`, `#005A66`) นอก `:root`
- [ ] การ์ด Academic 4 ใบ = ไล่เฉดฟ้าต่อเนื่อง ตัวอักษรขาวผ่าน AA ทุกใบ

### 8.2 รูปภาพ
- [ ] ทุกหน้าที่ระบุใน REQ-H2 มีรูป banner ใน hero และตัวอักษรอ่านออกบนรูป (scrim ≥ 4.5:1)
- [ ] ไม่มี `filter` / `mix-blend-mode` / overlay สีแบรนด์ทับรูปถ่ายใด ๆ
- [ ] พื้นหลังกรอบรูประหว่างโหลด = เทากลาง ไม่มี hue

### 8.3 ลิงก์
- [ ] คลิกที่ **รูป** ของ `.story-row`, `.staff-card`, `.card-linked`, `.leader-dean`, การ์ดกิจกรรม → ไปหน้าปลายทางได้จริง
- [ ] ทุกกล่องที่คลิกได้ใช้ `<a href>` — ไม่มี `onClick` navigation ใหม่
- [ ] Tab ไปถึงทุกกล่องได้ และมี focus ring มองเห็นชัด (`:focus-within`)
- [ ] ปุ่มรองในกล่อง (CV, อีเมล, "ดูประวัติ") ยังกดแยกได้ ไม่ถูก overlay กิน
- [ ] ไม่เหลือลิงก์ที่ชี้ `contact.html#dean-direct` ในไฟล์ใด (`grep -rn "contact.html#dean-direct" *.html` = 0)
- [ ] anchor `#accounting-finance`, `#marketing-management`, `#business-administration` มีอยู่จริงใน `departments.html`

### 8.4 Responsive (ทดสอบ 360 / 768 / 1024 / 1440 / 1920)
- [ ] ไม่มี horizontal scroll ทุก breakpoint
- [ ] `page-hero` + รูป: `h1` ไม่ล้น ไม่โดนครอบตัด
- [ ] marquee โลโก้: สูง 34px บนมือถือ ไม่ล้นกรอบ
- [ ] การ์ด Academic: 1 → 2 → 4 คอลัมน์ ตาม `sm:grid-cols-2 lg:grid-cols-4` เดิม

### 8.5 อื่น ๆ
- [ ] `gen/*.py` แก้ให้ตรงกับ HTML แล้ว — รัน generator ซ้ำแล้วผลลัพธ์ไม่ย้อนกลับ
- [ ] `assets/data.js` ยังเป็น single source of truth (ไม่ duplicate ข้อมูลผู้บริหาร/ภาควิชาลง HTML)

---

## 9. ประเด็นที่ต้องยืนยันก่อนลงมือ

| # | ประเด็น | ทางเลือก |
|---|---|---|
| 1 | **#00B3C9 มี hue 187° — ทางเทคนิคคือ "ฟ้าอมเขียว" (cyan)** เอกสารนี้จึงตีความว่า *ต้องการให้เฉดเข้มเลื่อนไปทางน้ำเงิน (H197–205)* ส่วน accent สว่างคงเป็น cyan ตามที่ระบุ | ยืนยัน / หรือให้เลื่อน accent ไปทางน้ำเงินด้วย (เช่น `#0090D4`) |
| 2 | **โลโก้พันธมิตร (REQ-A4)** ยังไม่มีไฟล์จริงในโปรเจกต์ | ส่งไฟล์โลโก้มา / หรือซ่อน section ไปก่อน |
| 3 | **รูปผู้บริหาร hotlink จาก bas2.swu.ac.th** | เก็บกวาดในรอบนี้ / หรือเลื่อนไปรอบถัดไป |
| 4 | **การ์ดกิจกรรมนิสิต** ยังไม่มีหน้ารายละเอียดของตัวเอง | ลิงก์ไป `news.html?cat=…` ตามที่เสนอ / หรือสร้างหน้าใหม่ |
| 5 | `contact.html` หลังย้าย "สายตรงคณบดี" ออก | เหลือลิงก์ redirect / หรือลบทิ้งเลย |

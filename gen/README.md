# gen/ — สคริปต์เตรียมรูป Green Office

เหลือ 3 สคริปต์ที่ **ยังไม่ได้รัน** ใช้เป็นชุดเดียวกันตามลำดับนี้ — ทำงานกับ `public/` โดยตรง
(ไม่มี template/build step แยกแล้ว — `public/*.html` คือไฟล์ live ตัวเดียว)

| ลำดับ | ไฟล์ | ทำอะไร |
|---|---|---|
| 1 | `fetch_bas2_media.py` | ดึงรูปจาก bas2.swu.ac.th (banner Green Office · แกลเลอรี · รูปผู้บริหาร 11 ใบ) ลง `public/assets/media/` แล้วแก้ `src` ใน `public/*.html` ให้ชี้ path ในเครื่อง |
| 2 | `fix_v9_detint_media.py` | ลบโทนฟ้าที่อาบมาในไฟล์ `banner-*.jpg` (สำรองต้นฉบับไว้ที่ `public/assets/media/_original-tinted/`) |
| 3 | `fix_v9_greenoffice.py` | เปิด hero + แกลเลอรี Green Office ใน `public/green-award.html` อัตโนมัติเมื่อมีไฟล์รูปครบ |

```bash
pip install -r ../requirements.txt   # requests + pillow (ใช้แค่ตอนดึงรูป)
python gen/fetch_bas2_media.py
python gen/fix_v9_detint_media.py
python gen/fix_v9_greenoffice.py
```

ทุกตัว idempotent — รันซ้ำไม่ทำอะไรเพิ่ม แก้ `public/*.html` ตรง ๆ เลย ไม่ต้องรันอะไรต่อ

---

## สคริปต์ที่ลบไปแล้ว

เดิมโฟลเดอร์นี้มี 40 สคริปต์ ส่วนใหญ่เป็น generator รอบเก่าที่ **patch ไฟล์ `.html` โดยตรง**
ทุกตัวรันไปแล้วและผลลัพธ์อยู่ใน `public/*.html` เรียบร้อย จึงลบออก 37 ตัว (ดูย้อนหลังได้จาก git history)

ที่ลบไปรวมถึง `build_v10_pages.py` (สร้าง 7 หน้า v10) และ `fix_v11_cyan_surfaces.py`
(ปรับสี `#37CBCB`) — ทั้งสองรันไปแล้วและผลอยู่ใน `public/*.html` กับ `public/assets/styles.css` แล้ว

## ประวัติ: จาก flat HTML → Jinja2 template → JS include (ปัจจุบัน)

**รอบแรก** ทุกการแก้ไขคือ "เขียนสคริปต์ patch HTML ทีละไฟล์" ซึ่งทำให้ nav/footer
ถูก copy ซ้ำใน 26 ไฟล์ — แก้ที่เดียวไม่พอ และไฟล์ค้างเวอร์ชันต่างกัน (ดู `docs/REQUIREMENTS-v9.md`)

**รอบสอง** ย้ายไปใช้ Jinja2 template (`app/views/` + `build.py`) — nav/footer อยู่ที่เดียว
แก้ครั้งเดียวมีผลทุกหน้า แต่ต้องรัน `python build.py` ทุกครั้งที่แก้ และ Live Server
เปิด template ตรง ๆ ไม่ได้ (ต้องเปิดที่ `public/` ที่ build ออกมา)

**ตอนนี้** nav/footer แยกเป็น `public/partials/nav.html` + `public/partials/footer.html`
ให้ `public/assets/include.js` โหลดมาแทรกตอนเปิดหน้า (ดู root README.md) — ไม่มี build step
เลย `public/*.html` เป็นไฟล์ live ตัวเดียว เปิดตรง ๆ ด้วย Live Server ได้ทันที

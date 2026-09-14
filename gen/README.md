# gen/ — สคริปต์เตรียมรูป Green Office

เหลือ 3 สคริปต์ที่ **ยังไม่ได้รัน** ใช้เป็นชุดเดียวกันตามลำดับนี้

| ลำดับ | ไฟล์ | ทำอะไร |
|---|---|---|
| 1 | `fetch_bas2_media.py` | ดึงรูปจาก bas2.swu.ac.th (banner Green Office · แกลเลอรี · รูปผู้บริหาร 11 ใบ) ลง `public/assets/media/` แล้วแก้ `src` ใน `app/views/pages/` ให้ชี้ path ในเครื่อง |
| 2 | `fix_v9_detint_media.py` | ลบโทนฟ้าที่อาบมาในไฟล์ `banner-*.jpg` (สำรองต้นฉบับไว้ที่ `public/assets/media/_original-tinted/`) |
| 3 | `fix_v9_greenoffice.py` | เปิด hero + แกลเลอรี Green Office ใน `green-award.html` อัตโนมัติเมื่อมีไฟล์รูปครบ |

```bash
python gen/fetch_bas2_media.py
python gen/fix_v9_detint_media.py
python gen/fix_v9_greenoffice.py
python build.py            # <- ต้องรันปิดท้ายเสมอ เพื่อสร้าง public/*.html ใหม่
```

ทุกตัว idempotent — รันซ้ำไม่ทำอะไรเพิ่ม

---

## สคริปต์ที่ลบไปแล้ว

เดิมโฟลเดอร์นี้มี 40 สคริปต์ ส่วนใหญ่เป็น generator รอบเก่าที่ **patch ไฟล์ `.html` โดยตรง**
ซึ่งตอนนี้ `build.py` เขียนทับหมดแล้ว ผลลัพธ์ของทุกตัวถูกรวมเข้า `app/views/` เรียบร้อย
จึงลบออก 37 ตัว (ยังดูย้อนหลังได้จาก git history)

ที่ลบไปรวมถึง `build_v10_pages.py` (สร้าง 7 หน้า v10) และ `fix_v11_cyan_surfaces.py`
(ปรับสี `#37CBCB`) — ทั้งสองรันไปแล้วและผลอยู่ใน `app/views/` กับ `public/assets/styles.css` แล้ว

## ทำไมถึงเลิกใช้วิธี patch HTML

เดิมทุกรอบปรับปรุงคือ "เขียนสคริปต์ patch HTML ทีละไฟล์" ซึ่งทำให้เกิดปัญหาสองข้อ

1. รอบถัดไป generator ทับงานรอบก่อน (ข้อควรรู้ข้อ 1 ใน `docs/REQUIREMENTS-v9.md`)
2. nav/footer ถูก copy ซ้ำใน 26 ไฟล์ — แก้ที่เดียวไม่พอ และไฟล์ค้างเวอร์ชันต่างกัน
   (ตรวจตอนย้ายมาเป็น template เจอว่า `faculty.html` กับ `index.html` มี modal เข้าสู่ระบบคนละเวอร์ชันกับอีก 24 หน้า)

ตอนนี้ nav/footer/head อยู่ที่ `app/views/base.html` ที่เดียว แก้ครั้งเดียวมีผลทุกหน้า

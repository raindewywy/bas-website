# gen/ — สคริปต์ช่วยงาน

ตั้งแต่ย้ายมาใช้ `templates/` + `build.py` แล้ว **แหล่งความจริงของ HTML คือ template**
สคริปต์ในโฟลเดอร์นี้แบ่งเป็น 3 กลุ่ม

---

## ✅ ยังใช้ได้ — ทำงานกับไฟล์รูป ไม่ใช่ HTML

| ไฟล์ | ทำอะไร |
|---|---|
| `fetch_bas2_media.py` | ดึงรูปจาก bas2.swu.ac.th (banner Green Office · แกลเลอรี · รูปผู้บริหาร 11 ใบ) ลง `assets/media/` แล้วแก้ `src` ใน `templates/pages/` ให้ชี้ path ในเครื่อง — **ยังไม่ได้รัน** |
| `fix_v9_detint_media.py` | ลบโทนฟ้าที่อาบมาในไฟล์ `banner-*.jpg` (สำรองต้นฉบับไว้ที่ `assets/media/_original-tinted/`) — รันไปแล้ว 11 ไฟล์ |

## ⏳ ยังใช้ได้ — patch template โดยตรง (ไม่ใช่ `.html` ที่ root)

| ไฟล์ | ทำอะไร |
|---|---|
| `fix_v9_greenoffice.py` | เปิด hero + แกลเลอรี Green Office **อัตโนมัติเมื่อมีไฟล์รูป** — ต้องรัน `fetch_bas2_media.py` ก่อน แล้วรัน `build.py` ตาม |
| `fix_v9_tweaks.py` | ปรับย่อยที่ทำไปแล้ว (idempotent — รันซ้ำไม่ทำอะไร) |

หลังรันสคริปต์กลุ่มนี้ **ต้องรัน `python build.py`** เพื่อสร้าง `.html` ใหม่

## 🗄️ เลิกใช้แล้ว — เก็บไว้อ้างอิงประวัติเท่านั้น

สคริปต์เหล่านี้ **patch ไฟล์ `.html` ที่ root** ซึ่งตอนนี้ถูก `build.py` เขียนทับ
ผลลัพธ์ของทุกตัวถูกรวมเข้า `templates/` เรียบร้อยแล้ว — **อย่ารันอีก**

```
build_about_pages.py   build_contact.py   build_home.py   build_leadership.py
build_news.py          build_programs.py  common.py       data_leaders.py
patch_site.py          patch_nav2.py      patch_nav3_ia.py
patch_sections_v3.py   patch_interactive_v4.py            patch_systems_v5.py
patch_typeface.py      patch_uiux_v6.py   audit_fixes_v7.py
add_images.py          add_images2.py     brighten_palette.py
fix_academic_tiles.py  fix_faculty_names.py                fix_identity_framework.py
fix_round3.py          remove_admin_demo.py                remove_podcast.py
restore_admin_login.py qa.py
fix_v9_phase1.py       fix_v9_phase5.py   fix_v9_phase6.py fix_v9_phase7.py
fix_v9_partners.py     fix_v9_media_clean.py               fix_v9_palette_37cbcb.py
```

ลบทิ้งได้เลยถ้าไม่ต้องการเก็บประวัติ — ไม่มีอะไรใน build pipeline อ้างถึงอีกแล้ว

---

## ทำไมถึงเลิกใช้

เดิมทุกรอบปรับปรุงคือ "เขียนสคริปต์ patch HTML ทีละไฟล์" ซึ่งทำให้เกิดปัญหาสองข้อ

1. รอบถัดไป generator ทับงานรอบก่อน (ข้อควรรู้ข้อ 1 ใน `REQUIREMENTS-v9.md`)
2. nav/footer ถูก copy ซ้ำใน 26 ไฟล์ — แก้ที่เดียวไม่พอ และไฟล์ค้างเวอร์ชันต่างกัน
   (ตรวจตอนย้ายมาเป็น template เจอว่า `faculty.html` กับ `index.html` มี modal เข้าสู่ระบบคนละเวอร์ชันกับอีก 24 หน้า)

ตอนนี้ nav/footer/head อยู่ที่ `templates/base.html` ที่เดียว แก้ครั้งเดียวมีผลทุกหน้า

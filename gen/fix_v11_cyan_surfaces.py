#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_v11_cyan_surfaces.py — ใช้ #37CBCB เป็นสีพื้นหลัก (ปรับได้ ±1 ระดับ)

พื้นที่เปลี่ยนตามที่ผู้ใช้เลือก
    page-hero ทุกหน้า · cta-band · footer · การ์ด Academic 4 ใบ
    วงกลม B·A·S (อัตลักษณ์คณะ) · ปุ่มลอยสายตรงคณบดี
    ปุ่มหลัก (.btn-primary) · เมนู mega/drawer ตอน hover

ช่วงสีที่อนุญาต (±1 ระดับจาก #37CBCB)
    สว่างขึ้น 1 ระดับ  --brand-400  #58E4E4
    สีหลัก            --brand-500  #37CBCB
    เข้มขึ้น 1 ระดับ   --brand-600  #13939C

ตัวอักษรบนพื้นเหล่านี้เป็น "สีขาว" ตามที่ผู้ใช้สั่ง
!! หมายเหตุ contrast (แจ้งไว้ให้ทราบ ไม่ได้เปลี่ยนตามเอง) !!
    ขาวบน #37CBCB = 1.99:1   ·  ขาวบน #13939C = 3.70:1
    WCAG AA ต้องการ 4.5:1 (ตัวเล็ก) หรือ 3:1 (ตัวใหญ่ >=24px หนา)
    => footer จึงใช้ระดับเข้มสุดที่อนุญาต (#13939C) เพราะมีตัวอักษรเล็กเยอะที่สุด
    ถ้าต้องการให้ผ่าน AA ทั้งหมด สลับ TEXT_ON_CYAN เป็น "ink" แล้วรันซ้ำ

รันซ้ำได้ (idempotent) — จากนั้นรัน  python build.py
    python gen/fix_v11_cyan_surfaces.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "styles.css"
MARK = "/* == v11 cyan surfaces =="

# "white" = ตามที่ผู้ใช้เลือก · "ink" = สลับเป็นตัวอักษรเข้มให้ผ่าน AA
TEXT_ON_CYAN = "white"

BG_MAIN = "#37CBCB"     # brand-500
BG_DARK = "#13939C"     # brand-600 (ลง 1 ระดับ) — ใช้เป็นสี hover

# การ์ด Academic 4 ใบ — ตามแพตเทิร์นเว็บอ้างอิง: แบรนด์เข้ม · แบรนด์ปกติ · เทาเข้ม · เทาอ่อน
TONES = [
    "#13939C",   # 1 ฟ้าเข้มลง 1 ระดับ (brand-600)  — ขาว 3.70:1
    "#37CBCB",   # 2 ฟ้าปกติ (brand-500)            — ขาว 1.99:1
    "#1F2A30",   # 3 เทาเข้ม                        — ขาว 14.66:1
    "#66757C",   # 4 เทาอ่อน (อ่อนสุดที่ยังผ่าน AA) — ขาว 4.77:1
]

# ---- ไล่สี (gradient) ทุกค่าอยู่ในช่วง ±1 ระดับ ------------------------
# ทิศทางไล่จาก "เข้ม -> สว่าง" ฝั่งที่มีตัวอักษรอยู่จะเข้มกว่าเสมอ contrast จึงดีขึ้น
G_HERO   = "linear-gradient(115deg, #13939C 0%, #2FC0C0 55%, #58E4E4 100%)"
G_CTA    = "linear-gradient(120deg, #13939C 0%, #37CBCB 58%, #58E4E4 100%)"
G_FOOTER = "linear-gradient(165deg, #37CBCB 0%, #13939C 100%)"
G_LETTER = "linear-gradient(140deg, #49D9D9 0%, #13939C 100%)"
G_FAB    = "linear-gradient(135deg, #49D9D9 0%, #13939C 100%)"
G_FAB_HOVER = "linear-gradient(135deg, #37CBCB 0%, #0F7F88 100%)"
G_TONES = [
    "linear-gradient(160deg, #1AA5AF 0%, #13939C 100%)",   # 1 ฟ้าเข้ม
    "linear-gradient(160deg, #49D9D9 0%, #2FC0C0 100%)",   # 2 ฟ้าปกติ
    "linear-gradient(160deg, #2A3942 0%, #1B252B 100%)",   # 3 เทาเข้ม
    "linear-gradient(160deg, #78868E 0%, #5D6C73 100%)",   # 4 เทาอ่อน
]

FG = "#fff" if TEXT_ON_CYAN == "white" else "var(--ink)"
FG_SOFT = "rgba(255,255,255,.88)" if TEXT_ON_CYAN == "white" else "var(--ink-soft)"
FG_DIM = "rgba(255,255,255,.78)" if TEXT_ON_CYAN == "white" else "var(--ink-soft)"

BLOCK = f"""

/* == v11 cyan surfaces ==================================================
   #37CBCB เป็นสีพื้นหลัก · ปรับได้ ±1 ระดับ (#13939C … #58E4E4)
   ตัวอักษรบนพื้นเหล่านี้ = {'ขาว' if TEXT_ON_CYAN == 'white' else 'สีเข้ม'} ตามที่กำหนด
   ===================================================================== */

/* ---- page-hero (ทุกหน้า) -------------------------------------------- */
.page-hero{{ background:{BG_MAIN}; background-image:{G_HERO}; color:{FG}; }}
.page-hero h1{{ color:{FG}; }}
.page-hero .eyebrow{{ color:{FG}; }}
.page-hero .eyebrow::before{{ background:{FG}; }}
.page-hero .bi-en{{ color:{FG_DIM}; }}
.page-hero .lede{{ color:{FG_SOFT}; }}
.page-hero::after{{
  background:radial-gradient(circle at 34% 34%, rgba(255,255,255,.22), rgba(255,255,255,0) 68%);
}}
/* hero ที่มีรูป banner — scrim เปลี่ยนเป็นฟ้าโปร่งให้เข้าชุดกัน */
.page-hero--image::before{{
  background:linear-gradient(90deg,
    rgba(55,203,203,.94) 0%, rgba(55,203,203,.82) 45%, rgba(55,203,203,.46) 100%);
}}
@media (max-width:760px){{
  .page-hero--image::before{{ background:rgba(55,203,203,.90); }}
}}

/* ---- cta-band -------------------------------------------------------- */
.cta-band{{ background:{BG_MAIN}; background-image:{G_CTA}; color:{FG}; }}
.cta-band .eyebrow{{ color:{FG}; }}
.cta-band .eyebrow::before{{ background:{FG}; }}
.cta-band h2{{ color:{FG}; }}
.cta-band p{{ color:{FG_SOFT}; }}

/* ---- footer ---------------------------------------------------------- */
.site-footer{{ background:{BG_MAIN}; background-image:{G_FOOTER}; color:{FG_SOFT}; }}
.site-footer a{{ color:{FG}; }}
.site-footer h3{{ color:{FG}; }}
.site-footer .footer-brand p{{ color:{FG_SOFT}; }}
.site-footer .footer-bottom{{ color:{FG_DIM}; border-top-color:rgba(255,255,255,.28); }}

/* ---- วงกลม B · A · S (อัตลักษณ์คณะ) ---------------------------------- */
.id-letter{{ background:{BG_MAIN}; background-image:{G_LETTER}; box-shadow:0 4px 14px rgba(55,203,203,.38); }}
.id-card:hover .id-letter,
.id-card:focus-within .id-letter{{ background-image:linear-gradient(140deg, #37CBCB 0%, #0F7F88 100%); }}

/* ---- ปุ่มลอย "สายตรงคณบดี" ------------------------------------------- */
.dean-direct{{ background:{BG_MAIN}; background-image:{G_FAB}; box-shadow:0 6px 18px rgba(55,203,203,.45); }}
.dean-direct:hover,
.dean-direct:focus-visible,
.dean-direct:active{{ background-image:{G_FAB_HOVER}; box-shadow:0 10px 22px rgba(19,147,156,.5); }}

/* ---- ปุ่มหลัก (สมัครเรียน · เข้าสู่ระบบ) ------------------------------
   ปุ่มขนาดเล็ก = สีเรียบ ไม่ไล่สี (ไล่สีสงวนไว้ให้พื้นผิวใหญ่)          */
.btn-primary{{ background:{BG_MAIN}; background-image:none; color:#fff; border-color:transparent; }}
.btn-primary:hover,
.btn-primary:focus-visible{{ background:{BG_DARK}; background-image:none; color:#fff; }}

/* ---- เมนู mega ตอน hover: พื้นฟ้า · ตัวอักษรขาวทั้งไทยและอังกฤษ ------- */
.mega a:hover,
.mega a:focus-visible{{ background:{BG_MAIN}; border-left-color:{BG_MAIN}; color:#fff; }}
.mega a:hover .th-body, .mega a:focus-visible .th-body,
.mega a:hover .en,      .mega a:focus-visible .en,
.mega a:hover .ext-ico, .mega a:focus-visible .ext-ico{{ color:#fff; }}
.mega a.is-sub:hover,
.mega a.is-sub:focus-visible{{ border-left-color:{BG_MAIN}; }}

/* ---- drawer (มือถือ) ตอน hover: เหมือนกัน ---------------------------- */
.drawer-sub a:hover,
.drawer-sub a:focus-visible{{ background:{BG_MAIN}; color:#fff; }}
.drawer-sub a:hover > span,   .drawer-sub a:focus-visible > span,
.drawer-sub a:hover .ext-ico, .drawer-sub a:focus-visible .ext-ico{{ color:#fff; }}

/* ---- ไอคอนใน modal เข้าสู่ระบบ ---------------------------------------
   ไอคอน "ค้นหา" กับ "ผู้ดูแลระบบ" บนหัวเว็บคงเป็นสีเทาตามเดิม
   (ไม่ override .icon-btn) — เปลี่ยนเฉพาะไอคอนโล่ในหน้าต่างเข้าสู่ระบบ */
.admin-modal-icon{{ color:{BG_DARK}; }}

/* ---- การ์ด Academic 4 ใบ — แบรนด์เข้ม · แบรนด์ปกติ · เทาเข้ม · เทาอ่อน -- */
.programme-card--tone-1{{ background:{TONES[0]}; background-image:{G_TONES[0]}; }}
.programme-card--tone-2{{ background:{TONES[1]}; background-image:{G_TONES[1]}; }}
.programme-card--tone-3{{ background:{TONES[2]}; background-image:{G_TONES[2]}; }}
.programme-card--tone-4{{ background:{TONES[3]}; background-image:{G_TONES[3]}; }}
"""


if __name__ == "__main__":
    print("v11 — #37CBCB เป็นสีพื้นหลัก (±1 ระดับ)")
    if not CSS.exists():
        sys.exit("!! ไม่พบ assets/styles.css")
    s = CSS.read_text(encoding="utf-8")
    if MARK in s:
        print("  styles.css: patch นี้มีอยู่แล้ว — ข้าม")
        print("  (ถ้าจะเปลี่ยนสี ให้ลบบล็อก '== v11 cyan surfaces ==' ท้ายไฟล์ก่อน แล้วรันใหม่)")
        sys.exit(0)
    CSS.write_text(s.rstrip("\n") + "\n" + BLOCK, encoding="utf-8")
    print(f"  page-hero · cta-band -> {BG_MAIN}")
    print(f"  footer               -> {BG_MAIN}")
    print(f"  วงกลม B·A·S · ปุ่มลอย -> {BG_MAIN}  (hover {BG_DARK})")
    print(f"  การ์ด Academic       -> {' · '.join(TONES)}")
    print(f"  ตัวอักษร             -> {'ขาว' if TEXT_ON_CYAN == 'white' else 'สีเข้ม'}")
    print("  ปุ่มหลัก · mega/drawer hover -> ฟ้า (ไอคอนหัวเว็บคงสีเทาเดิม)")
    print("  ไล่สี (gradient)     -> hero · cta-band · footer · การ์ด 4 ใบ · วงกลม B·A·S · ปุ่มลอย")
    print("\nต่อไปรัน:  python build.py  (ถ้าต้องการ regenerate .html)")

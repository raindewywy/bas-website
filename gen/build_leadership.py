# -*- coding: utf-8 -*-
"""สร้างหน้าผู้บริหาร (leadership.html) + หน้าประวัติรายบุคคล 11 หน้า"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
from data_leaders import GROUPS, LEADERS  # noqa: E402

E = html.escape
EXT_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'width="14" height="14" aria-hidden="true"><path d="M14 4h6v6"/>'
            '<path d="M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'width="14" height="14" aria-hidden="true"><path d="M5 12h13"/><path d="M13 6l6 6-6 6"/></svg>')


def photo(label="ภาพถ่าย (รอไฟล์จากคณะ)"):
    return '<div class="staff-photo"><span class="ph-label">%s</span></div>' % E(label)


def cv_button(p):
    return (
        '<a class="btn btn-secondary btn-sm cv-link" href="%s" target="_blank" rel="noopener" '
        'aria-label="ดาวน์โหลด CV ของ%s (ไฟล์ PDF เปิดในแท็บใหม่)">ดาวน์โหลด CV (PDF) %s</a>'
        % (p["cv"], E(p["name_th"]), EXT_ICON)
    )


def card(p):
    return (
        '<div class="staff-card leader-card reveal">'
        + photo()
        + '<div class="staff-info">'
        + '<div class="th-name th-body" style="font-weight:700;font-size:1.02rem;">'
        + '<a class="leader-link" href="leader-%s.html">%s</a></div>' % (p["slug"], E(p["name_th"]))
        + '<div class="en-name" style="color:var(--muted);font-size:.85rem;">%s</div>' % E(p["name_en"])
        + '<div class="staff-role th-body">%s</div>' % E(p["role_th"])
        + '<div class="staff-dept">%s</div>' % E(p["dept_th"])
        + '<span class="staff-more">ดูประวัติ %s</span>' % ARROW
        + "</div></div>"
    )


def build_index():
    dean = [p for p in LEADERS if p["group"] == "dean"][0]
    body = [
        common.breadcrumb([("หน้าแรก", "index.html"), ("เกี่ยวกับคณะ", "about.html"), ("ผู้บริหาร", None)]),
        '<section class="page-hero"><div class="wrap">',
        '<p class="eyebrow th-body">เกี่ยวกับคณะ</p>',
        '<h1 class="bi-heading"><span class="bi-th th-body">ผู้บริหารคณะ</span>'
        '<span class="bi-en">Faculty Leadership</span></h1>',
        '<p class="lede th-body">คณบดี รองคณบดี ผู้ช่วยคณบดี และหัวหน้าภาควิชา '
        'ผู้กำหนดทิศทางวิชาการและพันธกิจเพื่อสังคมของคณะบริหารธุรกิจเพื่อสังคม มศว</p>',
        "</div></section>",
        '<section class="section"><div class="wrap">',
        # ---- คณบดี: เน้นเป็นบล็อกเดี่ยว ไม่ปนกับการ์ดอื่น ----
        '<div class="leader-group"><div class="leader-group-head"><h2 class="th-body">คณบดี</h2>'
        '<span class="en">Dean</span></div>',
        '<div class="leader-dean">',
        photo(),
        '<div class="leader-dean-copy">',
        '<h3 class="th-body" style="font-size:var(--step-h3);margin:0;">%s</h3>' % E(dean["name_th"]),
        '<p style="color:var(--muted);margin:.2rem 0 0;">%s</p>' % E(dean["name_en"]),
        '<p class="staff-role th-body" style="font-size:.95rem;">%s · %s</p>' % (E(dean["role_th"]), E(dean["dept_th"])),
        '<p class="th-body" style="margin-top:var(--space-3);">ความเชี่ยวชาญ: %s</p>' % E(dean["expertise_th"]),
        '<p style="margin-top:var(--space-3);display:flex;gap:.6rem;flex-wrap:wrap;">'
        '<a class="btn btn-primary btn-sm" href="leader-%s.html">ดูประวัติฉบับเต็ม</a>%s</p>'
        % (dean["slug"], cv_button(dean)),
        "</div></div></div>",
    ]
    for key, th, en in GROUPS:
        if key == "dean":
            continue
        people = [p for p in LEADERS if p["group"] == key]
        if not people:
            continue
        body.append(
            '<div class="leader-group"><div class="leader-group-head">'
            '<h2 class="th-body">%s</h2><span class="en">%s</span></div>' % (E(th), E(en))
        )
        body.append('<div class="staff-grid">' + "".join(card(p) for p in people) + "</div></div>")

    body.append(
        '<p class="source-note th-body">ข้อมูลผู้บริหาร ตำแหน่ง ประวัติการศึกษา และไฟล์ CV '
        'นำมาจากเว็บไซต์ทางการของคณะ (bas.swu.ac.th และ bas2.swu.ac.th) ตรวจสอบเมื่อ 5 กันยายน 2569 '
        '— ภาพถ่ายผู้บริหารยังรอไฟล์จากคณะ</p>'
    )
    body.append("</div></section>")
    # ---- REQ-C-DEAN2 (v9): สายตรงคณบดี ย้ายมาจาก contact.html ----
    body.append(
        '<section class="section" id="dean-direct" style="background:var(--paper-dim);">'
        '<div class="wrap">'
        '<div class="section-head reveal"><div>'
        '<p class="eyebrow">สายตรงคณบดี</p>'
        '<h2 class="bi-heading"><span class="bi-th th-body">สายตรงคณบดี</span>'
        '<span class="bi-en">Direct Line to the Dean</span></h2>'
        '<p class="lede th-body">ช่องทางส่งข้อเสนอแนะ ข้อร้องเรียน '
        'หรือเรื่องที่ต้องการให้คณบดีรับทราบโดยตรง</p>'
        '</div></div>'
        '<div class="split mt-5"><div class="split-copy reveal">'
        '<p class="th-body"><strong>%s</strong> · %s</p>'
        '<p class="mt-3"><a class="btn dean-mail-btn" href="mailto:%s">'
        '<i class="fa-solid fa-envelope" aria-hidden="true"></i>'
        '<span>ส่งอีเมลถึงคณบดีโดยตรง</span></a></p>'
        '<p class="th-body mt-3"><a class="link-arrow" href="leader-%s.html">ดูประวัติคณบดี</a></p>'
        '</div><div class="split-copy reveal"></div></div>'
        '</div></section>'
        % (E(dean["name_th"]), E(dean["role_th"]), dean["email"], dean["slug"])
    )
    return common.page(
        "leadership.html",
        "ผู้บริหารคณะ — BAS SWU",
        "คณบดี รองคณบดี ผู้ช่วยคณบดี และหัวหน้าภาควิชา คณะบริหารธุรกิจเพื่อสังคม มศว พร้อมประวัติและ CV",
        "about",
        "\n".join(body),
    )


def build_profile(p):
    meta = [
        ("ตำแหน่งบริหาร", E(p["role_th"]) + ' <span style="color:var(--muted)">/ %s</span>' % E(p["role_en"])),
        ("ภาควิชา", E(p["dept_th"])),
        ("อีเมล", '<a href="mailto:%s">%s</a>' % (p["email"], p["email"])),
        ("ความเชี่ยวชาญ", E(p["expertise_th"])),
    ]
    body = [
        common.breadcrumb(
            [("หน้าแรก", "index.html"), ("เกี่ยวกับคณะ", "about.html"),
             ("ผู้บริหาร", "leadership.html"), (p["name_th"], None)]
        ),
        '<section class="section"><div class="wrap">',
        '<div class="profile-head">',
        photo(),
        "<div>",
        '<p class="eyebrow th-body">%s</p>' % E(p["role_th"]),
        '<h1 class="th-body" style="font-size:var(--step-h2);margin:0;">%s</h1>' % E(p["name_th"]),
        '<p style="color:var(--muted);margin:.3rem 0 0;font-size:1.02rem;">%s</p>' % E(p["name_en"]),
        '<ul class="profile-meta">'
        + "".join('<li><span class="k th-body">%s</span><span class="th-body">%s</span></li>' % (k, v) for k, v in meta)
        + "</ul>",
        '<p style="margin-top:var(--space-4);">%s</p>' % cv_button(p),
        '<p class="cv-note th-body">ไฟล์ CV เปิดจากเว็บไซต์ทางการของคณะโดยตรง '
        '(ยังไม่ได้ย้ายมาเก็บบนเว็บใหม่ — เมื่อย้ายแล้วจะระบุขนาดไฟล์กำกับปุ่มด้วย)</p>',
        "</div></div>",
    ]
    if p.get("cert_th"):
        body.append(
            '<div class="notice th-body" style="margin-top:var(--space-5);"><span>%s</span></div>' % E(p["cert_th"])
        )
    body.append(
        '<div class="profile-section"><h2 class="th-body">ประวัติการศึกษา</h2>'
        '<ul class="edu-list th-body">' + "".join("<li>%s</li>" % E(x) for x in p["edu"]) + "</ul></div>"
    )
    body.append(
        '<div class="profile-section"><h2 class="th-body">ความเชี่ยวชาญ</h2>'
        '<p class="th-body">%s</p></div>' % E(p["expertise_th"])
    )
    body.append(
        '<div class="profile-section"><h2 class="th-body">ผลงานวิจัยและบริการวิชาการ</h2>'
        '<div class="notice th-body"><span>ส่วนนี้ยังไม่มีข้อมูลบนเว็บไซต์ทางการ — '
        'รอรายการผลงานตีพิมพ์ วิชาที่สอน และงานบริการวิชาการจากคณะ '
        'ระหว่างนี้สามารถดูรายละเอียดได้จากไฟล์ CV ด้านบน</span></div></div>'
    )
    body.append(
        '<p class="source-note th-body">ที่มาข้อมูล: <a href="%s" target="_blank" rel="noopener">%s</a> '
        '· ตรวจสอบเมื่อ 5 กันยายน 2569</p>' % (p["source"], E(p["source"]))
    )
    body.append(
        '<p style="margin-top:var(--space-5);"><a class="link-arrow" href="leadership.html">'
        '&larr; กลับไปหน้าผู้บริหารทั้งหมด</a></p>'
    )
    body.append("</div></section>")
    return common.page(
        "leader-%s.html" % p["slug"],
        "%s — ผู้บริหาร BAS SWU" % p["name_th"],
        "%s %s คณะบริหารธุรกิจเพื่อสังคม มศว — ประวัติการศึกษา ความเชี่ยวชาญ และ CV"
        % (p["name_th"], p["role_th"]),
        "about",
        "\n".join(body),
    )


if __name__ == "__main__":
    out = [build_index()] + [build_profile(p) for p in LEADERS]
    for f in out:
        print("built", f.name)

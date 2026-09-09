# -*- coding: utf-8 -*-
"""สลับชุดฟอนต์ทั้งเว็บเป็น IBM Plex Sans Thai + IBM Plex Mono (ทิศทาง SYSTEMS)"""
import glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FONT_LINK = (
    '<link href="https://fonts.googleapis.com/css2?'
    'family=IBM+Plex+Sans+Thai:wght@400;500;600;700&'
    'family=IBM+Plex+Sans:wght@400;500;600;700&'
    'family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">'
)

for path in sorted(glob.glob(str(ROOT / "*.html"))):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    s2 = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">',
                lambda _: FONT_LINK, s, count=1)
    if s2 != s:
        p.write_text(s2, encoding="utf-8")
        print("fonts:", p.name)

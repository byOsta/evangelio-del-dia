#!/usr/bin/env python3
"""Generate daily dummy/authorized EPUBs and a rolling 31-day catalog."""
from __future__ import annotations
import html
import json
import os
import shutil
import sys
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor" / "lecturasdeldia"))
import liturgia
from proveedor_lecturas import get_readings

TZ = ZoneInfo("Europe/Madrid")
SOURCE_URL = "https://lecturasdeldia.org/"
RAW_BASE = "https://raw.githubusercontent.com/byOsta/evangelio-del-dia/master"
CATALOG = ROOT / "catalog" / "index.json"
EPUB_DIR = ROOT / "epubs"
HISTORY_DAYS = int(os.environ.get("HISTORY_DAYS", "30"))

def esc(value):
    return html.escape(str(value or ""), quote=True)

def xhtml_page(day, liturgical, readings, mode):
    parts = []
    if mode == "dummy_lorem_ipsum":
        parts.append('<p class="warning">DATOS FICTICIOS DE PRUEBA · LOREM IPSUM · NO SON LECTURAS REALES</p>')
    for reading in readings:
        label = esc(reading.get("label") or reading.get("slot") or "Lectura")
        citation = esc(reading.get("citation") or "Cita pendiente de autorización")
        text = esc(reading.get("text") or "Contenido pendiente de autorización.")
        paragraphs = "".join(f"<p>{esc(line)}</p>" for line in str(reading.get("text") or "").splitlines() if line.strip())
        parts.append(f'<section><h2>{label}</h2><p class="citation">{citation}</p>{paragraphs or "<p>Contenido pendiente.</p>"}</section>')
    name = esc(liturgical.get("name") or liturgical.get("day_name") or "Día litúrgico")
    season = esc(liturgical.get("season") or "")
    notice = ("Este EPUB contiene texto ficticio de prueba. No utilizar como fuente litúrgica."
              if mode == "dummy_lorem_ipsum" else
              "Contenido generado desde la fuente configurada por el propietario del repositorio.")
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es"><head><title>{name}</title>
<style>body{{font-family:serif;line-height:1.55;margin:5%;}}h1{{font-size:1.5em;}}h2{{font-size:1.15em;margin-top:1.8em;}}.citation{{font-style:italic;}}.warning{{border:1px solid #900;padding:.8em;font-weight:bold;}}section{{page-break-inside:avoid;}}</style></head>
<body><h1>{name}</h1><p>{day.strftime("%d/%m/%Y")} · {season}</p><p>{esc(notice)}</p>{''.join(parts)}
<p><small>Proyecto Lecturas del Día · Fuente de referencia: {esc(SOURCE_URL)}</small></p></body></html>'''

def make_epub(path, day, liturgical, readings, mode):
    title = f"Evangelio y lecturas — {day.isoformat()}"
    identifier = f"urn:evangelio-del-dia:{day.isoformat()}"
    page = xhtml_page(day, liturgical, readings, mode)
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0" xml:lang="es">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">{identifier}</dc:identifier><dc:title>{esc(title)}</dc:title><dc:language>es</dc:language><dc:creator>Lecturas del Día</dc:creator><meta property="dcterms:modified">{datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%SZ")}</meta></metadata>
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="day" href="day.xhtml" media-type="application/xhtml+xml"/></manifest>
<spine><itemref idref="day"/></spine></package>'''
    nav = f'''<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Índice</title></head><body><nav epub:type="toc"><h1>Índice</h1><ol><li><a href="day.xhtml">{esc(title)}</a></li></ol></nav></body></html>'''
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/nav.xhtml", nav)
        z.writestr("OEBPS/day.xhtml", page)

def main():
    today = datetime.now(TZ).date()
    first = today - timedelta(days=HISTORY_DAYS)
    items = []
    EPUB_DIR.mkdir(parents=True, exist_ok=True)
    keep = set()
    for offset in range(HISTORY_DAYS + 1):
        day = first + timedelta(days=offset)
        liturgical = liturgia.calculate(day)
        readings, mode = get_readings(day, liturgical)
        filename = f"{day.isoformat()}.epub"
        make_epub(EPUB_DIR / filename, day, liturgical, readings, mode)
        keep.add(filename)
        day_name = liturgical.get("name") or liturgical.get("day_name") or "Día litúrgico"
        items.append({
            "id": day.isoformat(),
            "title": f"Evangelio — {day.strftime('%d/%m/%Y')}",
            "author": day_name,
            "description": ("PRUEBA: Lorem ipsum, no son lecturas reales." if mode == "dummy_lorem_ipsum" else "Lecturas del día."),
            "url": f"{RAW_BASE}/epubs/{filename}",
            "date": day.isoformat(),
            "content_mode": mode,
            "source_url": SOURCE_URL
        })
    for old in EPUB_DIR.glob("*.epub"):
        if old.name not in keep:
            old.unlink()
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "timezone": "Europe/Madrid",
        "calendar_engine": "zeanuri/lecturasdeldia — liturgia.py (MIT)",
        "content_mode": "dummy_lorem_ipsum" if not os.environ.get("CEE_LECTIONARY_PATH") else "authorized_source",
        "notice": "Los EPUB actuales son de prueba Lorem ipsum. Sustituir por contenido autorizado antes de uso litúrgico.",
        "history_days": HISTORY_DAYS,
        "items": list(reversed(items))
    }
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generados {len(items)} EPUBs y catálogo en {CATALOG}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate a CrossPoint catalog with the upstream Spanish liturgical engine."""
from __future__ import annotations
import json, os, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor" / "lecturasdeldia"))
import liturgia

TZ = ZoneInfo("Europe/Madrid")
SOURCE_URL = "https://lecturasdeldia.org/"
OUT = ROOT / "catalog" / "index.json"

def clean_readings(raw):
    """Keep citations only; never serialize protected reading text."""
    if not isinstance(raw, dict):
        return []
    ordered = []
    for key in ("vigilia_lecturas", "primera", "salmo", "segunda", "aclamacion", "evangelio"):
        value = raw.get(key)
        for entry in (value if isinstance(value, list) else [value]):
            if isinstance(entry, dict) and entry.get("cita"):
                ordered.append({"slot": key, "citation": str(entry["cita"])})
    return ordered

def main():
    now = datetime.now(TZ)
    day = now.date()
    result = liturgia.calculate(day)
    item = {
        "id": day.isoformat(),
        "title": f"Evangelio y lecturas — {day.isoformat()}",
        "subtitle": result.get("name") or result.get("day_name") or "Calendario litúrgico CEE",
        "description": "Consulta las lecturas completas en la fuente original.",
        "date": day.isoformat(),
        "source_url": SOURCE_URL,
        "liturgical_day": result.get("name"),
        "season": result.get("season"),
        "rank": result.get("rank"),
        "citations": [],
    }
    data_path = os.environ.get("CEE_LECTIONARY_PATH")
    if data_path:
        path = Path(data_path)
        if not path.is_file():
            raise FileNotFoundError(f"No existe CEE_LECTIONARY_PATH: {path}")
        cache = json.loads(path.read_text(encoding="utf-8"))
        raw = liturgia.lookup_readings(result, cache=cache)
        if raw is None:
            raise RuntimeError(f"El motor no encontró lecturas para {day.isoformat()}; no se publicará un catálogo incompleto.")
        item["citations"] = clean_readings(raw)
        item["description"] = "Citas bíblicas del día. El texto completo se consulta en la fuente original."
    payload = {
        "generated_at": now.isoformat(timespec="seconds"),
        "timezone": "Europe/Madrid",
        "calendar": "Calendario litúrgico español — motor de zeanuri/lecturasdeldia",
        "source": SOURCE_URL,
        "content_policy": "metadata_and_citations_only",
        "notice": "No se copian textos bíblicos ni del Leccionario. La licencia MIT cubre el código del motor, no los datos litúrgicos.",
        "data_status": "citations_available" if data_path else "cee_data_not_configured",
        "items": [item],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Catálogo actualizado: {OUT} ({payload['data_status']})")

if __name__ == "__main__":
    main()

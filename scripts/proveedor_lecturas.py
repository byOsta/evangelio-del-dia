"""Adaptador de lecturas intercambiable.

Modo inicial: plantilla Lorem ipsum sin derechos de terceros.
Modo autorizado: define CEE_LECTIONARY_PATH con el JSON del Leccionario
obtenido legalmente; se consulta el mismo lookup_readings() del motor upstream.
Este adaptador es la única pieza que habrá que revisar al cambiar de fuente.
"""
from __future__ import annotations
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DUMMY_PATH = ROOT / "data" / "plantilla_dummy.json"

LABELS = {
    "vigilia_lecturas": "Lectura de la Vigilia",
    "primera": "Primera lectura",
    "salmo": "Salmo responsorial",
    "segunda": "Segunda lectura",
    "aclamacion": "Aclamación",
    "evangelio": "Evangelio",
}

def _normalise_upstream(raw):
    if not isinstance(raw, dict):
        return []
    out = []
    for slot in ("vigilia_lecturas", "primera", "salmo", "segunda", "aclamacion", "evangelio"):
        value = raw.get(slot)
        values = value if isinstance(value, list) else [value]
        for entry in values:
            if not isinstance(entry, dict):
                continue
            text = entry.get("texto") or entry.get("antifona") or ""
            citation = entry.get("cita") or ""
            if text or citation:
                out.append({
                    "slot": slot,
                    "label": LABELS.get(slot, slot.title()),
                    "citation": str(citation),
                    "text": str(text),
                })
    return out

def get_readings(day, liturgical_result):
    """Return (readings, content_mode); day is datetime.date."""
    upstream_path = os.environ.get("CEE_LECTIONARY_PATH")
    if upstream_path:
        import sys
        sys.path.insert(0, str(ROOT / "vendor" / "lecturasdeldia"))
        import liturgia
        path = Path(upstream_path)
        if not path.is_file():
            raise FileNotFoundError(f"CEE_LECTIONARY_PATH no existe: {path}")
        cache = json.loads(path.read_text(encoding="utf-8"))
        raw = liturgia.lookup_readings(liturgical_result, cache=cache)
        if raw is None:
            raise RuntimeError(f"No hay lecturas CEE para {day.isoformat()}; se cancela la generación.")
        return _normalise_upstream(raw), "authorized_source"
    template = json.loads(DUMMY_PATH.read_text(encoding="utf-8"))
    return template["readings"], "dummy_lorem_ipsum"

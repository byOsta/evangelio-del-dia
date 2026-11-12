#!/usr/bin/env python3
"""Genera un catálogo diario de referencias, sin copiar textos protegidos.

El calendario CEE se consulta en su fuente original. Este repositorio solo
publica la fecha, metadatos mínimos y un enlace a la fuente; no descarga ni
redistribuye el texto del Leccionario.
"""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "catalog" / "index.json"
SOURCE_URL = "https://lecturasdeldia.org/"


def main() -> None:
    today = datetime.now(ZoneInfo("Europe/Madrid")).date()
    date_text = today.isoformat()
    payload = {
        "generated_at": datetime.now(ZoneInfo("Europe/Madrid")).isoformat(timespec="seconds"),
        "timezone": "Europe/Madrid",
        "calendar": "Conferencia Episcopal Española (CEE)",
        "source": SOURCE_URL,
        "content_policy": "references_and_metadata_only",
        "notice": (
            "Este catálogo no reproduce textos bíblicos ni del Leccionario. "
            "Consulta las lecturas y sus citas en la fuente original."
        ),
        "items": [
            {
                "id": date_text,
                "title": f"Lecturas de la Misa — {date_text}",
                "subtitle": "Calendario litúrgico CEE",
                "description": "Abrir la fuente original para consultar las lecturas del día.",
                "date": date_text,
                "source_url": SOURCE_URL,
            }
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Catálogo actualizado: {OUTPUT}")


if __name__ == "__main__":
    main()

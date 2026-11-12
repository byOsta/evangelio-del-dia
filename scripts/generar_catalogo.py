#!/usr/bin/env python3
"""Genera el índice público del catálogo sin republicar textos protegidos.

El scraping y la generación de EPUB completos quedan deliberadamente
desactivados hasta disponer de una autorización/licencia de redistribución.
"""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "catalog" / "index.json"


def main() -> None:
    now = datetime.now(ZoneInfo("Europe/Madrid")).isoformat(timespec="seconds")
    payload = {
        "generated_at": now,
        "timezone": "Europe/Madrid",
        "source": "https://lecturasdeldia.org/",
        "status": "pending_content_rights",
        "notice": (
            "Catálogo preparado. Los textos íntegros y EPUB se publicarán "
            "cuando se confirme una licencia o autorización de redistribución."
        ),
        "items": [],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Índice actualizado: {OUTPUT}")


if __name__ == "__main__":
    main()

import os
import sys
from pathlib import Path


def obtener_directorio_datos():
    if getattr(sys, "frozen", False):
        local_app_data = os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local"
        base = Path(local_app_data) / "ElDescargador"
    else:
        base = Path(__file__).resolve().parents[2]

    base.mkdir(parents=True, exist_ok=True)
    return base

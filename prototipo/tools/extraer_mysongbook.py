"""Convierte un respaldo de MySongbook (.mysongbook, XML) al JSON que usa el prototipo.

Uso:
    python3 extraer_mysongbook.py respaldo.mysongbook datos.json
"""
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


def extraer(origen):
    root = ET.parse(origen).getroot()
    songs = []
    for s in root.findall("Song"):
        parts = [dict(p.attrib) for p in s.iter("Part")]
        tags = [t.get("Tag") for t in s.iter("Tag")]
        # Ignora cantos vacíos (sin título ni letra)
        if not s.get("Title", "").strip() and not any(p.get("Lyrics", "").strip() for p in parts):
            continue
        songs.append({"a": dict(s.attrib), "parts": parts, "tags": tags})

    sets = []
    for i, st in enumerate(root.findall("Set")):
        items = []
        for x in st:
            a = dict(x.attrib)
            items.append({
                "t": a.get("Title", ""),
                "ar": a.get("Artist", ""),
                "key": a.get("SetSongTransposeKeyName", ""),
                "tr": int(a.get("SetSongTranspose", "0") or 0),
                "a": a,
            })
        sets.append({"id": "set%d" % (i + 1), "title": st.get("Title", ""), "items": items})

    return {
        "v": 1,
        "savedAt": datetime.now(timezone.utc).isoformat(),
        "file": os.path.basename(origen),
        "songs": songs,
        "sets": sets,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    datos = extraer(sys.argv[1])
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    print("%d canciones, %d listas" % (len(datos["songs"]), len(datos["sets"])))

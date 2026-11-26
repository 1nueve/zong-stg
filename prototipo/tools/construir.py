"""Inserta los datos JSON en la plantilla y genera la página completa del prototipo.

Uso:
    python3 construir.py ../cancionero.template.html datos.json cancionero.html
"""
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    plantilla = open(sys.argv[1], encoding="utf-8").read()
    datos = open(sys.argv[2], encoding="utf-8").read()
    json.loads(datos)  # valida que sea JSON
    datos = datos.replace("<", "\\u003c")  # evita cerrar el <script> por accidente
    marca = "/*__DATA__*/"
    if plantilla.count(marca) != 1:
        sys.exit("La plantilla debe tener exactamente una marca " + marca)
    with open(sys.argv[3], "w", encoding="utf-8") as f:
        f.write(plantilla.replace(marca, datos))
    print("Listo:", sys.argv[3])

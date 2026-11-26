"""Empaqueta la página del prototipo en un .zip listo para subir a AWS Amplify (Implementar sin Git).

Amplify sirve el archivo index.html de la raíz, así que la página se guarda con ese nombre dentro del .zip.

Uso:
    python3 empaquetar_amplify.py ../cancionero.html zong-sitio.zip

El .zip lleva las letras de los cantos: no lo subas al repositorio (ya está en .gitignore).
"""
import sys
import zipfile

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    pagina = open(sys.argv[1], encoding="utf-8").read()
    if 'id="data"' not in pagina or "/*__DATA__*/" in pagina:
        sys.exit("Esa página no trae datos. Primero genera cancionero.html con construir.py.")
    with zipfile.ZipFile(sys.argv[2], "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("index.html", pagina)
    print("Listo:", sys.argv[2])

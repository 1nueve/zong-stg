# Zong · staging

Entorno de pruebas (staging) del prototipo "Cancionero y listas" de [Zong](https://github.com/1nueve/zong), publicado con AWS Amplify.

- `amplify.yml`: en cada publicación Amplify baja los cantos (`datos.json`) de un bucket S3 privado y arma `index.html`.
- `prototipo/cancionero.template.html`: la página, sin cantos (la marca `/*__DATA__*/` recibe el JSON).
- `prototipo/tools/`: convertir un respaldo de MySongbook a JSON, armar la página y empaquetarla.
- `docs/publicar-amplify.md`: guía paso a paso para conectar este repo a Amplify, S3 y el dominio.

Las letras de los cantos **no se suben a este repositorio**: tienen derechos de autor y viven en S3.

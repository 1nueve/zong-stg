# Zong · staging

Entorno de pruebas (staging) del prototipo "Cancionero y listas" de [Zong](https://github.com/1nueve/zong), publicado con AWS Amplify.

- `.github/workflows/publicar-amplify.yml`: con cada cambio en `main` (o a mano desde Actions) baja los cantos (`datos.json`) de un bucket S3 privado, arma `index.html` y lo publica en https://main.dfdniz78lcm41.amplifyapp.com.
- `prototipo/cancionero.template.html`: la página, sin cantos (la marca `/*__DATA__*/` recibe el JSON).
- `prototipo/tools/`: convertir un respaldo de MySongbook a JSON, armar la página y empaquetarla.
- `docs/publicar-amplify.md`: guía paso a paso para configurar S3, el usuario de AWS y los secretos de GitHub.

Las letras de los cantos **no se suben a este repositorio**: tienen derechos de autor y viven en S3.

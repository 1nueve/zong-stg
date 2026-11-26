# Publicar el prototipo en zong.1nueve.com (AWS Amplify)

Esta guía mueve el prototipo "Cancionero y listas" de claude.ai a tu cuenta de AWS, con AWS Amplify Hosting conectado a GitHub y el dominio `zong.1nueve.com`.

## Cómo funciona

- El prototipo es **una sola página** (`index.html`) que lleva dentro los cantos y las listas.
- Las letras tienen derechos de autor, así que **no van al repositorio**. Se guardan en un archivo privado, `datos.json`, en **S3** (el almacenamiento de AWS).
- Cada vez que Amplify publica, hace esto (lo dice `amplify.yml`):
  1. Toma el código de GitHub (rama `main`).
  2. Baja `datos.json` de S3.
  3. Arma `index.html` con `prototipo/tools/construir.py` y lo publica.
- Resultado: **los cambios de código se publican solos** al aprobar un PR. Los cambios de cantos y listas se publican subiendo un `datos.json` nuevo a S3.

## Qué cambia respecto a claude.ai

| | En claude.ai | En zong.1nueve.com |
|---|---|---|
| Ver cantos, listas, transponer, pantalla completa | Sí | Sí |
| Descargar para MySongbook | Sí | Sí (descarga normal del navegador) |
| Botón **Guardar** | Guarda para todos | Se llama **Descargar para publicar**: baja `zong-sitio.zip` con `datos.json` actualizado (ver paso 5) |
| Cambios sin publicar | Se quedan en el navegador | Igual: se quedan en el navegador hasta que publiques |

**Los datos no se pierden al mudarse**, porque lo guardado vive dentro de la página. Lo único que no se muda son los cambios que alguien dejó **sin guardar** en claude.ai (viven en el navegador de esa persona). Antes de mudarte, presiona **Guardar** en claude.ai.

Después de la mudanza, usa **una sola** como la buena: zong.1nueve.com.

## Paso 1. Guardar los cantos en S3 (privado)

1. En la consola de AWS abre **S3** → **Crear bucket**.
2. Nombre: por ejemplo `zong-datos-1nueve` (debe ser único en todo AWS). Región: la misma que usarás en Amplify (por ejemplo `us-east-1`).
3. Deja marcado **Bloquear todo el acceso público**. Crear.
4. Entra al bucket → **Cargar** → sube el `datos.json` que te pasé. Queda en `s3://zong-datos-1nueve/datos.json`.

## Paso 2. Crear la app en Amplify conectada a GitHub

1. Abre **AWS Amplify** → **Crear nueva aplicación** → **GitHub** → autoriza y elige el repo `1nueve/zong-stg`, rama `main`.
2. En la configuración de compilación Amplify detecta `amplify.yml` solo. No cambies nada.
3. En **Configuración avanzada → Variables de entorno** agrega:
   - Variable: `ZONG_DATOS_S3`
   - Valor: `s3://zong-datos-1nueve/datos.json`
4. En **Rol de servicio**, elige **Crear y usar un nuevo rol de servicio**. Anota su nombre (algo como `AmplifySSRLoggingRole-…` o `amplifyconsole-backend-role`).
5. **Guardar e implementar**. La primera vez va a **fallar** en el paso de S3, porque el rol aún no puede leer el bucket. Es normal: sigue al paso 3.

## Paso 3. Dar permiso al rol para leer los cantos

1. Abre **IAM → Roles** y busca el rol del paso anterior.
2. **Agregar permisos → Crear política insertada** → pestaña **JSON** y pega (cambia el nombre del bucket si usaste otro):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::zong-datos-1nueve/datos.json"
    }
  ]
}
```

3. Nómbrala `zong-leer-datos` y guarda.
4. Vuelve a Amplify → rama `main` → **Volver a implementar esta versión** (Redeploy this version). Ahora sí debe quedar verde. Abre la dirección `https://main.d….amplifyapp.com` y revisa tus cantos.

> Si en el paso 2 Amplify no te dejó elegir rol: en la app ve a **Configuración de la aplicación → Configuración general → Rol de servicio → Editar** y crea o elige uno.

## Paso 4. Conectar zong.1nueve.com

1. En la app: **Hosting → Dominios personalizados → Agregar dominio**.
2. Escribe `1nueve.com` → **Configurar dominio**.
3. **Quita la raíz y `www`** y deja solo el subdominio **`zong`** apuntando a `main`.
4. Certificado: **administrado por Amplify** (gratis). **Guardar**.

El DNS de 1nueve.com está en **Route 53**. Si la zona está en la misma cuenta de AWS, Amplify crea los registros solo; no tocas Route 53. Espera a que diga **Disponible** (5 a 30 minutos).

Si Route 53 está en **otra cuenta**, crea a mano en esa zona (Route 53 → Zonas hospedadas → 1nueve.com → Crear registro) los dos CNAME que muestra Amplify: uno que empieza con `_` (comprueba el certificado) y `zong` → `d….cloudfront.net`. No toques los demás registros de 1nueve.com.

## Paso 5 (recomendado). Ponerle contraseña

1. **Hosting → Control de acceso → Administrar acceso**.
2. En `main` elige **Restringido: se requiere contraseña**, pon usuario y contraseña, guarda.
3. Compártelos con tu grupo; el navegador los pide una vez.

La página además trae una etiqueta para que Google no la muestre en búsquedas.

## Cada vez que cambies cantos o listas

1. En zong.1nueve.com haz tus cambios y presiona **Descargar para publicar**. Se baja `zong-sitio.zip`.
2. Descomprímelo: trae `index.html` y `datos.json`.
3. En **S3** → tu bucket → **Cargar** → sube el nuevo `datos.json` (reemplaza el anterior).
4. En **Amplify** → rama `main` → **Volver a implementar esta versión**. En un par de minutos todos ven los cambios (si alguien no, que toque ↻).

Los cambios de **código** no necesitan nada de esto: al aprobar el PR en GitHub, Amplify publica solo.

## Generar datos.json desde un respaldo de MySongbook (opcional)

```bash
python3 prototipo/tools/extraer_mysongbook.py mi-respaldo.mysongbook datos.json
```

Y súbelo a S3 como en el paso 1.

## Plan B: sin Git (arrastrar un zip)

Si algo de lo anterior se complica, Amplify también acepta **Implementar sin Git**: arrastras un `.zip` con `index.html`. El `index.html` que viene en `zong-sitio.zip` sirve tal cual (empácalo solo, o usa `prototipo/tools/empaquetar_amplify.py`). Una app sin Git no se puede convertir después a Git; habría que crear otra.

## Costo

Amplify cobra por minutos de compilación, almacenamiento y tráfico; S3 por almacenamiento. Para un sitio de un archivo y un grupo son centavos al mes.

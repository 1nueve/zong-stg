# Publicar el prototipo en Amplify desde GitHub

Este repo publica el prototipo "Cancionero y listas" en la app de Amplify que ya existe, **https://main.dfdniz78lcm41.amplifyapp.com**, sin cambiar su dirección.

## Cómo funciona

- La app de Amplify se creó "sin Git", así que no se conecta directo a GitHub. En su lugar, **GitHub Actions** la publica: con cada cambio en `main` (o cuando tú lo pides), arma la página y se la sube a Amplify.
- Las letras tienen derechos de autor, así que **no van al repositorio**. Viven en un archivo privado, `datos.json`, en **S3**.
- Pasos de cada publicación (archivo `.github/workflows/publicar-amplify.yml`):
  1. Baja `datos.json` de S3.
  2. Arma `index.html` con `prototipo/tools/construir.py`.
  3. Se lo entrega a Amplify (igual que arrastrar el zip, pero automático).

## Configuración (una sola vez)

### 1. Guardar los cantos en S3

1. Consola de AWS → **S3** → **Crear bucket**. Nombre, por ejemplo, `zong-datos-1nueve`. Región: la misma de la app de Amplify (la ves arriba a la derecha cuando abres la app).
2. Deja marcado **Bloquear todo el acceso público**. Crear.
3. **Cargar** → sube tu `datos.json` (viene dentro del zip de **Descargar para publicar**).

### 2. Crear un usuario de AWS solo para GitHub

1. **IAM → Usuarios → Crear usuario**. Nombre: `github-zong-stg`. **No** le des acceso a la consola.
2. En permisos elige **Adjuntar políticas directamente → Crear política** → pestaña **JSON** y pega (cambia la región `us-east-1`, el número de cuenta `123456789012` y el bucket si son distintos):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::zong-datos-1nueve/datos.json"
    },
    {
      "Effect": "Allow",
      "Action": ["amplify:CreateDeployment", "amplify:StartDeployment", "amplify:GetJob"],
      "Resource": "arn:aws:amplify:us-east-1:123456789012:apps/dfdniz78lcm41/branches/main/*"
    },
    {
      "Effect": "Allow",
      "Action": ["amplify:CreateDeployment", "amplify:StartDeployment"],
      "Resource": "arn:aws:amplify:us-east-1:123456789012:apps/dfdniz78lcm41/branches/main"
    }
  ]
}
```

   Tu número de cuenta lo ves arriba a la derecha de la consola, al tocar tu nombre.
3. Nómbrala `zong-stg-publicar`, créala, vuelve a la pestaña del usuario, búscala, márcala y termina de crear el usuario.
4. Entra al usuario → **Credenciales de seguridad → Crear clave de acceso** → elige **Aplicación que se ejecuta fuera de AWS**. Copia la **clave de acceso** y la **clave secreta** (la secreta solo se muestra una vez).

### 3. Guardar la configuración en GitHub

En https://github.com/1nueve/zong-stg → **Settings → Secrets and variables → Actions**:

- Pestaña **Secrets** → **New repository secret**:
  - `AWS_ACCESS_KEY_ID` = la clave de acceso
  - `AWS_SECRET_ACCESS_KEY` = la clave secreta
- Pestaña **Variables** → **New repository variable**:
  - `AWS_REGION` = la región de tu app (por ejemplo `us-east-1`)
  - `AMPLIFY_APP_ID` = `dfdniz78lcm41`
  - `ZONG_DATOS_S3` = `s3://zong-datos-1nueve/datos.json`

### 4. Probar

En GitHub → pestaña **Actions** → **Publicar en Amplify** → **Run workflow**. En uno o dos minutos debe quedar en verde, y la página se actualiza en https://main.dfdniz78lcm41.amplifyapp.com. Si sale en rojo, el mensaje dice qué falta.

## Día a día

- **Cambios de código:** cuando unes un PR a `main`, se publica solo.
- **Cambios de cantos o listas:** en la página presiona **Descargar para publicar**, descomprime el zip, sube el `datos.json` nuevo a S3 (reemplaza el anterior) y en GitHub → **Actions** → **Publicar en Amplify** → **Run workflow**.

Esto último desaparece cuando la página guarde directo en la base de datos (Supabase).

## Qué cambia respecto a claude.ai

| | En claude.ai | En Amplify |
|---|---|---|
| Ver cantos, listas, transponer, pantalla completa | Sí | Sí |
| Descargar para MySongbook | Sí | Sí (descarga normal del navegador) |
| Botón **Guardar** | Guarda para todos | Se llama **Descargar para publicar**: baja `zong-sitio.zip` con `datos.json` actualizado (ver "Día a día") |
| Cambios sin publicar | Se quedan en el navegador | Igual: se quedan en el navegador hasta que publiques |

**Los datos no se pierden al mudarse**, porque lo guardado vive dentro de la página. Lo único que no se muda son los cambios que alguien dejó **sin guardar** en claude.ai (viven en el navegador de esa persona). Antes de mudarte, presiona **Guardar** en claude.ai.

Después de la mudanza, usa **una sola** como la buena: la de Amplify.

## Más adelante: dominio propio

1. En la app: **Hosting → Dominios personalizados → Agregar dominio**.
2. Escribe `1nueve.com` → **Configurar dominio**.
3. **Quita la raíz y `www`** y deja solo el subdominio **`zong`** apuntando a `main`.
4. Certificado: **administrado por Amplify** (gratis). **Guardar**.

El DNS de 1nueve.com está en **Route 53**. Si la zona está en la misma cuenta de AWS, Amplify crea los registros solo; no tocas Route 53. Espera a que diga **Disponible** (5 a 30 minutos).

Si Route 53 está en **otra cuenta**, crea a mano en esa zona (Route 53 → Zonas hospedadas → 1nueve.com → Crear registro) los dos CNAME que muestra Amplify: uno que empieza con `_` (comprueba el certificado) y `zong` → `d….cloudfront.net`. No toques los demás registros de 1nueve.com.

## Recomendado: ponerle contraseña

1. **Hosting → Control de acceso → Administrar acceso**.
2. En `main` elige **Restringido: se requiere contraseña**, pon usuario y contraseña, guarda.
3. Compártelos con tu grupo; el navegador los pide una vez.

La página además trae una etiqueta para que Google no la muestre en búsquedas.


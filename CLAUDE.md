# Instrucciones para Claude en el repositorio Zong

- Este repo es el staging del prototipo. El contexto completo (producto, arquitectura, pendientes) está en `docs/contexto.md` del repo principal, https://github.com/1nueve/zong. Léelo antes de proponer cambios grandes.
- Responde siempre en **español**. El dueño del proyecto no es programador de tiempo completo: explica en palabras simples.
- Cuando el usuario pida ver algo antes de hacerlo, muestra una maqueta o un plan y **espera su aprobación** antes de construir.
- **Nunca subas letras de cantos** ni archivos `.mysongbook` al repositorio; tienen derechos de autor. Para pruebas usa cantos de dominio público o inventados.
- Todo texto de la interfaz va en archivos de traducción (`es.json`, `en.json`…), nunca escrito directo en el código.
- Los cantos se guardan en ChordPro (`[G]letra`) con cifrado americano; la transposición y el cifrado latino (Do, Re, Mi) se aplican al mostrarlos.
- El aislamiento entre grupos se hace con Row Level Security en la base de datos, no solo en la app. Toda tabla nueva lleva sus políticas y pruebas por rol.
- Trabaja en una rama y abre un pull request; no hagas commits directos a `main` salvo que el usuario lo pida.

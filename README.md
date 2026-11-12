# Evangelio del Día — plugin nativo CrossPoint / Xteink X3

Plugin **nativo** para CrossPoint: el lector navega un catálogo JSON, descarga EPUBs a la SD y permite leerlos offline. No utiliza navegador integrado, web UI propia ni JavaScript ejecutado en el X3.

## Estado funcional

- Motor de calendario litúrgico: `liturgia.py` de [zeanuri/lecturasdeldia](https://github.com/zeanuri/lecturasdeldia), incorporado bajo MIT en `vendor/lecturasdeldia/`.
- Generación de EPUB 3 con Python estándar, sin dependencias externas.
- Catálogo con hoy y los 30 días anteriores.
- GitHub Actions genera y publica catálogo + EPUBs a diario a las 00:01, hora de Madrid, y al modificar el código.
- El plugin nativo descarga el EPUB seleccionado a `/Evangelio del Día` en la SD.
- **Modo actual:** Lorem ipsum ficticio, visible y rotulado como contenido de prueba en cada EPUB.
- **Modo autorizado:** el workflow puede descargar el JSON CEE desde una URL privada configurada en secretos de GitHub y el adaptador usa `liturgia.lookup_readings()`.

## Qué hay que cambiar cuando se obtenga autorización

1. Aloja el JSON del Leccionario autorizado en un almacenamiento privado o endpoint HTTPS que permita descargarlo desde GitHub Actions.
2. En GitHub → Settings → Secrets and variables → Actions, crea:
   - `CEE_LECTIONARY_URL`: URL de descarga del JSON autorizado.
   - `CEE_LECTIONARY_TOKEN`: token Bearer, solo si el endpoint lo requiere.
3. Ejecuta el workflow manualmente o espera a la siguiente ejecución. Si la URL está configurada, el generador deja de usar Lorem ipsum y carga las lecturas reales con el motor de referencia.
4. No subas el JSON protegido al repositorio público. La URL y el token se guardan como secretos.

El adaptador está en `scripts/proveedor_lecturas.py`; la plantilla de prueba en `data/plantilla_dummy.json`. El motor se conserva igual.

## Licencias

La licencia MIT del proyecto de referencia cubre el código, no `data/*.json` ni los textos litúrgicos. El leccionario oficial y las traducciones conservan sus propios derechos. El repositorio no contiene ni redistribuye esos textos: únicamente datos ficticios Lorem ipsum hasta que se configure una fuente autorizada.

## Instalación en Xteink X3

1. En CrossPoint activa **Settings → Connectivity → Plugins**.
2. Copia `plugin/evangelio-del-dia/` a `/.crosspoint/plugins/evangelio-del-dia/` en la SD.
3. Conecta el lector a Wi-Fi y abre **Home → Plugins → Evangelio del Día**.
4. Selecciona una fecha y descarga su EPUB. Después podrás leerlo sin conexión.

La carpeta del plugin contiene `device.json` y un README de instalación. El manifiesto usa el catálogo JSON y la descarga directa declarativa documentada por CrossPoint. No se ha hecho una prueba física en un X3 desde este entorno.

## Automatización

Workflow: `.github/workflows/generar.yml`. Mantiene 31 días (hoy + 30 anteriores), limpia EPUBs caducados y publica los archivos generados. GitHub puede retrasar las ejecuciones programadas; las 00:01 no son una garantía exacta.

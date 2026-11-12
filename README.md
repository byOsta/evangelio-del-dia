# Evangelio del Día — CrossPoint / Xteink X3

Plugin **nativo** para CrossPoint Stable 2.0.0. No usa `plugin.js`, navegador ni JavaScript en el lector.

## Estado actual

Esta primera estructura prepara el catálogo y la automatización, pero **no publica todavía el texto íntegro de las lecturas**. Los textos litúrgicos de la CEE no se consideran de libre redistribución por el mero hecho de poder consultarse en una web. Antes de generar EPUBs públicos con el Evangelio completo hay que confirmar una licencia o autorización expresa.

## Estructura

- `plugin/evangelio-del-dia/device.json`: catálogo declarativo nativo de CrossPoint.
- `catalog/index.json`: índice JSON público que consulta el X3.
- `.github/workflows/generar.yml`: ejecución diaria a las 00:01, hora peninsular.
- `scripts/generar_catalogo.py`: generador inicial del índice (sin republicar textos).

## Instalación en el Xteink X3

Con CrossPoint Stable 2.0.0:

1. Activa **Settings → Connectivity → Plugins**.
2. Copia la carpeta `plugin/evangelio-del-dia/` a `/.crosspoint/plugins/evangelio-del-dia/` en la SD (también se admite `/plugins/`).
3. Conecta el lector a Wi-Fi y abre **Home → Plugins → Evangelio del Día**.

El catálogo remoto se sirve desde GitHub Raw. Para leer sin conexión, cada EPUB deberá descargarse al dispositivo; la descarga de textos completos se habilitará cuando esté aclarada su licencia.

## Fuente litúrgica

Se pretende usar el calendario litúrgico de la Conferencia Episcopal Española y lecturas de [lecturasdeldia.org](https://lecturasdeldia.org/) como referencia. El proyecto no está afiliado a la CEE ni a esa web.

## Automatización

GitHub Actions ejecuta el generador diariamente. La hora programada es una petición a GitHub Actions, no una garantía de ejecución exacta al minuto: GitHub puede retrasar las tareas programadas.

## Licencias y atribución

El código de este proyecto se publica bajo MIT (ver `LICENSE`). Esa licencia **no cubre** textos bíblicos, traducciones, comentarios, calendarios o contenidos de terceros que puedan incorporarse en el futuro. No se incluirán esos materiales sin permiso/licencia compatible.

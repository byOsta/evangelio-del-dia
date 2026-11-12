# Lecturas del Día — CrossPoint / Xteink X3

Plugin nativo para CrossPoint Stable 2.0.0. No utiliza navegador integrado, interfaz web propia ni JavaScript ejecutado en el lector.

## Estado actual

- El catálogo se genera diariamente con el motor de cálculo litúrgico español del proyecto [zeanuri/lecturasdeldia](https://github.com/zeanuri/lecturasdeldia).
- El motor Python (`liturgia.py`) se incluye en `vendor/lecturasdeldia/` bajo MIT, con su licencia y atribución.
- El motor calcula el día litúrgico; el leccionario CEE es un conjunto de datos separado y NO se redistribuye aquí.
- Sin un fichero de datos CEE autorizado, el catálogo muestra la celebración/calendario y enlaza a la fuente, pero no inventa citas ni textos.
- Si se configura un leccionario con autorización de uso, el generador utiliza `liturgia.lookup_readings()` y publica únicamente las citas bíblicas, nunca el texto.

## Datos del Leccionario y derechos

La licencia MIT del proyecto de referencia cubre el código, no `data/*.json` ni los textos litúrgicos que contienen. El propio repositorio indica que esos textos pertenecen a sus titulares y que la reutilización debe autorizarse por separado.

Para habilitar las citas exactas:
1. Obtén autorización para usar el JSON del Leccionario CEE en este flujo.
2. Guarda el fichero autorizado como `data/Leccionario_CL.json` (no lo subas al repositorio público).
3. Configura la variable de entorno `CEE_LECTIONARY_PATH` apuntando a ese fichero durante el workflow. El generador solo conserva citas y metadatos.

No se generan EPUBs con textos bíblicos porque todavía no se ha incorporado una traducción con licencia explícita de redistribución. Un EPUB completo offline requiere esa licencia o permiso expreso.

## Estructura

- `plugin/evangelio-del-dia/device.json`: catálogo declarativo para CrossPoint.
- `catalog/index.json`: índice público.
- `scripts/generar_catalogo.py`: cálculo litúrgico y extracción opcional de citas.
- `.github/workflows/generar.yml`: actualización diaria a las 00:01 hora de Madrid.
- `vendor/lecturasdeldia/`: motor de cálculo bajo MIT; ver licencia incluida.

## Instalación

1. En CrossPoint, activa **Settings → Connectivity → Plugins**.
2. Copia `plugin/evangelio-del-dia/` a la carpeta de plugins de tu tarjeta SD.
3. Conecta el X3 a Wi-Fi para actualizar el catálogo.

La compatibilidad exacta del manifiesto `device.json` debe confirmarse con el esquema de plugins de la compilación concreta de CrossPoint Stable 2.0.0; no se ha probado en hardware X3 desde este entorno.

## Créditos y licencias

- Motor litúrgico: [zeanuri/lecturasdeldia](https://github.com/zeanuri/lecturasdeldia), licencia MIT; cambios locales en el adaptador.
- Calendario y textos litúrgicos: CEE y titulares correspondientes, sujetos a sus condiciones.
- Este proyecto no está afiliado a la CEE ni a lecturasdeldia.org.
- Código original/adaptador de este repositorio: MIT.

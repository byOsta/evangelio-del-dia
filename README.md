# Lecturas del Día — CrossPoint / Xteink X3

Plugin nativo para CrossPoint Stable 2.0.0. No utiliza navegador integrado, interfaz web propia ni JavaScript ejecutado en el lector.

## Qué hace esta versión

- Publica un índice JSON diario con la fecha y metadatos mínimos.
- Mantiene como referencia el calendario litúrgico de la Conferencia Episcopal Española (CEE).
- Enlaza a la fuente original para consultar las lecturas y sus citas.
- No copia, genera ni distribuye EPUBs con textos bíblicos o del Leccionario protegidos.

**Importante:** el texto íntegro de las lecturas oficiales de la CEE no se considera libre de redistribución por el hecho de estar disponible en una web. La licencia MIT de este repositorio cubre únicamente nuestro código. No cubre textos, traducciones ni datos de terceros.

## Estructura

- `plugin/evangelio-del-dia/device.json`: manifiesto declarativo para el catálogo nativo.
- `catalog/index.json`: índice público consultado por el X3.
- `scripts/generar_catalogo.py`: genera metadatos sin copiar contenido protegido.
- `.github/workflows/generar.yml`: actualiza el índice diariamente a las 00:01, hora de Madrid.

## Instalación

1. En CrossPoint, activa **Settings → Connectivity → Plugins**.
2. Copia `plugin/evangelio-del-dia/` a `/.crosspoint/plugins/evangelio-del-dia/` en la tarjeta SD (o a la carpeta de plugins que admita tu instalación).
3. Conecta el X3 a Wi-Fi y abre el catálogo desde **Home → Plugins**.

El índice requiere conexión para actualizarse. Esta versión no descarga lecturas completas para uso sin conexión, porque no tenemos autorización para redistribuir esos textos.

## Fuente y derechos

- Calendario y lecturas: [lecturasdeldia.org](https://lecturasdeldia.org/), que identifica los textos litúrgicos como propiedad de la CEE.
- Código de este proyecto: MIT.
- Textos litúrgicos, traducciones bíblicas y demás contenido de terceros: conservan sus propias condiciones y no quedan cubiertos por la licencia MIT de este repositorio.

El proyecto no está afiliado a la CEE ni a lecturasdeldia.org.

## Automatización

GitHub Actions actualiza el índice a las 00:01 en la zona horaria `Europe/Madrid`. GitHub puede retrasar las ejecuciones programadas; la hora no es una garantía exacta.

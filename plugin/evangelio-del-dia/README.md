EVANGELIO DEL DÍA — CROSSPOINT

Este plugin nativo muestra un catálogo diario y descarga EPUBs a la tarjeta SD.
Los EPUBs generados actualmente contienen Lorem ipsum ficticio, claramente
marcado como contenido de prueba. No son lecturas bíblicas ni litúrgicas reales.

Instalación:
1. Copia la carpeta evangelio-del-dia a /.crosspoint/plugins/ en la SD.
2. Activa Settings > Connectivity > Plugins.
3. Abre Home > Plugins > Evangelio del Día.
4. Selecciona una fecha y confirma la descarga. El EPUB se guarda en
   /Evangelio del Día/ para lectura offline.

El catálogo ofrece hoy y los 30 días anteriores. Requiere Wi-Fi para consultar
el catálogo y descargar; una vez descargado, el EPUB se lee sin conexión.

Cuando se obtenga autorización, configura CEE_LECTIONARY_PATH en GitHub Actions
con el JSON autorizado del Leccionario. El adaptador usa lookup_readings() del
motor litúrgico y el generador incorpora los textos recibidos al EPUB.
No subas el fichero protegido al repositorio público.

# convert-image-svg

Script en Python para convertir archivos XML o SVG a PNG usando Inkscape desde la linea de comandos.

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

## Versionado

Este proyecto sigue Semantic Versioning (`SemVer`) y mantiene el historial de cambios en `CHANGELOG.md`.

Formato de versiones:

- `vMAJOR.MINOR.PATCH`
- Ejemplo: `v1.0.0`

Reglas de incremento:

- `PATCH` como `v1.0.1`: correcciones de errores, ajustes menores y cambios internos sin impacto en el uso esperado del script.
- `MINOR` como `v1.1.0`: nuevas funcionalidades compatibles hacia atras, nuevas opciones de linea de comandos o mejoras de uso sin romper comandos existentes.
- `MAJOR` como `v2.0.0`: cambios incompatibles, eliminacion o renombre de parametros, cambios en comportamiento por defecto o cualquier ajuste que obligue a adaptar automatizaciones existentes.

Buenas practicas adoptadas:

- Crear una tag Git por cada version publicada.
- Publicar un GitHub Release por cada tag estable.
- Registrar los cambios en `CHANGELOG.md` antes de crear la release.
- Usar una seccion `Unreleased` para preparar cambios futuros antes de etiquetar una nueva version.

Guia rapida para proximas versiones:

- `v1.0.1` para fixes de conversion, deteccion de Inkscape o errores menores de documentacion.
- `v1.1.0` para nuevas opciones como formatos extra, parametros nuevos o mejoras funcionales compatibles.
- `v2.0.0` solo si se rompe compatibilidad con el comportamiento actual.

## Requisitos

- Python 3.10 o superior
- Inkscape instalado y disponible en el PATH, o en `C:\Program Files\Inkscape\bin\inkscape.exe`
- Pillow (`pip install pillow`) si vas a usar `--center`

## Instalacion de Inkscape

En Windows:

1. Instala Inkscape desde su sitio oficial.
2. Si el comando `inkscape` no funciona desde la terminal, verifica que exista `C:\Program Files\Inkscape\bin\inkscape.exe`.
3. Si lo instalaste en otra ruta, agrega esa carpeta al `PATH` o adapta el script.

## Uso

```bash
python convert-image-svg-to-png.py [ruta_entrada] [-o carpeta_salida] [--width N] [--height N] [--dpi N] [--transparent-bg] [--center] [--remove-solid-bg] [--bg-tolerance N]
```

Si no se indica una ruta, el script procesa la carpeta actual y convierte todos los archivos `.xml` y `.svg` que encuentre.

## Ejemplos

Convertir un solo archivo:

```bash
python convert-image-svg-to-png.py ejemplo_logo.xml
```

Convertir todos los `.xml` y `.svg` de la carpeta actual:

```bash
python convert-image-svg-to-png.py
```

Guardar la salida en otra carpeta:

```bash
python convert-image-svg-to-png.py . -o salida
```

Exportar con ancho especifico:

```bash
python convert-image-svg-to-png.py ejemplo_logo.xml --width 1200
```

Resultado esperado:

```text
ejemplo_logo_1200w.png
```

Exportar con ancho, alto y DPI:

```bash
python convert-image-svg-to-png.py ejemplo_logo.xml --width 120 --height 120 --dpi 200
```

Resultado esperado:

```text
ejemplo_logo_120x120_200dpi.png
```

Exportar con fondo transparente:

```bash
python convert-image-svg-to-png.py ejemplo_logo.xml --transparent-bg
```

Exportar centrando el dibujo en un lienzo 512x512 (fondo transparente):

```bash
python convert-image-svg-to-png.py ejemplo_logo.xml --width 512 --height 512 --center --transparent-bg
```

Resultado esperado:

```text
ejemplo_logo_512x512.png
```

Eliminar fondo solido detectado en los bordes:

```bash
python convert-image-svg-to-png.py ejemplo_logo.xml --remove-solid-bg
```

Eliminar fondo solido con tolerancia personalizada:

```bash
python convert-image-svg-to-png.py ejemplo_logo.xml --remove-solid-bg --bg-tolerance 24
```

Exportar con resolucion DPI:

```bash
python convert-image-svg-to-png.py ejemplo_logo.xml --dpi 300
```

Resultado esperado:

```text
ejemplo_logo_300dpi.png
```

## Notas

- El script genera archivos PNG con el mismo nombre base que el archivo de entrada.
- Si defines `--width`, `--height` o `--dpi`, esos valores se agregan al nombre del archivo generado.
- Si defines ancho y alto a la vez, el nombre usa el formato `ANCHOxALTO`, por ejemplo `ejemplo_logo_120x120_200dpi.png`.
- `--transparent-bg` exporta el PNG con transparencia en el fondo de pagina.
- `--center` centra el dibujo en un lienzo de salida y requiere definir `--width` y `--height`.
- `--remove-solid-bg` elimina un fondo de color solido conectado a los bordes del PNG.
- `--bg-tolerance` ajusta que tan estricto es el detector de fondo (0 a 255, por defecto 16).
- Si se indica una carpeta como entrada, se procesan todos los archivos `.xml` y `.svg` dentro de esa carpeta.
- Los archivos de imagen y recursos fuente estan excluidos del repositorio publico mediante `.gitignore`.
- En modo `--center`, el script crea archivos temporales ocultos (`.center.tmp.png`, `.bgclean.tmp.png`) y los elimina al finalizar; el PNG final no se elimina.
# convert-image-svg

Script en Python para convertir archivos XML o SVG a PNG usando Inkscape desde la linea de comandos.

## Requisitos

- Python 3.10 o superior
- Inkscape instalado y disponible en el PATH, o en `C:\Program Files\Inkscape\bin\inkscape.exe`

## Uso

```bash
python convert-image-svg-to-png.py [ruta_entrada] [-o carpeta_salida] [--width N] [--height N] [--dpi N]
```

Si no se indica una ruta, el script procesa la carpeta actual y convierte todos los archivos `.xml` y `.svg` que encuentre.
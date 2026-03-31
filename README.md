# convert-image-svg

Script en Python para convertir archivos XML o SVG a PNG usando Inkscape desde la linea de comandos.

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

## Requisitos

- Python 3.10 o superior
- Inkscape instalado y disponible en el PATH, o en `C:\Program Files\Inkscape\bin\inkscape.exe`

## Instalacion de Inkscape

En Windows:

1. Instala Inkscape desde su sitio oficial.
2. Si el comando `inkscape` no funciona desde la terminal, verifica que exista `C:\Program Files\Inkscape\bin\inkscape.exe`.
3. Si lo instalaste en otra ruta, agrega esa carpeta al `PATH` o adapta el script.

## Uso

```bash
python convert-image-svg-to-png.py [ruta_entrada] [-o carpeta_salida] [--width N] [--height N] [--dpi N]
```

Si no se indica una ruta, el script procesa la carpeta actual y convierte todos los archivos `.xml` y `.svg` que encuentre.

## Ejemplos

Convertir un solo archivo:

```bash
python convert-image-svg-to-png.py logo_tuno_libre_white.xml
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
python convert-image-svg-to-png.py logo_main.xml --width 1200
```

Exportar con resolucion DPI:

```bash
python convert-image-svg-to-png.py logo_main.xml --dpi 300
```

## Notas

- El script genera archivos PNG con el mismo nombre base que el archivo de entrada.
- Si se indica una carpeta como entrada, se procesan todos los archivos `.xml` y `.svg` dentro de esa carpeta.
- Los archivos de imagen y recursos fuente estan excluidos del repositorio publico mediante `.gitignore`.
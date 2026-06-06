# Changelog

Todos los cambios importantes de este proyecto se documentan en este archivo.

Este archivo sigue el enfoque de Keep a Changelog y las versiones publicadas usan Semantic Versioning.

## [Unreleased]

### Changed

- El nombre del PNG generado ahora incluye ancho, alto y DPI cuando esos parametros se definen.
- Se agregaron las opciones `--transparent-bg` y `--center` para exportar con fondo transparente y centrar el dibujo en un lienzo PNG.
- La salida del script ahora muestra la ruta completa del PNG generado para facilitar su ubicacion.

### Added

- Soporte opcional de Pillow para centrar la imagen en una salida con ancho y alto fijos (`--center`).
- Nuevas opciones `--remove-solid-bg` y `--bg-tolerance` para remover fondo solido detectado en los bordes del PNG exportado.

## [v1.0.0] - 2026-03-31

### Added

- Script en Python para convertir archivos XML o SVG a PNG usando Inkscape.
- Deteccion de Inkscape desde el `PATH` o desde la ruta por defecto en Windows.
- Opciones de exportacion para `--width`, `--height` y `--dpi`.
- Soporte para procesar un archivo individual o todos los `.xml` y `.svg` de una carpeta.
- README con requisitos, instalacion y ejemplos de uso.
- Licencia MIT para distribucion publica.

### Changed

- Se limpiaron los ejemplos y textos publicos para usar nombres genericos en la documentacion.
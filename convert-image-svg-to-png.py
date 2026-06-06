from __future__ import annotations

import argparse
from collections import deque
import shutil
import subprocess
from pathlib import Path


def center_png_on_canvas(source_png: Path, target_png: Path, canvas_width: int, canvas_height: int) -> None:
	try:
		from PIL import Image
	except ImportError as exc:
		raise SystemExit(
			"Para usar --center, instala Pillow: pip install pillow"
		) from exc

	with Image.open(source_png).convert("RGBA") as image:
		working = image
		if working.width > canvas_width or working.height > canvas_height:
			ratio = min(canvas_width / working.width, canvas_height / working.height)
			new_size = (
				max(1, int(working.width * ratio)),
				max(1, int(working.height * ratio)),
			)
			working = working.resize(new_size, Image.Resampling.LANCZOS)

		canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
		offset = (
			(canvas_width - working.width) // 2,
			(canvas_height - working.height) // 2,
		)
		canvas.paste(working, offset, working)
		canvas.save(target_png)


def remove_solid_background(source_png: Path, target_png: Path, tolerance: int) -> None:
	try:
		from PIL import Image
	except ImportError as exc:
		raise SystemExit(
			"Para usar --remove-solid-bg, instala Pillow: pip install pillow"
		) from exc

	with Image.open(source_png).convert("RGBA") as image:
		width, height = image.size
		pixels = image.load()

		if width == 0 or height == 0:
			image.save(target_png)
			return

		corners = [
			pixels[0, 0],
			pixels[width - 1, 0],
			pixels[0, height - 1],
			pixels[width - 1, height - 1],
		]
		background = max(corners, key=corners.count)

		def is_match(color: tuple[int, int, int, int], base: tuple[int, int, int, int]) -> bool:
			return (
				abs(color[0] - base[0]) <= tolerance
				and abs(color[1] - base[1]) <= tolerance
				and abs(color[2] - base[2]) <= tolerance
				and color[3] > 0
			)

		visited = bytearray(width * height)
		queue: deque[tuple[int, int]] = deque()

		for x in range(width):
			queue.append((x, 0))
			if height > 1:
				queue.append((x, height - 1))
		for y in range(height):
			queue.append((0, y))
			if width > 1:
				queue.append((width - 1, y))

		while queue:
			x, y = queue.popleft()
			idx = y * width + x
			if visited[idx]:
				continue
			visited[idx] = 1

			current = pixels[x, y]
			if not is_match(current, background):
				continue

			pixels[x, y] = (current[0], current[1], current[2], 0)

			if x > 0:
				queue.append((x - 1, y))
			if x + 1 < width:
				queue.append((x + 1, y))
			if y > 0:
				queue.append((x, y - 1))
			if y + 1 < height:
				queue.append((x, y + 1))

		image.save(target_png)


def build_output_stem(
	input_path: Path,
	width: int | None,
	height: int | None,
	dpi: int | None,
) -> str:
	parts = [input_path.stem]

	if width and height:
		parts.append(f"{width}x{height}")
	elif width:
		parts.append(f"{width}w")
	elif height:
		parts.append(f"{height}h")

	if dpi:
		parts.append(f"{dpi}dpi")

	return "_".join(parts)


def convert_svg_in_xml(
	input_path: Path,
	output_path: Path,
	width: int | None,
	height: int | None,
	dpi: int | None,
	transparent_bg: bool,
	center: bool,
	remove_solid_bg: bool,
	bg_tolerance: int,
) -> None:
	inkscape = shutil.which("inkscape")
	if not inkscape:
		fallback = Path(r"C:\Program Files\Inkscape\bin\inkscape.exe")
		if fallback.exists():
			inkscape = str(fallback)
		else:
			raise SystemExit(
				"No se encontro Inkscape en el PATH ni en C:\\Program Files\\Inkscape\\bin."
			)

	cmd = [
		inkscape,
		str(input_path),
		"--export-type=png",
		f"--export-filename={output_path}",
	]
	if center:
		cmd.append("--export-area-drawing")
	if width and not center:
		cmd.append(f"--export-width={width}")
	if height and not center:
		cmd.append(f"--export-height={height}")
	if dpi:
		cmd.append(f"--export-dpi={dpi}")
	if transparent_bg:
		cmd.append("--export-background-opacity=0")

	if center:
		temp_output = output_path.with_name(f".{output_path.stem}.center.tmp.png")
		cleanup_paths = [temp_output]
		cmd = [
			part if not part.startswith("--export-filename=") else f"--export-filename={temp_output}"
			for part in cmd
		]
		subprocess.run(cmd, check=True)
		working_source = temp_output

		if remove_solid_bg:
			bg_clean_output = output_path.with_name(f".{output_path.stem}.bgclean.tmp.png")
			remove_solid_background(working_source, bg_clean_output, bg_tolerance)
			cleanup_paths.append(bg_clean_output)
			working_source = bg_clean_output

		center_png_on_canvas(working_source, output_path, width, height)
		for temp_path in cleanup_paths:
			temp_path.unlink(missing_ok=True)
		return

	subprocess.run(cmd, check=True)
	if remove_solid_bg:
		remove_solid_background(output_path, output_path, bg_tolerance)


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Convierte XML con SVG embebido a PNG.",
	)
	parser.add_argument(
		"input",
		nargs="?",
		default=".",
		help="Archivo XML/SVG o carpeta (por defecto, la carpeta actual).",
	)
	parser.add_argument(
		"-o",
		"--output",
		default=None,
		help="Carpeta de salida (por defecto, la misma del archivo).",
	)
	parser.add_argument(
		"--width",
		type=int,
		default=None,
		help="Ancho de salida en px (opcional).",
	)
	parser.add_argument(
		"--height",
		type=int,
		default=None,
		help="Alto de salida en px (opcional).",
	)
	parser.add_argument(
		"--dpi",
		type=int,
		default=None,
		help="Resolucion de salida en DPI (opcional).",
	)
	parser.add_argument(
		"--transparent-bg",
		action="store_true",
		help="Exporta PNG con fondo transparente.",
	)
	parser.add_argument(
		"--center",
		action="store_true",
		help="Centra el dibujo en un lienzo PNG del tamano --width x --height.",
	)
	parser.add_argument(
		"--remove-solid-bg",
		action="store_true",
		help="Elimina fondo solido detectado en los bordes del PNG.",
	)
	parser.add_argument(
		"--bg-tolerance",
		type=int,
		default=16,
		help="Tolerancia (0-255) para detectar fondo solido al usar --remove-solid-bg.",
	)
	args = parser.parse_args()

	if args.center and (args.width is None or args.height is None):
		raise SystemExit("--center requiere definir --width y --height.")
	if args.bg_tolerance < 0 or args.bg_tolerance > 255:
		raise SystemExit("--bg-tolerance debe estar entre 0 y 255.")

	input_path = Path(args.input).resolve()
	output_dir = Path(args.output).resolve() if args.output else None

	if input_path.is_dir():
		candidates = sorted(
			[
				*input_path.glob("*.xml"),
				*input_path.glob("*.svg"),
			]
		)
		if not candidates:
			raise SystemExit("No se encontraron archivos .xml o .svg en la carpeta.")
	else:
		candidates = [input_path]

	for xml_path in candidates:
		out_dir = output_dir or xml_path.parent
		out_stem = build_output_stem(xml_path, args.width, args.height, args.dpi)
		out_path = out_dir / f"{out_stem}.png"
		convert_svg_in_xml(
			xml_path,
			out_path,
			args.width,
			args.height,
			args.dpi,
			args.transparent_bg,
			args.center,
			args.remove_solid_bg,
			args.bg_tolerance,
		)
		print(f"OK: {xml_path.name} -> {out_path}")


if __name__ == "__main__":
	main()
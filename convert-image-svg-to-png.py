from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


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
	if width:
		cmd.append(f"--export-width={width}")
	if height:
		cmd.append(f"--export-height={height}")
	if dpi:
		cmd.append(f"--export-dpi={dpi}")
	subprocess.run(cmd, check=True)


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
	args = parser.parse_args()

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
		convert_svg_in_xml(xml_path, out_path, args.width, args.height, args.dpi)
		print(f"OK: {xml_path.name} -> {out_path.name}")


if __name__ == "__main__":
	main()
from os import path
from struct import pack
from sys import argv
from thumpie2obj import Vertex, TextureCoordinate, Face, Model
from typing import BinaryIO

def write_int(fp: BinaryIO, val: int) -> int:
	return fp.write(pack('<I', val))


def write_float(fp: BinaryIO, val: float) -> float:
	return fp.write(pack('<f', val))


def write_str(fp: BinaryIO, val: str) -> int:
	bytes_written: int = 0
	str_len: int = len(val)

	bytes_written += write_int(fp, str_len + 1)  # null terminator, even bbb does this
	bytes_written += fp.write(val.encode('ascii'))

	fp.seek(4 - (str_len % 4), 1)

	return bytes_written


def convert_obj(in_file: str, texture_name: str) -> None:
	models: list[Model] = []

	with open(in_file, 'r') as fp:
		vertexes: list[Vertex] = []
		texture_coords: list[TextureCoordinate] = []
		faces: list[Face] = []

		line: str
		for line in fp.readlines():
			mode: str; vals: list[str]
			mode, *vals = line.split(' ')

			match mode:
				case 'v':
					if len(vals) < 3:
						break

					vertexes.append(Vertex(
						float(vals[0]) / 75.0,
						float(vals[1]) / 75.0,
						float(vals[2]) / 75.0
					))
				case 'vt':
					if len(vals) < 2:
						break

					texture_coords.append(TextureCoordinate(
						float(vals[0]),
						float(vals[1]),
					))
				case 'f':
					if len(vals) < 3:
						break

					faces.append(Face(
						int(vals[0].split('/')[0]) - 1,
						int(vals[1].split('/')[0]) - 1,
						int(vals[2].split('/')[0]) - 1
					))

		models.append(Model(
			texture_name,
			vertexes,
			texture_coords,
			faces
		))

	with open(path.splitext(in_file)[0] + '.bin', 'wb') as fp:
		write_int(fp, len(models))

		model: Model
		for model in models:
			write_str(fp, model.texture)
			write_int(fp, 1)

			if len(model.vertexes) < len(model.texture_coords):
				raise Exception('more texture coordinates than vertexes')

			write_int(fp, len(model.vertexes))
			vertex: Vertex; texture_coord: TextureCoordinate
			for vertex, texture_coord in zip(model.vertexes, model.texture_coords):
				write_float(fp, vertex.x)
				write_float(fp, vertex.y)
				write_float(fp, vertex.z)
				write_float(fp, texture_coord.u)
				write_float(fp, texture_coord.v)
				write_int(fp, 0x00FFFFFF)  # reversed because endianness, also no colour 😈

			write_int(fp, len(model.faces))
			face: Face
			for face in model.faces:
				write_int(fp, face.v1)
				write_int(fp, face.v2)
				write_int(fp, face.v3)

		write_int(fp, 0)


def main() -> None:
	if len(argv) < 3:
		print(f'usage: {argv[0]} <in_file.obj> texture/name/and/path.png')
		return

	in_file: str = argv[1]
	texture: str = argv[2]

	if not path.exists(in_file):
		print(f'error: {in_file} does not exist')
		return

	convert_obj(in_file, texture)


if __name__ == '__main__':
	main()

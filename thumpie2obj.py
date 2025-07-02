from dataclasses import dataclass
from os import path
from struct import unpack
from sys import argv
from typing import BinaryIO
import os


@dataclass
class Vertex:
	x: float
	y: float
	z: float


@dataclass
class TextureCoordinate:
	u: float
	v: float


@dataclass
class Face:
	v1: int
	v2: int
	v3: int


@dataclass
class Model:
	texture: str
	vertexes: list[Vertex]
	texture_coords: list[TextureCoordinate]
	faces: list[Face]


def read_byte(fp: BinaryIO) -> int:
	return unpack('<B', fp.read(1))[0]


def read_int(fp: BinaryIO) -> int:
	return unpack('<I', fp.read(4))[0]


def read_float(fp: BinaryIO) -> float:
	return unpack('<f', fp.read(4))[0]


def read_str(fp: BinaryIO) -> str:
	str_len: int = read_int(fp) - 1  # null terminator, even bbb does this
	str_bytes: bytes = fp.read(str_len)
	fp.seek(4 - (str_len % 4), 1)
	return str_bytes.decode('ascii')


def read_vertex(fp: BinaryIO) -> Vertex:
	return Vertex(read_float(fp) * 75.0, read_float(fp) * 75.0, read_float(fp) * 75.0)


def read_texture_coords(fp: BinaryIO) -> TextureCoordinate:
	return TextureCoordinate(read_float(fp), read_float(fp))


def read_face(fp: BinaryIO) -> Face:
	return Face(read_int(fp) + 1, read_int(fp) + 1, read_int(fp) + 1)


def convert_thumpie(in_file: str) -> None:
	models: list[Model] = []

	with open(in_file, 'rb') as fp:
		for _ in range(read_int(fp)):
			texture: str = read_str(fp)
			fp.seek(4, 1)  # idk what this one is

			vertexes: list[Vertex] = []
			texture_coords: list[TextureCoordinate] = []
			faces: list[Face] = []

			for _ in range(read_int(fp)):
				vertexes.append(read_vertex(fp))
				texture_coords.append(read_texture_coords(fp))
				fp.seek(4, 1)  # we don't need colour, right?

			for _ in range(read_int(fp)):
				faces.append(read_face(fp))

			models.append(Model(texture, vertexes, texture_coords, faces))

	out_folder: str = path.splitext(in_file)[0]
	if not path.exists(out_folder):
		os.makedirs(out_folder, exist_ok=True)

	i: int; model: Model
	for i, model in enumerate(models):
		# suck it up buttercup this is life, and it hits hard,
		# there's no time to complain about filenames
		out_file: str = path.join(out_folder, f'{i}.obj')

		with open(out_file, 'w') as fp:
			fp.write(
				f'# Created by https://github.com/iestyn129/Thumpie2Obj\n'
				f'# The texture intended for use here is "{model.texture}"\n'
			)

			fp.write('\n# Vertexes\n')
			vertex: Vertex
			for vertex in model.vertexes:
				fp.write(f'v {vertex.x} {vertex.y} {vertex.z}\n')

			fp.write('\n# Texture Coordinates\n')
			texture_coord: TextureCoordinate
			for texture_coord in model.texture_coords:
				fp.write(f'vt {texture_coord.u} {texture_coord.v}\n')

			fp.write('\n# Faces\n')
			face: Face
			for face in model.faces:
				# texture coordinates are grouped with vertexes so this would always work,
				# since the number of vertexes will be the same as the number of coords
				fp.write(f'f {face.v1}/{face.v1} {face.v2}/{face.v2} {face.v3}/{face.v3}\n')


def main() -> None:
	if len(argv) < 2:
		print(f'usage: {argv[0]} <in_file.bin>')
		return

	in_file: str = argv[1]

	if not path.exists(in_file):
		print(f'error: {in_file} does not exist')
		return

	convert_thumpie(in_file)


if __name__ == '__main__':
	main()

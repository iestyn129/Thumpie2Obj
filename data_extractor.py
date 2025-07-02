from os import path
from shutil import rmtree
from sys import argv
from zipfile import ZipFile
import os


def extract_data(in_file: str) -> None:
	out_dir: str = path.splitext(in_file)[0]

	if path.exists(out_dir):
		rmtree(out_dir)

	os.makedirs(out_dir)

	ZipFile(in_file).extractall(out_dir)


def compress_data(in_dir: str) -> None:
	with ZipFile(f'{in_dir}.bin', 'w') as zf:
		for root, dirs, files in os.walk(in_dir):
			for file in files:
				file_path: str = path.join(root, file)
				rel_file_path: str = path.relpath(file_path, in_dir)
				zf.write(file_path, rel_file_path)


def main() -> None:
	if len(argv) < 3:
		print(f'usage: {argv[0]} (d[code]|e[ncode]) (<in_dir>|<in_file.bin>)')
		return

	mode: str = argv[1][0]
	in_path: str = argv[2]

	if not path.exists(in_path):
		print(f'error: {in_path} does not exist')
		return

	match mode.lower():
		case 'd':
			extract_data(in_path)
		case 'e':
			compress_data(in_path)


if __name__ == '__main__':
	main()

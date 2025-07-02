# Thumpie2Obj
A quick and dirty tool for convert the models from the hit 2010 game Thumpies by Big Blue Bubble to Wavefront OBJ (`.obj`) files.

<img src="images/blender example.png" alt="example image of extracted models in blender">

## Usage
For extracting models, run:
```shell
python thumpie2obj.py <models.bin>
```
With `<models.bin>` replaced by actual models file you wish to convert (i.e. noobie01.bin).

For encoding models, run:
```shell
python obj2thumpie.py <in_file.obj> <texture/name/and/path.png>
```
With `<in_file.obj>` replaced by your Wavefront OBJ (`.obj`), and `<texture/name/and/path.png>` with the path to the texture the game will use.
(`noobie01.obj game/data/images/textures/models/balls/noobie_bigger01`)

For extracting and compressing the games assets, run:
```shell
python data_extractor.py (d[code]|e[ncode]) (<in_dir>|<in_file.bin>)
```
With `(d[code]|e[ncode])` replaced by the action you wish to do (i.e. `d` or `decode` for extracting, and `e` or `encode` for compressing).
and `(<in_dir>|<in_file.bin>)` with either the `data.bin` from the data or the folder containing the extracted assets.
## Note
If you notice any issues or inconsistencies with the models this program makes open an issue.
I did not make this to accurately extract models, but only to see if I could, so I did skip things.
## Disclaimer
>This project is an unofficial program designed for use with Thumpies (2010) files.
>All trademarks, logos, and copyrighted materials are the property of their respective owners.
>This tool is not affiliated with, endorsed by, or sponsored by Big Blue bubble.
>Use of this tool is at your own risk. Please respect the terms of service and other agreements of the original game.

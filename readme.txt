Most code is based on: https://github.com/LaMuerteDeLaPassion/Wildstar-Export
Used code from various other sources. Credit is given in the source files.


installed using:
	python -m venv .venv
	. .\.venv\Scripts\activate

	pip3 install numpy
	pip3 install scipy
	pip install pygltflib
	pip install pyrender
	pip install dearpygui
	pip install pyinstaller


activate venv using
	. .\.venv\Scripts\activate



TODO:
	Cleanup m3_to_gltf.py and make the code easier to read.
	Clean up the samplers and buffers that make up the GLTF format and make the logic easier to follow. Maybe use a class for this.
	Tangents and Normals most likely still incorrectly calculated. see implementations and check with W* values.
	finish the gui mass export
	improve efficiency of tex_to_png.py because it is way too slow.
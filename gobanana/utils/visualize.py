"""Methods for visualizing gobanana levels as images"""

import sys
import os
import glob
from PIL import Image
from gobanana.game.tiles import Tiles

def create_visualization(levelname, leveldirectory, spritesdirectory):
	"""
	Visualizes GoBanana levels converted using the rules in tiles.py

	levelname (str): the name of the level file within its directory, excluding the .txt extension
	leveldirectory (str): the directory containing the level, relative to the launching location
	spritesdirectory (str): the directory containing the sprites, relative to the launching location
	"""
	#Load sprites
	sprites = {}
	for filename in glob.glob(f"{spritesdirectory}/**/*.png", recursive=True):
		im = Image.open(filename)
		name = filename.split("/")[-1][:-4]
		sprites[name] = im.convert("RGBA")

	level = {}
	with open(f"{leveldirectory}/{levelname}.txt") as fp:
		for y, line in enumerate(fp):
			level[y] = line[:-1]
			print(f"{y}:")
			print(line)

	maxX = len(level[0])
	maxY = y+1
	print(f"Max y is {y}")



	#Create backdrop of tiled plains sprites to which to write actual sprites
	def createTiledPlainsImage():
		image = Image.new("RGB", (maxX*16, (maxY)*16), color=(91, 153, 254))
		pixels = image.load()

		imageToUse = sprites[Tiles.FLOOR.spritename]
		pixelsToUse = imageToUse.load()
		for y in range(0, maxY):
			for x in range(0, maxX):
				for x2 in range(0, 16):
					for y2 in range(0, 16):
						pixels[x*16+x2,y*16+y2] = pixelsToUse[x2,y2][:-1]
		return image, pixels

	image, pixels = createTiledPlainsImage()

	#Draw the actual building/terrain sprites to the image
	for y in range(0, maxY):
		for x in range(0, maxX):
			imageToUse = None
			print(y)
			print(maxY)
			print(levelname)
			print(f"{x}, {y}")
			if level[y][x] in Tiles.reverse_character_lookup.keys():
				print(Tiles.reverse_character_lookup[level[y][x]])
				imageToUse = sprites[Tiles.reverse_character_lookup[level[y][x]].spritename]
			if not imageToUse == None:
				pixelsToUse = imageToUse.load()
				x2max = imageToUse.size[0]
				y2max = imageToUse.size[1]
				for x2 in range(0, x2max):
					for y2 in range(0, y2max):
						if pixelsToUse[x2,y2][3]>0:
							upwardoffset = y2max-16
							ywritepixel = y*16+y2-upwardoffset if y*16+y2-upwardoffset>=0 else y*16+y2
							#print(ywritepixel)
							#ywritepixel=y*16+y2
							pixels[x*16+x2,ywritepixel] = pixelsToUse[x2,y2][:-1]

	#save the resulting level image
	absleveldir = os.path.abspath(f"{leveldirectory}")
	print(leveldirectory)
	print(absleveldir)
	image.save(rf"{absleveldir}/{levelname}.png","PNG")

if __name__ == "__main__":
	leveldirectory = "./gobanana/assets/levels"
	spritesdirectory = "./gobanana/assets"
	#create_visualization("battle-of-thermopylae", leveldirectory, spritesdirectory)
	for levelfile in glob.glob(f"{leveldirectory}/*.txt"):
		levelname = os.path.basename(levelfile)[:-4]
		print(levelname)
		create_visualization(levelname, leveldirectory, spritesdirectory)

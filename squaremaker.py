# author: fatcat2

import argparse
import os

from wand.color import Color
from wand.image import Image

FILE_EXTENSIONS = ["jpg", "HEIC"]

def processOutputDirectory(path, filename):
    filename = os.path.basename(filename)
    if os.path.isdir(path):
        return f"{path}/{filename}-square.jpg"
    else:
        return path

def resizeImage(filename, file_format="jpg", output_dir=None):
    image = Image(filename=filename)
    image = image.clone()

    if output_dir:
        output_dir = processOutputDirectory(output_dir, filename)

    with Color('white') as color:
        image.transform(resize="2000x2000>")
        image.gravity = 'center'
        image.extent(width=2200, height=2200, gravity="center")
        image.crop(width=2200, height=2200)
        image.background_color = color
        image.merge_layers("flatten")

    save_path = output_dir if output_dir else f"{filename}-square.{file_format}"

    image.save(filename=save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make your images into nice looking squares.")
    parser.add_argument("path", help="Path to the image or directory you want to convert into squares.")
    parser.add_argument("--output", "-o", help="Specify a directory to output the file to.")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        for filename in os.listdir(args.path):
            if filename.split(".")[1] in FILE_EXTENSIONS:
                resizeImage(f"{args.path}/{filename}", output_dir=args.output)
    else:
        resizeImage(args.path, output_dir=args.output)


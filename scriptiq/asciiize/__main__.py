import argparse
import os
import sys

from PIL import Image
import numpy as np


def convert(dapic, outfile):
    im = Image.open(dapic)
    min, max, delta = 255, 0, 0
    im = im.resize((70, int((im.size[1] / im.size[0]) * 70)))
    basem = np.empty((im.size[0], im.size[1]))
    basem2 = np.full((im.size[0], im.size[1]), ' ')
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            basem[i, j] = int((im.getpixel((i, j))[0] + im.getpixel((i, j))[1] + im.getpixel((i, j))[2]) / 3)
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if basem[i, j] > max: max = basem[i, j]
            if basem[i, j] < min: min = basem[i, j]
    delta = abs(max - min)
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if basem[i, j] >= (int(0.95 * (delta)) + min) and basem[i, j] <= max: basem2[i, j] = '#'
            if basem[i, j] >= (int(0.9 * (delta)) + min) and basem[i, j] < (int(0.95 * (delta)) + min): basem2[i, j] = '0'
            if basem[i, j] >= (int(0.85 * (delta)) + min) and basem[i, j] < (int(0.9 * (delta)) + min): basem2[i, j] = '%'
            if basem[i, j] >= (int(0.8 * (delta)) + min) and basem[i, j] < (int(0.85 * (delta)) + min): basem2[i, j] = '?'
            if basem[i, j] >= (int(0.7 * (delta)) + min) and basem[i, j] < (int(0.8 * (delta)) + min): basem2[i, j] = '/'
            if basem[i, j] >= (int(0.6 * (delta)) + min) and basem[i, j] < (int(0.7 * (delta)) + min): basem2[i, j] = '+'
            if basem[i, j] >= (int(0.5 * (delta)) + min) and basem[i, j] < (int(0.6 * (delta)) + min): basem2[i, j] = '='
            if basem[i, j] >= (int(0.4 * (delta)) + min) and basem[i, j] < (int(0.5 * (delta)) + min): basem2[i, j] = '_'
            if basem[i, j] >= (int(0.3 * (delta)) + min) and basem[i, j] < (int(0.4 * (delta)) + min): basem2[i, j] = '-'
            if basem[i, j] >= (int(0.2 * (delta)) + min) and basem[i, j] < (int(0.3 * (delta)) + min): basem2[i, j] = ','
            if basem[i, j] >= (int(0.1 * (delta)) + min) and basem[i, j] < (int(0.2 * (delta)) + min): basem2[i, j] = '.'
            if basem[i, j] < (int(0.1 * (delta)) + min): basem2[i, j] = ' '
    basem2 = basem2.T
    # создаём директорию для результата, если её нет
    out_dir = os.path.dirname(os.path.abspath(outfile))
    os.makedirs(out_dir, exist_ok=True)
    np.savetxt(outfile, basem2, fmt="%s", delimiter=" ")


def main():
    parser = argparse.ArgumentParser(
        prog="asciiize",
        description="Convert an image to ASCII art saved as .txt"
    )
    # позиционные аргументы, но с дефолтами из env — удобно для docker run -e ...
    parser.add_argument(
        "input",
        nargs="?",
        default=os.environ.get("ASCIIIZE_INPUT"),
        help="Path to the input image (or env ASCIIIZE_INPUT)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=os.environ.get("ASCIIIZE_OUTPUT"),
        help="Path to save the resulting .txt (or env ASCIIIZE_OUTPUT)",
    )
    args = parser.parse_args()

    if not args.input:
        parser.error("input image path is required (arg or ASCIIIZE_INPUT)")
    if not args.output:
        parser.error("output path is required (arg or ASCIIIZE_OUTPUT)")

    if not os.path.isfile(args.input):
        print(f"error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        convert(args.input, args.output)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    print("success")


if __name__ == "__main__":
    main()
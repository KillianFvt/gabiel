import os
import re
import sys

from PIL import Image

from ensure_pillow import is_module_installed, install_package


def create_mirrored_image(img):
    """
    Creates a new image with the original image on top and a mirrored version below.

    :param img: Pillow Image object
    """

    # Get image dimensions
    width, height = img.size

    # Create a new image with double the height
    new_image = Image.new(img.mode, (width * 2, height * 2))

    # Paste the original image on top
    new_image.paste(img, (0, 0))

    # Mirror the image and paste it on the bottom
    mirrored_image_bottom_left = img.transpose(Image.FLIP_TOP_BOTTOM)
    new_image.paste(mirrored_image_bottom_left, (0, height))

    mirrored_image_top_right = img.transpose(Image.FLIP_LEFT_RIGHT)
    new_image.paste(mirrored_image_top_right, (width, 0))

    mirrored_image_bottom_right = mirrored_image_top_right.transpose(Image.FLIP_TOP_BOTTOM)
    new_image.paste(mirrored_image_bottom_right, (width, height))

    return new_image


def image_slice_rev(image: Image, slice_amt: int) -> Image:
    """
    Slices the image into `slice_amt` pieces and pastes them in half-reversed order.

    :param image: Pillow Image object
    :param slice_amt: int
    :return: Pillow Image object
    """
    slices = []
    slice_size = image.width // slice_amt
    new_image = Image.new(image.mode, (slice_size * slice_amt, image.height))

    for i in range(slice_amt):
        new_slice = image.crop((i * slice_size, 0, (i + 1) * slice_size, image.height))
        slices.append(new_slice)

    print(f"Slicing done. Pasting...")

    for i in range(slice_amt):
        new_image.paste(slices[0], (i * slice_size, 0))
        slices.pop(0)
        slices.reverse()

    return new_image


def make_gabial(image_path: str, output_path: str, slice_amt: int) -> Image:
    """
    Creates a Gabiel image from the given image file.
    :param image_path: Path to the original image file.
    :param output_path: Path to save the Gabiel image.
    :param slice_amt: Number of slices to make.
    :return: Image object of the Gabiel image.
    """


    print("Opening image...")
    try:
        original_image = Image.open(image_path)
    except FileNotFoundError:
        print(f"File {image_path} not found.")
        sys.exit(1)

    print("Creating mirrored image...")
    mirrored_image = create_mirrored_image(original_image)

    print("First slicing...")
    sliced_image_vert = image_slice_rev(mirrored_image, slice_amt)

    print("Rotating image...")
    sliced_image_horz = sliced_image_vert.rotate(90, expand=1)

    print("Second slicing...")
    sliced_image_horz = image_slice_rev(sliced_image_horz, slice_amt)

    print("Rotating image back...")
    final_image = sliced_image_horz.rotate(-90, expand=1)

    print("Saving and displaying image...")
    final_image.save(output_path)
    final_image.show()

    return final_image


if __name__ == '__main__':

    if not is_module_installed("PIL"):
        print("Pillow is not installed. Installing now...")
        install_package("Pillow")
    else:
        print("Pillow is installed... Proceeding...")

    if len(sys.argv) != 3:
        print("Usage: py gabiel.py [input file] [slice amt]")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"File {input_file} not found.")
    else:

        regex = re.compile('[^a-zA-Z_-]')
        output_file = input_file.split(".")[-2] + "_gabial"
        output_file = regex.sub('', output_file)
        output_file += ".png"

        slice_amt = int(sys.argv[2])

        make_gabial(input_file, output_file, slice_amt)

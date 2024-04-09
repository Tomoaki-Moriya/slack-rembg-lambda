from rembg import remove
from PIL import Image


def remove_background(input_path: str, output_path: str) -> None:
    im = Image.open(input_path)
    output = remove(im)
    output.save(output_path, "PNG")  # type: ignore

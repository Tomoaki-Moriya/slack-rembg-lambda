import os
import tempfile
import uuid
from rembg import remove
from PIL import Image


class ImageService:

    def remove_background(self, input_path: str) -> str:
        with tempfile.TemporaryDirectory() as temp_dir:
            p = os.path.join(temp_dir, str(uuid.uuid4()))
            im = Image.open(input_path)
            output = remove(im)
            output.save(p, "jpg")  # type: ignore
            return output

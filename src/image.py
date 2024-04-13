import os
from typing import Final
from rembg import remove
from PIL import Image
from PIL.Image import Image as PILImage
import onnxruntime as ort
from rembg.session_simple import SimpleSession


class ImageService:

    def __init__(self, u2net_home: str) -> None:
        sess_opts = ort.SessionOptions()
        self.__session: Final = SimpleSession("u2net", ort.InferenceSession(
            u2net_home,
            providers=ort.get_available_providers(),
            sess_options=sess_opts,
        ),
        )

    def remove_background(self, input_path: str) -> str:
        filename = os.path.basename(input_path)
        p = input_path.replace(filename, f"removed_{filename}")
        im = Image.open(input_path)
        output: PILImage = remove(im, session=self.__session)  # type: ignore
        if output.mode != "RGB":
            output = output.convert("RGB")
        output.save(p)
        return p

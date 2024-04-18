import os
from typing import Final
from rembg import remove
from PIL import Image
from PIL.Image import Image as PILImage
import onnxruntime as ort
from rembg.session_simple import SimpleSession


class ImageService:

    def __init__(self, u2net_home: str) -> None:
        """
        u2net.onnxの配置パスを引数に、rembgが使う学習モデルのセッションを作成する。
        rembgが内部で自動でセッションをつくってくれるが、ディレクトリ作成する部分があり、
        Lambdaではエラーが発生するため、事前にセッションを作成しておく。
        """
        sess_opts = ort.SessionOptions()
        self._session: Final = SimpleSession("u2net", ort.InferenceSession(
            u2net_home,
            providers=ort.get_available_providers(),
            sess_options=sess_opts,
        ),
        )

    def remove_background(self, input_path: str) -> str:
        """
        指定された画像パスの背景を除去する
        """
        filename = os.path.basename(input_path)
        p = input_path.replace(filename, f"removed_{filename}")
        im = Image.open(input_path)
        output: PILImage = remove(im, session=self._session)  # type: ignore
        if output.mode != "RGB":
            output = output.convert("RGB")
        output.save(p)
        return p

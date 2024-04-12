import os
import tempfile
from typing import Final, Optional
import requests


class SlackService:

    def __init__(self) -> None:
        self.__verification_token: Final = os.environ["VERIFICATION_TOKEN"]
        self.__api_token: Final = os.environ["API_TOKEN"]

    def auth(self, body: dict) -> Optional[dict[str, str]]:
        if "challenge" not in body:
            return None
        token = body["token"]
        challenge = body["challenge"]
        event_type = body["type"]

        if token == self.__verification_token and event_type == "url_verification":
            return {
                "challenge": challenge
            }

    def download_file(self, file_id: str) -> str:
        url_private_download = self.__get_url_private_download(file_id)
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        file_response = requests.get(
            url_private_download, headers=headers, stream=True)
        if file_response.status_code == 200:
            with tempfile.TemporaryDirectory() as temp_dir:
                download_path = os.path.join(temp_dir, file_id)
                with open(download_path, "wb") as f:
                    for chunk in file_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                return download_path
        else:
            raise ValueError(f"Failed to download file with id {file_id}")

    def upload_file(self, channel_id: str, file_path: str) -> None:
        url = "https://slack.com/api/files.getUploadURLExternal"
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        with open(file_path, 'rb') as f:
            payload = {
                "filename": os.path.basename(file_path),
                "length": os.path.getsize(file_path),
            }
            res = requests.post(url, headers=headers, data=payload)
            if not res.ok:
                raise ValueError(
                    f"Failed to get upload URL for channel {channel_id}")
            res_body = res.json()

            files = {'file': f}
            upload_res = requests.post(
                res_body["upload_url"], headers=headers, files=files)
            if not upload_res.ok:
                raise ValueError(
                    f"Failed to upload file to channel {channel_id}")

            complete_url = "https://slack.com/api/files.completeUploadExternal"
            payload = {
                "files": [
                    {"id": res_body["file_id"],
                        "title": os.path.basename(file_path)}
                ],
                "channel_id": channel_id,
                "initial_comment": "お待たせしました。。。"
            }
            complete_res = requests.post(
                complete_url, headers=headers, json=payload)
            if not complete_res.ok:
                raise ValueError(
                    f"Failed to complete upload for channel {channel_id}")

    def __get_url_private_download(self, file_id: str):
        url = f"https://slack.com/api/files.info"
        send_data = {
            "file": file_id,
            "token": self.__api_token
        }
        res = requests.post(url, send_data)
        if not res.ok:
            raise ValueError(
                f"Failed to get url_private_download for file {file_id}")
        url_private_download = res.json()["file"]["url_private_download"]
        return url_private_download

    def post_message(self, channel_id: str, message: str) -> None:
        url = "https://slack.com/api/chat.postMessage"
        headers = {"Authorization": f"Bearer {self.__api_token}",
                   "Content-type": "application/json"}
        payload = {
            "channel": channel_id,
            "text": message
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise ValueError(f"Failed to post message to channel {channel_id}")

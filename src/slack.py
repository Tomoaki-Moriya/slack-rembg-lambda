import os
from typing import Any, Final, Optional
import uuid
import requests


class SlackService:

    def __init__(self) -> None:
        self.__verification_token: Final = os.environ["VERIFICATION_TOKEN"]
        self.__api_token: Final = os.environ["API_TOKEN"]
        self.__bot_user_id: Final = os.environ["BOT_USER_ID"]

    def auth(self, body: dict) -> Optional[dict[str, Any]]:
        event_type = body.get("type")

        if event_type == "url_verification" and body["token"] == self.__verification_token:
            return {
                "challenge": body["challenge"]
            }

        if body["event"]["user_id"] == self.__bot_user_id:
            return {
                "statusCode": 400
            }

        return None

    def download_file(self, file_id: str, download_dir: str) -> str:
        url_private_download, original_filename = self.__get_url_private_download(
            file_id)
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        file_response = requests.get(
            url_private_download, headers=headers, stream=True)
        if file_response.status_code == 200:
            download_path = os.path.join(
                download_dir, f"{uuid.uuid4()}.{original_filename.split('.')[-1]}")
            with open(download_path, "wb") as f:
                for chunk in file_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                return download_path
        else:
            raise ValueError(f"Failed to download file with id {file_id}")

    def upload_file(self, channel_id: str, file_path: str, message: Optional[str] = None) -> None:
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
            }
            if message:
                payload["initial_comment"] = message
            complete_res = requests.post(
                complete_url, headers=headers, json=payload)
            if not complete_res.ok:
                raise ValueError(
                    f"Failed to complete upload for channel {channel_id}")

    def __get_url_private_download(self, file_id: str) -> tuple[str, str]:
        url = f"https://slack.com/api/files.info"
        send_data = {
            "file": file_id,
            "token": self.__api_token
        }
        res = requests.post(url, send_data)
        if not res.ok:
            raise ValueError(
                f"Failed to get url_private_download for file {file_id}")
        body = res.json()
        url_private_download = body["file"]["url_private_download"]
        name = body["file"]["name"]
        return url_private_download, name

import json
import os
import tempfile
from image import ImageService
from slack import SlackService

slack_service = SlackService()
u2net_home = os.path.join(os.path.dirname(__file__), "u2net.onnx")
image_service = ImageService(u2net_home)


def lambda_handler(event, _):
    if "headers" in event and "x-slack-retry-reason" in event["headers"]:
        return {
            "statusCode": 200
        }

    body = json.loads(event["body"])
    res = slack_service.auth(body)
    if res:
        return res

    file_id = body["event"]["file_id"]
    with tempfile.TemporaryDirectory() as temp_dir:
        download_path = slack_service.download_file(file_id, temp_dir)

        output = image_service.remove_background(download_path)

        channel_id = body["event"]["channel_id"]
        slack_service.upload_file(channel_id, output, "お待たせしました。。。")

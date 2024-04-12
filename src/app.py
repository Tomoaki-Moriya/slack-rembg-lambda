import json
from image import ImageService
from slack import SlackService


def lambda_handler(event, _):
    body = json.loads(event["body"])
    slack_service = SlackService()
    res = slack_service.auth(body)
    if res:
        return res

    file_id = body["event"]["file_id"]
    image = slack_service.download_file(file_id)

    image_service = ImageService()
    output = image_service.remove_background(image)

    channel_id = body["event"]["channel_id"]
    slack_service.upload_file(channel_id, output)

import os
from typing import Optional


verification_token = os.environ['VERIFICATION_TOKEN']


def first_auth(body: dict) -> Optional[dict[str, str]]:
    if "challenge" not in body:
        return None
    token = body["token"]
    challenge = body["challenge"]
    event_type = body["type"]

    if token == verification_token and event_type == "url_verification":
        return {
            "challenge": challenge
        }

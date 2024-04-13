# slack-rembg-lambda

Slack bot to fire rembg with AWS Lambda

# Getting started

## Setup environment

```
pip install -r src/requirements.txt
```

## Download u2net.onnx and put current directory.

```
https://drive.google.com/uc?
```

# Deploy

```

sam build

```

```

sam deploy \
--parameter-overrides VerificationToken=<your_verifiaction_token> ApiToken=<your_bot_user_auth_token> BotUserId=<your_bot_user_id> \
--stack-name slack-rembg-lambda-stack \
--region <your_region> \
--s3-bucket <your_s3_bucket> \
--capabilities CAPABILITY_NAMED_IAM \
--image-repository <your-account_id>.dkr.ecr.<your_region>.amazonaws.com/<your_repository_name> \
--profile <your_profile_name>

```

import boto3
from botocore.config import Config
from common.config import settings
from uuid import uuid4


def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.CLOUDFLARE_R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
        aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )


def generate_r2_image_key(prefix: str) -> str:
    filename = f"{uuid4().hex}.png"
    return f"{prefix}/{filename}"

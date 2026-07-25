import base64
import json
import os
from pathlib import Path
from uuid import uuid4
import requests
from agents.daily_logs_agent.state import Context
from agents.subgraphs.generate_log_image.state import GraphState
from common.utils.r2 import get_r2_client
from langgraph.runtime import Runtime
from common.config import settings


def generate_image(state: GraphState, runtime: Runtime[Context]):

    image_prompt = state["image_prompt"]
    image_url = runtime.context.image_url

    response = requests.post(
        url="https://openrouter.ai/api/v1/images",
        headers={
            "Authorization": f"Bearer {settings.DATABASE_URL}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": "openai/gpt-image-2",
                "prompt": image_prompt,
                "input_references": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    }
                ],
            }
        ),
    )

    response.raise_for_status()

    result = response.json()

    output_dir = Path("generated_images")
    output_dir.mkdir(parents=True, exist_ok=True)

    bucket = os.getenv("R2_BUCKET_NAME", "bluepill-images")
    r2 = get_r2_client()

    log_image_url: list[str] = []

    for image in result.get("data", []):
        image_bytes = base64.b64decode(image["b64_json"])

        filename = f"{uuid4().hex}.png"
        output_path = output_dir / filename
        output_path.write_bytes(image_bytes)  # 로컬 저장 (디버깅용)

        # R2 업로드
        key = f"logs/{filename}"
        r2.put_object(Bucket=bucket, Key=key, Body=image_bytes, ContentType="image/png")

        # DB엔 key만 저장
        log_image_url.append(key)
    return {
        "log_image_url": log_image_url,
    }

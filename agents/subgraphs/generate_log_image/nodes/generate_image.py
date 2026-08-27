import base64
import json
import os
from uuid import uuid4
import requests
from agents.daily_logs_agent.state import Context
from agents.subgraphs.generate_log_image.state import GraphState
from common.utils.r2 import generate_r2_image_key, get_r2_client
from langgraph.runtime import Runtime
from common.config import settings


def generate_image(state: GraphState, runtime: Runtime[Context]):

    image_prompt = state["image_prompt"]
    image_reference_image_url = state["image_reference_image_url"]
    image_url = runtime.context.image_url

    payload = {
        "model": "google/gemini-3.1-flash-lite-image",
        "prompt": image_prompt,
    }

    input_references = []

    if image_url:
        input_references.append(
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            }
        )

    if image_reference_image_url:
        input_references.append(
            {
                "type": "image_url",
                "image_url": {"url": image_reference_image_url},
            }
        )

    if input_references:
        payload["input_references"] = input_references

    response = requests.post(
        url="https://openrouter.ai/api/v1/images",
        headers={
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
    )

    response.raise_for_status()

    result = response.json()

    r2 = get_r2_client()

    log_image_url: list[str] = []

    for image in result.get("data", []):
        image_bytes = base64.b64decode(image["b64_json"])
        # R2 업로드
        key = generate_r2_image_key("logs")
        r2.put_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=key,
            Body=image_bytes,
            ContentType="image/png",
        )

        # DB엔 key만 저장
        log_image_url.append(key)
    return {
        "log_image_url": log_image_url[0],
    }

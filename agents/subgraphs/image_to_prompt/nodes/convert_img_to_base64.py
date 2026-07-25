import base64
import requests
from agents.subgraphs.image_to_prompt.state import GraphState


def convert_img_to_base64(state: GraphState) -> GraphState:
    url = state["image_url"]
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        base64_image = base64.b64encode(response.content).decode("utf-8")
        return {"image_base64": base64_image}
    return {"image_base64": ""}

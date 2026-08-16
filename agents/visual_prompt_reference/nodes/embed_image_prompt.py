from common.utils.embedding import embed_text
from agents.visual_prompt_reference.state import GraphState


def embed_image_prompt(state: GraphState) -> GraphState:
    image_prompt = state["image_prompt"]

    embedding = embed_text(image_prompt.prompt)

    return {"embedding": embedding}

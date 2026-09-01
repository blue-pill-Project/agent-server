import base64
from agents.visual_prompt_reference.llm import extract_info_from_image_llm
from agents.visual_prompt_reference.state import (
    Context,
    GraphState,
    VisualPromptReferenceInfo,
)
from langgraph.runtime import Runtime
from agents.visual_prompt_reference.prompts import (
    extract_info_from_image_instructions,
)


def extract_info_from_image(state: GraphState, runtime: Runtime[Context]) -> GraphState:
    image_bytes = runtime.context.image_bytes

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    structured_model = extract_info_from_image_llm.with_structured_output(
        VisualPromptReferenceInfo
    )
    response = structured_model.invoke(
        [
            {
                "role": "human",
                "content": [
                    {
                        "type": "text",
                        "text": extract_info_from_image_instructions,
                    },
                    {
                        "type": "image",
                        "base64": encoded_image,
                        "mime_type": "image/jpeg",
                    },
                ],
            }
        ]
    )

    return {"visual_prompt_reference_info": response}

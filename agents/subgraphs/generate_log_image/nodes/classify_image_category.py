from agents.subgraphs.generate_log_image.llm import classify_image_category_llm
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategoryResult
from agents.subgraphs.generate_log_image.prompts import (
    classify_image_category_instructions,
)


def classify_image_category(state: GraphState):
    hourly_plan_description = state["hourly_plan"].description
    formatted_prompt = classify_image_category_instructions.format(
        hourly_plan_description=hourly_plan_description
    )

    structured_model = classify_image_category_llm.with_structured_output(
        ImageCategoryResult
    )
    response = structured_model.invoke(formatted_prompt)

    return {"image_category": response.image_category}

import pprint
from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategory
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context


async def retrieve_image_prompt(state: GraphState, runtime: Runtime[Context]):
    repository = runtime.context.visual_prompt_reference_repository
    timeslot_label = runtime.context.timeslot_label

    hourly_plan_description = state["hourly_plan"].description
    # TODO: 나중에 이미지 SOLO 말고 다른 종류의 사진도 검색해서 제네레이션 가능해야함
    category = ImageCategory.SOLO_PHOTO
    print(f"{timeslot_label}, {hourly_plan_description}")
    embedding = embed_text(f"{timeslot_label}, {hourly_plan_description}")

    print(hourly_plan_description)

    reference = await repository.search(
        category=category,
        query_vector=embedding,
    )

    return {"image_reference": reference}

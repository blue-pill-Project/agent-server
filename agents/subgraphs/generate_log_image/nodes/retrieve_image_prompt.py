from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState


# TODO: 에이전트 서버 합치면서 현재 사용 안함 리팩토링 할때 연결 하거나 해야함
# 그리고 사용안했을때 출력물 품질도 확인해야함
def retrieve_image_prompt(state: GraphState):
    return True
    # hourly_plan_description = state["hourly_plan"].description
    # category = state["image_category"]

    # print(category)

    # query_vector = str(embed_text(hourly_plan_description))

    # sql = """
    #     SELECT
    #         id,
    #         category,
    #         participant_count,
    #         prompt,
    #         embedding <=> %s::vector AS distance
    #     FROM prompt_references
    #     WHERE category = %s
    #     ORDER BY embedding <=> %s::vector
    #     LIMIT 1
    # """

    # conn = get_connection()

    # try:
    #     with conn.cursor() as cur:
    #         cur.execute(sql, (query_vector, category, query_vector))
    #         row = cur.fetchone()
    # finally:
    #     conn.close()

    # if row is None:
    #     return {"image_reference": None}

    # return {
    #     "image_reference": {
    #         "id": row[0],
    #         "category": row[1],
    #         "participant_count": row[2],
    #         "prompt": row[3],
    #         "distance": float(row[4]),
    #     }
    # }

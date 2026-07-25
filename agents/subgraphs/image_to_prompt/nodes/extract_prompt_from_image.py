from agents.subgraphs.image_to_prompt.llm import extract_prompt_from_image_llm
from agents.subgraphs.image_to_prompt.state import GraphState, ImagePrompt


def extract_prompt_from_image(state: GraphState) -> GraphState:
    image_base64 = state["image_base64"]

    structured_model = extract_prompt_from_image_llm.with_structured_output(
        ImagePrompt, method="json_schema"
    )
    response = structured_model.invoke(
        [
            {
                "role": "human",
                "content": [
                    {
                        "type": "text",
                        "text": """
                당신은 이미지 생성 프롬프트를 저장하는 큐레이터입니다.

목표:
이미지에서 재사용 가능한 '촬영 방식'만 추출합니다.

절대 포함하지 마세요.
- 인물의 얼굴
- 머리색
- 헤어스타일
- 의상
- 소품
- 특정 장소명
- 캐릭터 고유 정보
- 배경의 세부 묘사

반드시 아래 정보만 추출하세요.

1. 실내/실외
2. 구도(composition)
3. 카메라 앵글(camera angle)
4. 거리감(camera distance)
5. 포즈(pose)
6. 표정(expression)
7. 분위기(mood)

추출한 정보를 하나의 재사용 가능한 이미지 생성 프롬프트로 작성하세요.

규칙:
- 누가 와도 재사용 가능하도록 일반화합니다.
- 사람 대신 'subject'라고 표현합니다.
- 장소 대신 'indoor space' 또는 'outdoor space'처럼 일반화합니다.
- 구도와 촬영 방식 위주로 작성합니다.
- 3~5문장으로 작성합니다.
- category는 반드시 enum 값 중 하나로 선택합니다.
- participant_count는 주요 인물 수만 계산합니다.

                """,
                    },
                    {
                        "type": "image",
                        "base64": image_base64,
                        "mime_type": "image/jpeg",
                    },
                ],
            }
        ]
    )

    return {"image_prompt": response}

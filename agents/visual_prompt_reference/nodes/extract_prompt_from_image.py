import base64
from agents.visual_prompt_reference.llm import extract_prompt_from_image_llm
from agents.visual_prompt_reference.state import Context, GraphState, ImagePrompt
from langgraph.runtime import Runtime


def extract_prompt_from_image(
    state: GraphState, runtime: Runtime[Context]
) -> GraphState:
    image_bytes = runtime.context.image_bytes
    # image_content_type = (
    #     runtime.context.image_content_type
    # )

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    structured_model = extract_prompt_from_image_llm.with_structured_output(ImagePrompt)
    response = structured_model.invoke(
        [
            {
                "role": "human",
                "content": [
                    {
                        "type": "text",
                        "text": """
              당신은 이미지 생성용 촬영 레퍼런스를 저장하는 큐레이터입니다.

목표:
이미지의 캐릭터나 상황이 아니라, 다른 인물과 장소에도 적용할 수 있는
재사용 가능한 '시각적 촬영 문법'을 추출합니다.

핵심 판단 원칙:
- 이미지의 내용보다 사진이 어떻게 촬영되었는지를 설명합니다.
- 다른 subject와 장소로 교체해도 동일한 구도와 촬영 효과를 재현할 수 있어야 합니다.
- 촬영 구도를 형성하는 필수 요소는 제거하지 말고 일반화합니다.
  예: 편의점 보안 거울 → 크고 둥근 볼록 반사면
- 단순히 장면을 꾸미는 요소는 제거합니다.
  예: 음식, 가방, 상품, 장식, 의상, 배경 속 물건
- 이미지에서 명확히 확인되지 않는 정보는 추측하지 않습니다.

절대 포함하지 마세요:
- 인물의 얼굴 생김새
- 머리색과 헤어스타일
- 인물의 고유한 신체 특징
- 의상
- 장면에 종속된 소품
- 브랜드와 상품명
- 특정 장소명
- 캐릭터 고유 정보
- 배경의 구체적인 물건과 장식
- 이미지 속 문구

반드시 다음 정보를 추출하세요:
1. 실내 또는 실외
2. 이미지 방향과 구도
3. 프레임 안에서 subject의 위치
4. 카메라 앵글
5. 카메라 거리와 촬영 범위
6. subject의 자세와 손·팔·다리의 배치
7. 시선과 표정의 감정 상태
8. 조명의 방향, 세기, 성질
9. 반사, 왜곡, 원근감 등의 광학 효과
10. 스마트폰 스냅, 필름 사진 등의 촬영 질감
11. 전체적인 분위기
12. 해당 촬영법을 재현하는 데 반드시 필요한 시각적 요소

작성 규칙:
- 사람은 반드시 'subject'라고 표현합니다.
- 장소는 'indoor space' 또는 'outdoor space'로 일반화합니다.
- subject가 프레임의 중앙, 왼쪽, 오른쪽, 전경 또는 후경 중 어디에 있는지 명시합니다.
- '감성적', '예쁜' 같은 추상적인 표현만 사용하지 말고 이를 만드는 조명과 구도를 설명합니다.
- 촬영에 필수적인 구조물은 형태와 기능만 남겨 일반화합니다.
- prompt는 한국어로 5~7문장으로 최대한 자세히 작성합니다.
- category는 SOLO, PAIR, GROUP, FOOD, PLACE, OBJECT 중 하나만 사용합니다.
- participant_count는 주요 subject의 수만 계산합니다.

출력 형식:
{
  "category": "enum 값",
  "participant_count": 1,
  "prompt": "재사용 가능한 한국어 이미지 생성 프롬프트"
}

                """,
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

    return {"visual_prompt_reference": response}

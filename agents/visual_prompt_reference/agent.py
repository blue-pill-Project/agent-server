import os
from uuid import uuid4
from agents.base import BaseAgent
from agents.visual_prompt_reference.state import Context, VisualPromptReferenceForSave
from agents.visual_prompt_reference.graph import build_visual_prompt_reference_graph
from common.utils.embedding import embed_text
from common.utils.r2 import generate_r2_image_key, get_r2_client
from domains.visual_prompt_reference.repository import VisualPromptReferenceRepository
from common.config import settings


class VisualPromptReferenceAgent(BaseAgent):
    """
    주어진 이미지를 기반으로 이미지를 해석한후 이미지 레퍼런스를 만들고 저장한다.
    """

    def __init__(
        self,
        visual_prompt_reference_repository: VisualPromptReferenceRepository,
    ):
        super().__init__()

        self._visual_prompt_reference_repository = visual_prompt_reference_repository

    def build_graph(self):
        return build_visual_prompt_reference_graph()

    def _build_visual_prompt_reference_for_save(
        self,
        info,
        image_key: str,
        is_default: bool,
    ) -> VisualPromptReferenceForSave:
        return VisualPromptReferenceForSave(
            category=info.category,
            camera_style=info.camera_style,
            participant_count=info.participant_count,
            image_key=image_key,
            situation=info.situation,
            situation_embedding=embed_text(info.situation),
            is_default_selfie=(is_default and info.camera_style == "selfie"),
        )

    async def run(self, image_bytes: bytes, image_content_type: str, is_default: bool):
        """
        주어진 이미지를 기반으로 이미지를 해석한후 이미지 레퍼런스를 만들고 저장하는 핵심 함수
        Args:
            image_bytes:
                바이트로 표현된 이미지

            image_content_type:
                이미지 타입

            is_default:
                해당 이미지를 기본 이미지로 사용할것인지
        Returns:
            전체 성공 유무(데이터 생성 및 저장) 불리언값

        Notes:
            벡터 검색을 했을때 점수가 낮다면 기본 셀카를 사용해야하기 때문에
            selfie와 is_default가 모두 참이면 기본 셀카로 저장이 되고 이를 사용할수 있도록 한다.
        """
        context = Context(
            image_bytes=image_bytes,
            image_content_type=image_content_type,
            is_default=is_default,
        )

        state = await self.invoke({}, context=context)
        # TODO: 반복 수정 해야함
        # R2 에 이미지를 저장한다.
        r2 = get_r2_client()
        key = generate_r2_image_key("visual_prompt_references")
        r2.put_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=key,
            Body=image_bytes,
            ContentType="image/png",
        )

        # DB에 저장할 정보를 모으고 객체로 만든다.
        visual_prompt_reference_info = state["visual_prompt_reference_info"]

        visual_prompt_reference_for_save = self._build_visual_prompt_reference_for_save(
            info=visual_prompt_reference_info,
            image_key=key,
            is_default=is_default,
        )
        # 정리된 최종 데이터를 저장한다.
        success = await self._visual_prompt_reference_repository.save(
            visual_prompt_reference_for_save
        )

        # TODO: 테스트 후 삭제해야함
        print(visual_prompt_reference_info.situation)

        return success

from fastapi import APIRouter, Request
from api.schemas.character_chat import CharacterChatRequest, CharacterChatResponse

# TODO: 나중에 다른 chat agent가 추가 될수 있어서  해당 이름 character-chat으로 바꿔야함
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=CharacterChatResponse)
async def run_character_chat(
    body: CharacterChatRequest,
    request: Request,
):
    character_chat_agent = request.app.state.character_chat_agent

    user_id = body.user_id
    log_room_id = body.log_room_id
    log_room_member_id = body.log_room_member_id
    content = body.content

    result = await character_chat_agent.run(
        user_id, log_room_id, log_room_member_id, content
    )

    return CharacterChatResponse(reply=result)

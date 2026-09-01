from fastapi import APIRouter, Request

from api.schemas.chat_rule import (
    ChatRuleRequest,
    ChatRuleResponse,
)

router = APIRouter(prefix="/chat-rule", tags=["chat_rule"])


@router.post("/run", response_model=ChatRuleResponse)
async def run_chat_rule(
    body: ChatRuleRequest,
    request: Request,
):
    chat_rule_agent = request.app.state.chat_rule_agent

    chat_rule = await chat_rule_agent.run(
        body.character_id,
        body.relationship,
    )

    return ChatRuleResponse(chat_rule=chat_rule)

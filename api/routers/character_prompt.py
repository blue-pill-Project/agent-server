from fastapi import APIRouter, Request

from api.schemas.character_prompt import (
    CharacterPromptRequest,
    CharacterPromptResponse,
)

router = APIRouter(prefix="/character-prompt", tags=["character_prompt"])


@router.post("/complete", response_model=CharacterPromptResponse)
async def complete_character_prompt(
    body: CharacterPromptRequest,
    request: Request,
):
    character_prompt_agent = request.app.state.character_prompt_agent

    prompt = await character_prompt_agent.run(
        body.name,
        body.intro,
        body.user_prompt,
    )

    return CharacterPromptResponse(prompt=prompt)

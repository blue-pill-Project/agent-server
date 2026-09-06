from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

from common.config import settings


@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )


async def embed_text(text: str) -> list[float]:
    embeddings = get_embeddings()
    return await embeddings.aembed_query(text)

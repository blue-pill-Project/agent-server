from langchain_openai import OpenAIEmbeddings
from common.config import settings


def embed_text(text: str) -> list[float]:
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    vector = embeddings.embed_query(text)

    return vector

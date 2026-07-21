from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def embed_text(text: str) -> list[float]:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    if not OPENROUTER_API_KEY:
        raise RuntimeError("required OPENROUTER_API_KEY")

    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    vector = embeddings.embed_query(text)

    return vector

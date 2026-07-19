from dataclasses import dataclass


@dataclass
class LLMConfig:
    model: str
    temperature: float = 0.7
    max_retries: int = 2
    max_tokens: int | None = None

from dataclasses import dataclass

import torch
from sentence_transformers import CrossEncoder


@dataclass
class RerankedDocument:
    content: str
    score: float
    original_index: int


class BgeReranker:
    def __init__(
        self,
        model_name: str = "skygudanr/klue-roberta-small-cross-encoder",
        max_length: int = 512,
    ) -> None:
        self.model = CrossEncoder(
            model_name,
            device=self._get_device(),
            max_length=max_length,
        )

    @staticmethod
    def _get_device() -> str:
        if torch.cuda.is_available():
            return "cuda"

        if torch.backends.mps.is_available():
            return "mps"

        return "cpu"

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int | None = None,
    ) -> list[RerankedDocument]:
        if not documents:
            return []

        pairs = [(query, document) for document in documents]

        scores = self.model.predict(
            pairs,
            batch_size=8,
            show_progress_bar=False,
            processing_kwargs={"text": {"return_token_type_ids": False}},
        )

        results = [
            RerankedDocument(
                content=document,
                score=float(score),
                original_index=index,
            )
            for index, (document, score) in enumerate(zip(documents, scores))
        ]

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        if top_k is not None:
            results = results[:top_k]

        return results

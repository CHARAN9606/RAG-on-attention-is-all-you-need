from qdrant_client import QdrantClient

from app.ingestion.embedder import get_embedder
from app.retrieval.vector_store import COLLECTION_NAME


def search_chunks(query: str, top_k: int = 5) -> list[dict]:
    client = QdrantClient(path="./data/qdrant")
    embedder = get_embedder()

    query_vector = embedder.embed_text(query)

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )

    retrieved_chunks = []

    for result in response.points:
        payload = result.payload or {}

        retrieved_chunks.append(
            {
                "chunk_id": payload.get("chunk_id"),
                "page_number": payload.get("page_number"),
                "section": payload.get("section"),
                "text": payload.get("text", ""),
                "score": result.score,
            }
        )

    client.close()

    return retrieved_chunks
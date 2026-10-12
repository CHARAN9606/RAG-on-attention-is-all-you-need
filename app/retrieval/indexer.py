from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from app.ingestion.embedder import BGEEmbedder
from app.retrieval.vector_store import COLLECTION_NAME, create_vector_store


def index_chunks(chunks: list[dict]) -> QdrantClient:
    client = create_vector_store()
    embedder = BGEEmbedder()

    if not chunks:
        print("No chunks to index.")
        return client

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.embed_texts(texts)

    points = []

    for point_id, (chunk, embedding) in enumerate(
        zip(chunks, embeddings), start=1
    ):
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "document_id": chunk["document_id"],
                "document_name": chunk["document_name"],
                "chunk_id": chunk["chunk_id"],
                "page_number": chunk["page_number"],
                "section": chunk["section"],
                "source": chunk["source"],
                "text": chunk["text"],
            },
        )
        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(f"Indexed {len(points)} chunks into Qdrant.")
    return client
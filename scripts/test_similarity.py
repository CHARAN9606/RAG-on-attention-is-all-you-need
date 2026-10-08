from pathlib import Path

import numpy as np
from unstructured.partition.pdf import partition_pdf

from app.ingestion.normalizer import normalize_element
from app.ingestion.cleaner import clean_element
from app.ingestion.grouper import group_elements
from app.ingestion.chunker import create_chunks
from app.ingestion.embedder import BGEEmbedder


PDF_PATH = Path("data/raw/attention-is-all-you-need.pdf")


def load_chunks() -> list[dict]:
    elements = partition_pdf(
        filename=str(PDF_PATH),
        strategy="fast",
    )

    cleaned_elements = []

    for element in elements:
        normalized = normalize_element(
            element=element,
            document_id="attention-is-all-you-need",
            document_name=PDF_PATH.name,
        )

        cleaned = clean_element(normalized)

        if cleaned is not None:
            cleaned_elements.append(cleaned)

    blocks = group_elements(cleaned_elements)

    return create_chunks(
        blocks,
        chunk_size=2000,
        chunk_overlap=200,
    )


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a)
    b = np.array(b)

    return float(
        np.dot(a, b)
        / (np.linalg.norm(a) * np.linalg.norm(b))
    )


def main() -> None:
    chunks = load_chunks()

    print(f"Total chunks: {len(chunks)}")

    embedder = BGEEmbedder()

    chunk_texts = [chunk["text"] for chunk in chunks]

    print("\nCreating document embeddings...")
    chunk_embeddings = embedder.embed_texts(chunk_texts)

    query = "What is multi-head attention?"

    print(f"\nQuery: {query}")

    query_embedding = embedder.embed_text(query)

    results = []

    for chunk, embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(
            query_embedding,
            embedding,
        )

        results.append(
            {
                "score": score,
                "chunk": chunk,
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    print("\n" + "=" * 80)
    print("TOP 5 RESULTS")
    print("=" * 80)

    for rank, result in enumerate(results[:5], start=1):
        chunk = result["chunk"]

        print("\n" + "-" * 80)
        print(f"Rank       : {rank}")
        print(f"Score      : {result['score']:.4f}")
        print(f"Chunk ID    : {chunk['chunk_id']}")
        print(f"Page       : {chunk['page_number']}")
        print(f"Section    : {chunk['section']}")
        print(f"Text       : {chunk['text'][:1000]}")


if __name__ == "__main__":
    main()
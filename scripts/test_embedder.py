from pathlib import Path

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

    chunks = create_chunks(
        blocks,
        chunk_size=2000,
        chunk_overlap=200,
    )

    return chunks


def main() -> None:
    chunks = load_chunks()

    print(f"Total chunks: {len(chunks)}")

    texts = [chunk["text"] for chunk in chunks]

    embedder = BGEEmbedder()

    embeddings = embedder.embed_texts(texts)

    print(f"Total embeddings: {len(embeddings)}")
    print(f"Embedding dimension: {len(embeddings[0])}")

    print("\nFirst embedding:")
    print(embeddings[0][:10])

    print("\nFirst chunk:")
    print(chunks[0]["text"][:500])


if __name__ == "__main__":
    main()
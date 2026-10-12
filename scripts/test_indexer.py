from pathlib import Path

from unstructured.partition.pdf import partition_pdf

from app.ingestion.normalizer import normalize_element
from app.ingestion.cleaner import clean_element
from app.ingestion.grouper import group_elements
from app.ingestion.chunker import create_chunks
from app.retrieval.indexer import index_chunks


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


def main() -> None:
    chunks = load_chunks()
    client = index_chunks(chunks)

    collection = client.get_collection("attention_paper")

    print(f"Points stored: {collection.points_count}")


if __name__ == "__main__":
    main()
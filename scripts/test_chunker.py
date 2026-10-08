from pathlib import Path

from unstructured.partition.pdf import partition_pdf

from app.ingestion.normalizer import normalize_element
from app.ingestion.cleaner import clean_element
from app.ingestion.grouper import group_elements
from app.ingestion.chunker import create_chunks


PDF_PATH = Path("data/raw/attention-is-all-you-need.pdf")


def main() -> None:
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

    print(f"Cleaned elements: {len(cleaned_elements)}")
    print(f"Logical blocks:   {len(blocks)}")

    print("\nFIRST 10 BLOCKS")

    for block in blocks[:10]:
        print("\n" + "=" * 80)
        print(f"Page: {block.page_number}")
        print(f"Section: {block.section}")
        print(f"Characters: {len(block.text)}")
        print("-" * 80)
        print(block.text[:1000])

    chunks = create_chunks(
        blocks,
        chunk_size=2000,
        chunk_overlap=200,
    )

    print("\n" + "=" * 80)
    print(f"Total chunks: {len(chunks)}")

    print("\nFIRST 10 CHUNKS")

    for chunk in chunks[:10]:
        print("\n" + "=" * 80)
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Page: {chunk['page_number']}")
        print(f"Section: {chunk['section']}")
        print(f"Characters: {len(chunk['text'])}")
        print("-" * 80)
        print(chunk["text"])


if __name__ == "__main__":
    main()
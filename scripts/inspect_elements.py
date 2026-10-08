from pathlib import Path

from unstructured.partition.pdf import partition_pdf

from app.ingestion.normalizer import normalize_element


PDF_PATH = Path("data/raw/attention-is-all-you-need.pdf")


def main() -> None:
    elements = partition_pdf(
        filename=str(PDF_PATH),
        strategy="fast",
    )

    for i, element in enumerate(elements):
        normalized = normalize_element(
            element=element,
            document_id="attention-is-all-you-need",
            document_name=PDF_PATH.name,
        )

        print("\n" + "=" * 80)
        print(f"Index: {i}")
        print(f"Type: {normalized.element_type}")
        print(f"Page: {normalized.page_number}")
        print(f"Text: {normalized.text[:300]}")


if __name__ == "__main__":
    main()
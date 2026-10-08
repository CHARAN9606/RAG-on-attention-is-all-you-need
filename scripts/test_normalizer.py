from pathlib import Path

from unstructured.partition.pdf import partition_pdf

from app.ingestion.normalizer import normalize_element


PDF_PATH = Path("data/raw/attention-is-all-you-need.pdf")


def main() -> None:
    elements = partition_pdf(
        filename=str(PDF_PATH),
        strategy="fast",
    )

    first_element = elements[5]

    normalized = normalize_element(
        element=first_element,
        document_id="attention-is-all-you-need",
        document_name=PDF_PATH.name,
    )

    print(normalized)
if __name__ == "__main__":
    main()
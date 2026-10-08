from pathlib import Path

from unstructured.partition.pdf import partition_pdf

from app.ingestion.normalizer import normalize_element
from app.ingestion.cleaner import clean_element


PDF_PATH = Path("data/raw/attention-is-all-you-need.pdf")


def main() -> None:
    elements = partition_pdf(
        filename=str(PDF_PATH),
        strategy="fast",
    )

    kept = 0
    removed = 0

    for element in elements:
        normalized = normalize_element(
            element=element,
            document_id="attention-is-all-you-need",
            document_name=PDF_PATH.name,
        )

        cleaned = clean_element(normalized)

        if cleaned is None:
            removed += 1
            continue

        kept += 1

        print(
            f"[Page {cleaned.page_number}] "
            f"{cleaned.element_type}: "
            f"{cleaned.text[:200]}"
        )

    print("\n" + "=" * 80)
    print(f"Original elements : {len(elements)}")
    print(f"Kept elements     : {kept}")
    print(f"Removed elements  : {removed}")


if __name__ == "__main__":
    main()
from pathlib import Path
from collections import Counter
from unstructured.partition.pdf import partition_pdf

PDF_PATH = Path("data/raw/attention-is-all-you-need.pdf")

def main() -> None:
    elements = partition_pdf(
        filename=str(PDF_PATH),
        strategy="fast",
    )

    print(f"Total elements: {len(elements)}")

    # 1. Count element types
    type_counts = Counter(
        type(element).__name__
        for element in elements
    )

    print("\n" + "=" * 80)
    print("ELEMENT TYPE SUMMARY")
    print("=" * 80)

    for element_type, count in type_counts.most_common():
        print(f"{element_type:30} {count}")

    # 2. Inspect first 15 elements
    print("\n" + "=" * 80)
    print("ELEMENT DETAILS")
    print("=" * 80)

    for i, element in enumerate(elements[:15]):
        print("\n" + "-" * 80)
        print(f"Element #{i}")
        print(f"Type: {type(element).__name__}")
        print(f"Text: {str(element)[:500]}")

        metadata = element.metadata

        print(f"Page: {metadata.page_number}")
        print(f"Element ID: {element.id}")
        print(f"Section: {metadata.to_dict()}")

if __name__ == "__main__":
    main()
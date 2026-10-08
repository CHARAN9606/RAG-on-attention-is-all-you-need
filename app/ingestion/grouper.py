from dataclasses import dataclass

from .normalizer import DocumentElement


@dataclass
class DocumentBlock:
    document_id: str
    document_name: str
    page_number: int | None
    section: str | None
    text: str


def group_elements(
    elements: list[DocumentElement],
) -> list[DocumentBlock]:
    blocks = []

    current_text = []
    current_page = None
    current_section = None

    for element in elements:
        text = element.text.strip()

        if not text:
            continue

        # Treat obvious numbered headings as section boundaries.
        is_section = (
            element.element_type == "Title"
            and (
                text[0].isdigit()
                or text in {
                    "Abstract",
                    "Introduction",
                    "Conclusion",
                    "References",
                }
            )
        )

        if is_section:
            # Finish the previous block.
            if current_text:
                blocks.append(
                    DocumentBlock(
                        document_id=element.document_id,
                        document_name=element.document_name,
                        page_number=current_page,
                        section=current_section,
                        text="\n\n".join(current_text),
                    )
                )

                current_text = []

            current_section = text
            current_page = element.page_number
            current_text.append(text)
            continue

        if current_page is None:
            current_page = element.page_number

        current_text.append(text)

    # Save final block.
    if current_text:
        blocks.append(
            DocumentBlock(
                document_id=elements[0].document_id,
                document_name=elements[0].document_name,
                page_number=current_page,
                section=current_section,
                text="\n\n".join(current_text),
            )
        )

    return blocks
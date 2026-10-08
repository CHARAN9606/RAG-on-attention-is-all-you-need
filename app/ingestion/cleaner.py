from .normalizer import DocumentElement


NOISE_TEXTS = {
    "<pad>",
    "<EOS>",
    "3 2 0 2",
    "g u A 2",
    "] L C . s c [",
    "7 v 2 6 7 3 0 . 6 0 7 1 : v i X r a",
}


def clean_element(element: DocumentElement) -> DocumentElement | None:
    text = element.text.strip()

    # Remove empty elements
    if not text:
        return None

    # Remove obvious PDF extraction artifacts
    if text in NOISE_TEXTS:
        return None

    # Normalize repeated whitespace/newlines
    text = " ".join(text.split())

    return DocumentElement(
        document_id=element.document_id,
        document_name=element.document_name,
        element_id=element.element_id,
        element_type=element.element_type,
        page_number=element.page_number,
        text=text,
        metadata=element.metadata,
    )
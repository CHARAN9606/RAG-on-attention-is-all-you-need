from langchain_text_splitters import RecursiveCharacterTextSplitter

from .grouper import DocumentBlock


def create_chunks(
    blocks: list[DocumentBlock],
    chunk_size: int = 2000,
    chunk_overlap: int = 200,
) -> list[dict]:

    if not blocks:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []

    for block in blocks:
        split_texts = splitter.split_text(block.text)

        for text in split_texts:
            chunk_number = len(chunks) + 1

            chunks.append(
                {
                    "chunk_id": f"{block.document_id}-{chunk_number}",
                    "document_id": block.document_id,
                    "document_name": block.document_name,
                    "page_number": block.page_number,
                    "section": block.section,
                    "source": block.document_name,
                    "text": text,
                }
            )

    return chunks
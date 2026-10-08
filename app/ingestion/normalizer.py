from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentElement:
    document_id: str
    document_name: str
    element_id: str
    element_type: str
    page_number: int | None
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_element(
    element: Any,
    document_id: str,
    document_name: str,
) -> DocumentElement:
    metadata = element.metadata.to_dict()

    return DocumentElement(
        document_id=document_id,
        document_name=document_name,
        element_id=element.id,
        element_type=type(element).__name__,
        page_number=metadata.get("page_number"),
        text=str(element).strip(),
        metadata=metadata,
    )
from app.retrieval.vector_store import (
    COLLECTION_NAME,
    create_vector_store,
)


def main() -> None:
    client = create_vector_store()

    collection = client.get_collection(COLLECTION_NAME)

    print("Qdrant collection created successfully.")
    print(f"Collection name: {COLLECTION_NAME}")
    print(f"Vector count: {collection.points_count}")
    print(f"Vector configuration: {collection.config.params.vectors}")


if __name__ == "__main__":
    main()
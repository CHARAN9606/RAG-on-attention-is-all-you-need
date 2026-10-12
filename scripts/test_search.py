from app.retrieval.search import search_chunks


def main() -> None:
    query = "What is multi-head attention?"

    results = search_chunks(query, top_k=5)

    print(f"\nQuery: {query}\n")

    if not results:
        print("No results found.")
        return

    for rank, result in enumerate(results, start=1):
        print("=" * 80)
        print(f"Rank: {rank}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Page: {result['page_number']}")
        print(f"Section: {result['section']}")
        print(f"Similarity score: {result['score']:.4f}")
        print(f"\nText:\n{result['text'][:700]}")

    print("=" * 80)


if __name__ == "__main__":
    main()
from app.retrieval.search import search_chunks


def main() -> None:
    queries = [
    "How does the Transformer handle long-range dependencies?",
]

    for query in queries:
        print("\n" + "=" * 80)
        print(f"Query: {query}")
        print("=" * 80)

        results = search_chunks(query, top_k=10)

        for rank, result in enumerate(results, start=1):
            print(
                f"\nRank: {rank} | "
                f"Score: {result['score']:.4f}"
            )
            print(f"Section: {result['section']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Text: {result['text'][:300]}")


if __name__ == "__main__":
    main()
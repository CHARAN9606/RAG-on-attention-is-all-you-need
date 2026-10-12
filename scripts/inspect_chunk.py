from app.retrieval.search import search_chunks


def main() -> None:
    query = "Why does self-attention help the Transformer handle long-range dependencies?"

    results = search_chunks(query, top_k=10)

    for result in results:
        if result["chunk_id"] == "attention-is-all-you-need-15":
            print("=" * 80)
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Section: {result['section']}")
            print(f"Page: {result['page_number']}")
            print(f"Score: {result['score']:.4f}")
            print("=" * 80)
            print(result["text"])
            return

    print("Target chunk was not found in the top 10 results.")


if __name__ == "__main__":
    main()
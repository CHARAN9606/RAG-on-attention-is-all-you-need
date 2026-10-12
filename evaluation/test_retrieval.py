from app.retrieval.search import search_chunks


EVALUATION_DATASET = [
    {
        "question": "What is multi-head attention?",
        "expected_section": "3.2.2 Multi-Head Attention",
    },
    {
        "question": "How is scaled dot-product attention calculated?",
        "expected_section": "3.2.1 Scaled Dot-Product Attention",
    },
    {
        "question": "Why does the Transformer use positional encodings?",
        "expected_section": "3.5 Positional Encoding",
    },
    {
        "question": "What is the role of the encoder in the Transformer?",
        "expected_section": "3.1 Encoder and Decoder Stacks",
    },
    {
    "question": "How does the Transformer handle long-range dependencies?",
    "expected_section": "4 Why Self-Attention",
    },
]


def evaluate_retrieval(top_k: int = 3) -> None:
    total_questions = len(EVALUATION_DATASET)
    hits = 0
    reciprocal_ranks = []

    for item in EVALUATION_DATASET:
        question = item["question"]
        expected_section = item["expected_section"]

        results = search_chunks(question, top_k=top_k)

        matching_rank = None

        for rank, result in enumerate(results, start=1):
            if result["section"] == expected_section:
                matching_rank = rank
                break

        if matching_rank is not None:
            hits += 1
            reciprocal_ranks.append(1 / matching_rank)
        else:
            reciprocal_ranks.append(0)

        print("\n" + "=" * 70)
        print(f"Question: {question}")
        print(f"Expected section: {expected_section}")

        if matching_rank is not None:
            print(f"Expected section found at rank: {matching_rank}")
        else:
            print(f"Expected section not found in top {top_k}")

        print("\nRetrieved results:")

        for rank, result in enumerate(results, start=1):
            print(
                f"Rank {rank} | "
                f"Score: {result['score']:.4f} | "
                f"Section: {result['section']}"
            )

    hit_rate = hits / total_questions
    mrr = sum(reciprocal_ranks) / total_questions

    print("\n" + "=" * 70)
    print("RETRIEVAL EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Total questions: {total_questions}")
    print(f"Hit Rate@{top_k}: {hit_rate:.2%}")
    print(f"MRR@{top_k}: {mrr:.4f}")


if __name__ == "__main__":
    evaluate_retrieval(top_k=3)
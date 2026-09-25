from chat.services.retrieval import (
    retrieve_relevant_chunks,
)

from chat.services.rag import (
    generate_answer,
)


def calculate_keyword_score(
    answer,
    expected_keywords,
):
    if not expected_keywords:
        return 0.0

    answer_lower = answer.lower()

    matched = 0

    for keyword in expected_keywords:

        if keyword.lower() in answer_lower:
            matched += 1

    return matched / len(expected_keywords)


def calculate_retrieval_score(
    chunks,
    expected_keywords,
):
    if not chunks:
        return 0.0

    if not expected_keywords:
        return 0.0

    combined_text = " ".join(
        chunk["content"]
        for chunk in chunks
    ).lower()

    matched = 0

    for keyword in expected_keywords:

        if keyword.lower() in combined_text:
            matched += 1

    return matched / len(expected_keywords)


def evaluate_case(
    question,
    user_id,
    expected_keywords,
):
    chunks = retrieve_relevant_chunks(
        question=question,
        user_id=user_id,
        n_results=5,
    )


    result = generate_answer(
        question=question,
        user_id=user_id,
        n_results=5,
    )


    answer = result["answer"]


    keyword_score = calculate_keyword_score(
        answer=answer,
        expected_keywords=expected_keywords,
    )


    retrieval_score = calculate_retrieval_score(
        chunks=chunks,
        expected_keywords=expected_keywords,
    )


    return {
        "question": question,

        "answer": answer,

        "retrieved_chunks":
            len(chunks),

        "keyword_score":
            keyword_score,

        "retrieval_score":
            retrieval_score,

        "sources":
            result["sources"],
    }
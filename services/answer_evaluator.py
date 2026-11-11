
STOP_WORDS = {
    "what", "is", "are", "the", "a", "an", "of", "in", "to",
    "and", "or", "for", "how", "does", "do", "explain",
    "difference", "between", "main", "features", "concept"
}


def evaluate_answer(question, answer):
    question_words = {
        word.lower().strip(".,?!")
        for word in question.split()
        if word.lower().strip(".,?!") not in STOP_WORDS
    }

    answer_words = {
        word.lower().strip(".,?!")
        for word in answer.split()
    }

    # Check answer length (maximum 30 marks)
    word_count = len(answer.split())

    if word_count < 5:
        length_score = 0
    elif word_count < 15:
        length_score = 10
    elif word_count < 30:
        length_score = 20
    else:
        length_score = 30

    # Check relevance using common keywords (maximum 50 marks)
    if question_words:
        matched_words = question_words.intersection(answer_words)
        relevance_score = round(
            (len(matched_words) / len(question_words)) * 50
        )
    else:
        relevance_score = 0

    # Reward a reasonably detailed answer (maximum 20 marks)
    detail_score = 20 if word_count >= 20 else 10 if word_count >= 10 else 0

    total_score = min(
        100, length_score + relevance_score + detail_score
    )

    if total_score >= 75:
        feedback = "Good answer! You have demonstrated a good understanding."
    elif total_score >= 50:
        feedback = "Average answer. Try to include more relevant details."
    else:
        feedback = "Needs improvement. Study the topic and provide a more detailed answer."

    return {
        "question": question,
        "answer": answer,
        "score": total_score,
        "feedback": feedback
    }


def evaluate_answers(answers):
    results = []

    for item in answers:
        question = item.get("question", "")
        answer = item.get("answer", "")

        if not question.strip() or not answer.strip():
            continue

        result = evaluate_answer(question, answer)
        results.append(result)

    if not results:
        return {
            "evaluated_answers": [],
            "preparedness_percentage": 0,
            "message": "No valid answers were submitted."
        }

    total_score = sum(item["score"] for item in results)
    preparedness = round(total_score / len(results), 2)

    return {
        "evaluated_answers": results,
        "preparedness_percentage": preparedness,
        "message": "Interview evaluation completed successfully."
    }

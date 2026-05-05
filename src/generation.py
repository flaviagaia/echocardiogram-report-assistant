from __future__ import annotations

from collections import Counter

from .retrieval import RetrievedItem


def similarity_to_confidence(similarity: float) -> str:
    if similarity >= 0.5:
        return "high"
    if similarity >= 0.25:
        return "medium"
    return "low"


def generate_report(
    question: str,
    retrieved_items: list[RetrievedItem],
    structured_summary: dict,
    summary_lines: list[str],
    impression_lines: list[str],
) -> dict:
    case_hits = [item for item in retrieved_items if item.source_type == "case"]
    knowledge_hits = [item for item in retrieved_items if item.source_type == "knowledge"]
    primary_case = case_hits[0].payload if case_hits else None
    best_similarity = retrieved_items[0].similarity if retrieved_items else 0.0

    pattern_counter = Counter()
    for item in case_hits[:3]:
        pattern_counter.update(
            [
                item.payload["lv_size"],
                item.payload["rv_function"],
                item.payload["diastolic_function"],
                item.payload["mitral_regurgitation"],
                item.payload["aortic_stenosis"],
                item.payload["pericardial_effusion"],
            ]
        )

    findings = " ".join(summary_lines)
    if primary_case:
        findings += f" Retrieved similar case wording suggests: {primary_case['findings']}"
    impression = " ".join(impression_lines)

    recommendation = "Physician review is required before report sign-off."
    if knowledge_hits:
        recommendation += " Guideline/template context was retrieved to improve wording consistency."

    return {
        "question": question,
        "confidence": similarity_to_confidence(best_similarity),
        "best_similarity": round(best_similarity, 4),
        "draft_report": {
            "technique": "Comprehensive transthoracic echocardiogram performed.",
            "findings": findings,
            "impression": impression,
        },
        "suggested_patterns": [label for label, _ in pattern_counter.most_common(6)],
        "reference_case_ids": [hit.source_id for hit in case_hits[:3]],
        "recommendation": recommendation,
        "evidence": [
            {
                "source_type": item.source_type,
                "source_id": item.source_id,
                "title": item.title,
                "similarity": round(item.similarity, 4),
            }
            for item in retrieved_items
        ],
    }

def calculate_match_score(result):
    """
    Calculate opportunity relevance while respecting eligibility.

    Confirmed ineligible opportunities receive zero.
    Opportunities needing more information retain a relevance score.
    """
    eligibility_status = result.get("eligibility_status")

    # Preserve the existing behavior for confirmed ineligibility.
    if eligibility_status == "INELIGIBLE":
        return 0.0

    # Backward compatibility with existing callers and tests.
    if eligibility_status is None and not result.get("eligible", False):
        return 0.0

    similarity = max(
        0.0,
        min(1.0, float(result.get("semantic_similarity", 0.0)))
    )

    interest_match = max(
        0.0,
        min(1.0, float(result.get("interest_match", 0.0)))
    )

    score = (0.80 * similarity) + (0.20 * interest_match)

    return round(score * 100, 2)


def rank_matches(results):
    for result in results:
        result["match_score"] = calculate_match_score(result)

    return sorted(
        results,
        key=lambda result: result["match_score"],
        reverse=True
    )

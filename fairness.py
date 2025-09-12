# fairness.py
from typing import List, Dict

def fairness_rerank_for_candidate(results: List[Dict], candidate_profile: Dict, required_accommodation_min: bool = False, top_k: int = 5):
    """
    Simple re-ranking that ensures low-income/out-of-state candidates get at least one
    internship that provides accommodation (if available in job pool).
    If candidate_income is low (e.g., <3L), and no accommodation in top results,
    we try to insert the highest-scoring job that provides accommodation.
    """
    income = candidate_profile.get("annual_income")
    prefer_accom = False
    if income is not None and income > 0 and income < 300000:
        prefer_accom = True
    # If required_accommodation_min True, treat as prefer_accom
    if required_accommodation_min:
        prefer_accom = True

    # if not preferring, just return results
    if not prefer_accom:
        return results[:top_k]

    # check if any of top_k have accommodation
    top = results[:top_k]
    if any(r["accommodation_flag"]==1 for r in top):
        return top

    # else find highest-scoring accom job in results beyond top_k
    accom_candidates = [r for r in results if r["accommodation_flag"]==1]
    if not accom_candidates:
        return top  # nothing to do

    best_accom = accom_candidates[0]
    # replace the last element (lowest of top_k) with best_accom if best_accom not in top
    if best_accom not in top:
        new_top = top[:-1] + [best_accom]
    else:
        new_top = top
    # ensure sorted by final_score descending
    new_top = sorted(new_top, key=lambda x: x["final_score"], reverse=True)
    return new_top
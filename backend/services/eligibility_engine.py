"""
Eligibility Engine — Rule-based logic for scheme matching.
"""
from typing import List
from models import Scheme
from schemas import EligibilityCriteria


def get_eligible_schemes(profile: EligibilityCriteria, all_schemes: List[Scheme]) -> List[Scheme]:
    """
    Check eligibility against all schemes using structured rule-based logic.
    Uses the min_age, max_age, max_income, and target_categories fields on Scheme.
    """
    eligible = []

    for scheme in all_schemes:
        if not _check_age(profile.age, scheme):
            continue
        if not _check_income(profile.income, scheme):
            continue
        if not _check_category(profile.category, scheme):
            continue
        eligible.append(scheme)

    return eligible


def _check_age(age: int, scheme: Scheme) -> bool:
    """Check if user's age falls within scheme range."""
    min_age = scheme.min_age or 0
    max_age = scheme.max_age or 100
    return min_age <= age <= max_age


def _check_income(income: float, scheme: Scheme) -> bool:
    """Check if user's income is within scheme limits. 0 means no limit."""
    max_income = scheme.max_income or 0
    if max_income <= 0:
        return True  # No income restriction
    return income <= max_income


def _check_category(category: str, scheme: Scheme) -> bool:
    """Check if user's category matches scheme target categories."""
    target = scheme.target_categories or "All"
    if target.strip().lower() == "all":
        return True
    allowed = [c.strip().upper() for c in target.split(",")]
    return category.strip().upper() in allowed

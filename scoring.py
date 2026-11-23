"""Scoring and action plan logic of the CSR pre-assessment.

Kept separate from the interface so it can be tested on its own.
"""

from dataclasses import dataclass

from questionnaire import (
    HIGHER_RISK_REGIONS,
    PILLARS,
    QUESTIONS,
    SECTOR_WEIGHTS,
    Question,
)

MAX_ANSWER = 3

LEVELS = [
    (65, {"fr": "Avancé", "en": "Advanced", "ja": "先進的"}),
    (45, {"fr": "Solide", "en": "Good", "ja": "良好"}),
    (25, {"fr": "Partiel", "en": "Partial", "ja": "部分的"}),
    (0, {"fr": "Insuffisant", "en": "Insufficient", "ja": "不十分"}),
]

# Multipliers used to rank actions
INTERNATIONAL_BOOST = 1.2  # entity active in 3 regions or more
RISK_BOOST = 1.3  # entity active in at least one higher-risk region


@dataclass
class Profile:
    sector: str  # key of SECTORS
    entity_type: str  # key of ENTITY_TYPES
    regions: list  # keys of REGIONS

    @property
    def is_international(self) -> bool:
        return len(self.regions) >= 3

    @property
    def has_higher_risk_region(self) -> bool:
        return any(r in HIGHER_RISK_REGIONS for r in self.regions)


@dataclass
class Action:
    question: Question
    answer: int
    priority: float
    quick_win: bool


@dataclass
class Result:
    pillar_scores: dict  # pillar -> score out of 100
    overall: float
    level: dict  # {"fr": ..., "en": ...}
    actions: list  # list of Action, highest priority first
    regulations: list  # regulation keys linked to weak answers
    strengths: list  # questions answered at the top level


def level_for(score: float) -> dict:
    for threshold, label in LEVELS:
        if score >= threshold:
            return label
    return LEVELS[-1][1]


def pillar_scores(answers: dict) -> dict:
    """Score of each theme out of 100. Missing answers count as 0."""
    scores = {}
    for pillar in PILLARS:
        qs = [q for q in QUESTIONS if q.pillar == pillar]
        total = sum(answers.get(q.id, 0) for q in qs)
        scores[pillar] = round(100 * total / (MAX_ANSWER * len(qs)), 1)
    return scores


def overall_score(scores: dict, sector: str) -> float:
    weights = SECTOR_WEIGHTS[sector]
    return round(sum(scores[p] * weights[p] for p in PILLARS), 1)


def action_priority(q: Question, answer: int, profile: Profile) -> float:
    """Higher means more urgent. Zero when the question is fully covered."""
    gap = MAX_ANSWER - answer
    if gap <= 0:
        return 0.0
    priority = q.impact * (4 - q.effort) * gap
    priority *= q.sector_boost.get(profile.sector, 1.0)
    if q.international and profile.is_international:
        priority *= INTERNATIONAL_BOOST
    if q.risk_sensitive and profile.has_higher_risk_region:
        priority *= RISK_BOOST
    return round(priority, 2)


def is_quick_win(q: Question, answer: int) -> bool:
    return answer < MAX_ANSWER and q.effort == 1 and q.impact >= 2


def evaluate(answers: dict, profile: Profile) -> Result:
    scores = pillar_scores(answers)
    overall = overall_score(scores, profile.sector)

    actions = []
    for q in QUESTIONS:
        a = answers.get(q.id, 0)
        p = action_priority(q, a, profile)
        if p > 0:
            actions.append(Action(q, a, p, is_quick_win(q, a)))
    actions.sort(key=lambda x: x.priority, reverse=True)

    regulations = []
    for q in QUESTIONS:
        if answers.get(q.id, 0) <= 1:
            for reg in q.regulations:
                if reg not in regulations:
                    regulations.append(reg)

    strengths = [q for q in QUESTIONS if answers.get(q.id, 0) == MAX_ANSWER]

    return Result(scores, overall, level_for(overall), actions, regulations, strengths)

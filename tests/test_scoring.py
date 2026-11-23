import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from questionnaire import PILLARS, QUESTIONS, SECTOR_WEIGHTS  # noqa: E402
from scoring import Profile, evaluate, level_for  # noqa: E402

PROFILE = Profile(sector="IT", entity_type="SUB", regions=["EU"])


def all_answers(value):
    return {q.id: value for q in QUESTIONS}


def test_weights_sum_to_one():
    for sector, weights in SECTOR_WEIGHTS.items():
        assert abs(sum(weights.values()) - 1) < 1e-9, sector
        assert set(weights) == set(PILLARS)


def test_every_question_has_both_languages():
    for q in QUESTIONS:
        for field in (q.text, q.help, q.action):
            assert field.get("fr") and field.get("en"), q.id


def test_five_questions_per_pillar():
    for pillar in PILLARS:
        assert len([q for q in QUESTIONS if q.pillar == pillar]) == 5


def test_empty_answers_give_zero_and_full_plan():
    result = evaluate({}, PROFILE)
    assert result.overall == 0
    assert all(s == 0 for s in result.pillar_scores.values())
    assert len(result.actions) == len(QUESTIONS)
    assert result.level["en"] == "Insufficient"


def test_full_answers_give_100_and_no_action():
    result = evaluate(all_answers(3), PROFILE)
    assert result.overall == 100
    assert result.actions == []
    assert result.regulations == []
    assert len(result.strengths) == len(QUESTIONS)


def test_middle_answers():
    result = evaluate(all_answers(2), PROFILE)
    assert round(result.overall, 1) == 66.7
    assert result.level["fr"] == "Avancé"


def test_actions_sorted_by_priority():
    result = evaluate({}, PROFILE)
    priorities = [a.priority for a in result.actions]
    assert priorities == sorted(priorities, reverse=True)


def test_sector_boost_changes_ranking():
    it = evaluate({}, Profile("IT", "SUB", ["EU"]))
    scm = evaluate({}, Profile("SCM", "SUB", ["EU"]))
    rank_it = [a.question.id for a in it.actions].index("ENV4")
    rank_scm = [a.question.id for a in scm.actions].index("ENV4")
    assert rank_it < rank_scm


def test_higher_risk_region_raises_due_diligence_priority():
    eu = evaluate({}, Profile("SCM", "SUP", ["EU"]))
    apac = evaluate({}, Profile("SCM", "SUP", ["EU", "APAC"]))
    p_eu = next(a.priority for a in eu.actions if a.question.id == "ACH2")
    p_apac = next(a.priority for a in apac.actions if a.question.id == "ACH2")
    assert p_apac > p_eu


def test_weak_answers_list_regulations():
    answers = all_answers(3)
    answers["ACH2"] = 0
    result = evaluate(answers, PROFILE)
    assert "VIGILANCE" in result.regulations
    assert "CSDDD" in result.regulations


def test_levels():
    assert level_for(10)["en"] == "Insufficient"
    assert level_for(30)["en"] == "Partial"
    assert level_for(50)["en"] == "Good"
    assert level_for(80)["en"] == "Advanced"

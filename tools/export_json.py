"""Export the questionnaire to docs/questionnaire.json for the web version.

The GitHub Pages version (docs/index.html) reads this file, so questions and
weights stay defined in one place: questionnaire.py.
Run from the repository root:  python tools/export_json.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import questionnaire as qn  # noqa: E402
import scoring  # noqa: E402
from i18n import TEXTS  # noqa: E402

data = {
    "texts": TEXTS,
    "answer_scale": {lang: {str(k): v for k, v in scale.items()} for lang, scale in qn.ANSWER_SCALE.items()},
    "pillars": qn.PILLARS,
    "sectors": qn.SECTORS,
    "entity_types": qn.ENTITY_TYPES,
    "regions": qn.REGIONS,
    "higher_risk_regions": sorted(qn.HIGHER_RISK_REGIONS),
    "regulations": qn.REGULATIONS,
    "sector_weights": qn.SECTOR_WEIGHTS,
    "levels": [{"threshold": th, "label": label} for th, label in scoring.LEVELS],
    "international_boost": scoring.INTERNATIONAL_BOOST,
    "risk_boost": scoring.RISK_BOOST,
    "questions": [
        {
            "id": q.id,
            "pillar": q.pillar,
            "text": q.text,
            "help": q.help,
            "action": q.action,
            "impact": q.impact,
            "effort": q.effort,
            "regulations": list(q.regulations),
            "sector_boost": q.sector_boost,
            "international": q.international,
            "risk_sensitive": q.risk_sensitive,
        }
        for q in qn.QUESTIONS
    ],
}

out = ROOT / "docs" / "questionnaire.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Wrote {out.relative_to(ROOT)} ({len(data['questions'])} questions)")

# Checklist of generic improvement actions (docs/checklist.html)
sys.path.insert(0, str(ROOT / "tools"))
from checklist_data import as_json  # noqa: E402

checklist = as_json()
out2 = ROOT / "docs" / "checklist.json"
out2.write_text(json.dumps(checklist, ensure_ascii=False, indent=1), encoding="utf-8")
total = sum(len(c["items"]) for c in checklist)
print(f"Wrote {out2.relative_to(ROOT)} ({len(checklist)} categories, {total} actions)")

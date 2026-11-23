"""The PDF report stays short: two pages, in every language."""
import re

import pytest

from report import build_pdf
from scoring import Profile, evaluate

DEMO = dict(ENV1=2, ENV2=1, ENV3=0, ENV4=1, ENV5=2, SOC1=3, SOC2=2, SOC3=2, SOC4=1, SOC5=0,
            ETH1=3, ETH2=1, ETH3=2, ETH4=3, ETH5=2, ACH1=2, ACH2=0, ACH3=1, ACH4=0, ACH5=1)


@pytest.mark.parametrize("lang", ["fr", "en", "ja"])
@pytest.mark.parametrize("answers", [DEMO, {}, {k: 3 for k in DEMO}])
def test_report_has_two_pages(lang, answers):
    profile = Profile(sector="IT", entity_type="SUB", regions=["EU", "APAC", "NA"])
    pdf = build_pdf(evaluate(answers, profile), profile, "Test", lang)
    assert pdf.startswith(b"%PDF")
    assert len(re.findall(rb"/Type /Page[^s]", pdf)) == 2

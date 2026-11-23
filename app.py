"""CSR pre-assessment for IT and supply chain (Streamlit app).

Run locally with:  streamlit run app.py
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from i18n import t
from questionnaire import (
    ANSWER_SCALE,
    ENTITY_TYPES,
    PILLARS,
    QUESTIONS,
    REGIONS,
    REGULATIONS,
    SECTORS,
    questions_by_pillar,
)
from report import build_pdf
from scoring import Profile, evaluate

st.set_page_config(page_title="CSR pre-assessment", page_icon="🌱", layout="wide")

# Language
with st.sidebar:
    lang_label = st.radio("Langue / Language", ["Français", "English"], horizontal=True)
lang = "fr" if lang_label == "Français" else "en"

st.title(t(lang, "app_title"))
st.write(t(lang, "tagline"))
st.caption(t(lang, "disclaimer"))

# 1. Profile
st.header(t(lang, "step_profile"))
c1, c2 = st.columns(2)
with c1:
    entity_name = st.text_input(
        t(lang, "entity_name"),
        placeholder=t(lang, "entity_name_placeholder"),
        key="entity_name",
    )
    sector = st.selectbox(
        t(lang, "sector"), list(SECTORS),
        format_func=lambda k: SECTORS[k][lang], key="sector",
    )
with c2:
    entity_type = st.selectbox(
        t(lang, "entity_type"), list(ENTITY_TYPES),
        format_func=lambda k: ENTITY_TYPES[k][lang], key="entity_type",
    )
    regions = st.multiselect(
        t(lang, "regions"), list(REGIONS), default=["EU"],
        format_func=lambda k: REGIONS[k][lang], key="regions",
        help=t(lang, "regions_help"),
    )

profile = Profile(sector=sector, entity_type=entity_type, regions=regions)
if profile.is_international:
    st.info(t(lang, "international_flag"))
if profile.has_higher_risk_region:
    st.info(t(lang, "risk_flag"))

# 2. Questionnaire
st.header(t(lang, "step_questions"))
with st.expander(t(lang, "scale_title")):
    for value, label in ANSWER_SCALE[lang].items():
        st.write(f"**{value}** : {label}" if lang == "fr" else f"**{value}**: {label}")

answers = {}
tabs = st.tabs([PILLARS[p][lang] for p in PILLARS])
for tab, pillar in zip(tabs, PILLARS):
    with tab:
        for q in questions_by_pillar(pillar):
            choice = st.radio(
                q.text[lang],
                options=[0, 1, 2, 3],
                index=None,
                format_func=lambda v: ANSWER_SCALE[lang][v],
                help=q.help[lang],
                key=f"q_{q.id}",
            )
            if choice is not None:
                answers[q.id] = choice

answered = len(answers)
st.progress(answered / len(QUESTIONS), text=f"{answered}/{len(QUESTIONS)} {t(lang, 'progress')}")

# 3. Results
st.header(t(lang, "results"))
result = evaluate(answers, profile)

m1, m2 = st.columns(2)
m1.metric(t(lang, "overall"), f"{result.overall:.0f}/100")
m2.metric(t(lang, "level"), result.level[lang])

labels = [PILLARS[p][lang] for p in PILLARS]
values = [result.pillar_scores[p] for p in PILLARS]
radar = go.Figure(
    go.Scatterpolar(
        r=values + values[:1],
        theta=labels + labels[:1],
        fill="toself",
        line_color="#1F6F50",
        fillcolor="rgba(31, 111, 80, 0.25)",
    )
)
radar.update_layout(
    title=t(lang, "radar_title"),
    polar=dict(radialaxis=dict(range=[0, 100], tickvals=[25, 50, 75, 100])),
    showlegend=False,
    height=420,
    margin=dict(l=60, r=60, t=60, b=40),
)

left, right = st.columns([1, 1])
with left:
    st.plotly_chart(radar, use_container_width=True)
with right:
    st.subheader(t(lang, "regulations"))
    if result.regulations:
        for reg in result.regulations:
            st.write(f"- {REGULATIONS[reg][lang]}")
        st.caption(t(lang, "regulations_help"))
    else:
        st.write(t(lang, "no_regulation"))

    st.subheader(t(lang, "strengths"))
    if result.strengths:
        for q in result.strengths:
            st.write(f"- {q.text[lang]}")
    else:
        st.write(t(lang, "no_strength"))

st.subheader(t(lang, "action_plan"))
if result.actions:
    plan = pd.DataFrame(
        [
            {
                "#": i,
                t(lang, "theme"): PILLARS[a.question.pillar][lang],
                t(lang, "action"): a.question.action[lang],
                t(lang, "quick_win"): "✓" if a.quick_win else "",
                t(lang, "priority"): a.priority,
            }
            for i, a in enumerate(result.actions, start=1)
        ]
    )
    st.dataframe(plan, hide_index=True, use_container_width=True)

# Downloads
d1, d2 = st.columns(2)
with d1:
    st.download_button(
        t(lang, "download_pdf"),
        data=build_pdf(result, profile, entity_name, lang),
        file_name="csr_pre_assessment.pdf",
        mime="application/pdf",
        type="primary",
    )
with d2:
    rows = [
        {
            "question_id": q.id,
            "theme": PILLARS[q.pillar][lang],
            "question": q.text[lang],
            "answer": answers.get(q.id, ""),
        }
        for q in QUESTIONS
    ]
    st.download_button(
        t(lang, "download_csv"),
        data=pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),
        file_name="csr_pre_assessment_answers.csv",
        mime="text/csv",
    )

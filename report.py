"""PDF report of the CSR pre-assessment (built with ReportLab)."""

from datetime import date
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from i18n import t
from questionnaire import ENTITY_TYPES, PILLARS, REGIONS, REGULATIONS, SECTORS

GREEN = colors.HexColor("#1F6F50")
LIGHT = colors.HexColor("#E8F1EC")
GREY = colors.HexColor("#5F6B66")


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Title"], textColor=GREEN, fontSize=20, spaceAfter=4),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], textColor=GREEN, fontSize=13, spaceBefore=10, spaceAfter=4),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontSize=9.5, leading=13),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontSize=8, leading=10, textColor=GREY),
        "cell": ParagraphStyle("cell", parent=base["BodyText"], fontSize=8.5, leading=11),
    }


def _bars(scores: dict, lang: str) -> Drawing:
    """Horizontal bars, one per theme."""
    width, row = 170 * mm, 9 * mm
    label_w, bar_w = 62 * mm, 90 * mm
    d = Drawing(width, row * len(scores))
    for i, (pillar, score) in enumerate(scores.items()):
        y = row * (len(scores) - 1 - i) + 2 * mm
        d.add(String(0, y + 1.5 * mm, PILLARS[pillar][lang], fontName="Helvetica", fontSize=9, fillColor=colors.black))
        d.add(Rect(label_w, y, bar_w, 5 * mm, fillColor=LIGHT, strokeColor=None))
        d.add(Rect(label_w, y, bar_w * score / 100, 5 * mm, fillColor=GREEN, strokeColor=None))
        d.add(String(label_w + bar_w + 3 * mm, y + 1.5 * mm, f"{score:.0f}/100", fontName="Helvetica", fontSize=9))
    return d


def build_pdf(result, profile, entity_name: str, lang: str) -> bytes:
    s = _styles()
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
        title=t(lang, "report_title"),
    )
    name = entity_name.strip() or t(lang, "unnamed")
    sep = " : " if lang == "fr" else ": "
    regions = ", ".join(REGIONS[r][lang] for r in profile.regions) or "-"

    story = [
        Paragraph(t(lang, "report_title"), s["title"]),
        Paragraph(
            f"<b>{t(lang, 'report_entity')}</b>{sep}{escape(name)}<br/>"
            f"<b>{t(lang, 'sector')}</b>{sep}{SECTORS[profile.sector][lang]}<br/>"
            f"<b>{t(lang, 'entity_type')}</b>{sep}{ENTITY_TYPES[profile.entity_type][lang]}<br/>"
            f"<b>{t(lang, 'regions')}</b>{sep}{regions}<br/>"
            f"<b>{t(lang, 'report_date')}</b>{sep}{date.today().strftime('%d/%m/%Y')}",
            s["body"],
        ),
        Spacer(1, 6 * mm),
        Paragraph(
            f"<font size=14><b>{t(lang, 'overall')}{sep}{result.overall:.0f}/100</b></font>"
            f"&nbsp;&nbsp;&nbsp;{t(lang, 'level')}{sep}<b>{result.level[lang]}</b>",
            s["body"],
        ),
        Paragraph(t(lang, "by_theme"), s["h2"]),
        _bars(result.pillar_scores, lang),
    ]

    # Action plan
    story.append(Paragraph(t(lang, "report_top_actions"), s["h2"]))
    rows = [["#", t(lang, "theme"), t(lang, "action"), t(lang, "quick_win")]]
    for i, a in enumerate(result.actions[:10], start=1):
        rows.append([
            str(i),
            Paragraph(PILLARS[a.question.pillar][lang], s["cell"]),
            Paragraph(escape(a.question.action[lang]), s["cell"]),
            "X" if a.quick_win else "",
        ])
    if len(rows) > 1:
        table = Table(rows, colWidths=[8 * mm, 36 * mm, 104 * mm, 26 * mm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), GREEN),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, 0), 8.5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (3, 1), (3, -1), "CENTER"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#C9D6CF")),
        ]))
        story.append(table)
    else:
        story.append(Paragraph("-", s["body"]))

    # Regulations
    story.append(Paragraph(t(lang, "regulations"), s["h2"]))
    if result.regulations:
        items = "<br/>".join(f"&bull; {REGULATIONS[r][lang]}" for r in result.regulations)
        story.append(Paragraph(items, s["body"]))
        story.append(Paragraph(t(lang, "regulations_help"), s["small"]))
    else:
        story.append(Paragraph(t(lang, "no_regulation"), s["body"]))

    # Strengths
    story.append(Paragraph(t(lang, "strengths"), s["h2"]))
    if result.strengths:
        items = "<br/>".join(f"&bull; {escape(q.text[lang])}" for q in result.strengths)
        story.append(Paragraph(items, s["body"]))
    else:
        story.append(Paragraph(t(lang, "no_strength"), s["body"]))

    story += [
        Paragraph(t(lang, "methodology"), s["h2"]),
        Paragraph(t(lang, "methodology_text"), s["small"]),
        Spacer(1, 3 * mm),
        Paragraph(t(lang, "disclaimer"), s["small"]),
    ]

    doc.build(story)
    return buf.getvalue()

"""PDF report of the CSR pre-assessment (built with ReportLab).

Two pages, same layout as the web version:
page 1 is a synthesis (score, level, themes, regulations, 3 priorities),
page 2 is the short action plan with strengths and method.
"""

from datetime import date
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from i18n import t
from questionnaire import ENTITY_TYPES, PILLARS, REGIONS, REGULATIONS, SECTORS

INK = colors.HexColor("#14211C")
INK_2 = colors.HexColor("#3E4E47")
MUTED = colors.HexColor("#66746E")
PAPER = colors.HexColor("#F3F5F1")
MIST = colors.HexColor("#E4EBE5")
LINE = colors.HexColor("#D4DCD6")
PINE = colors.HexColor("#1E5B45")
PINE_DEEP = colors.HexColor("#123B2C")
MOSS = colors.HexColor("#6E9C82")
AMBER_SOFT = colors.HexColor("#FBF0D4")
AMBER_INK = colors.HexColor("#6E4F05")
DANGER_SOFT = colors.HexColor("#F6E3D4")

TOOL_URL = "constanceweber6-alt.github.io/rse-prediagnostic"
PAGE_W, PAGE_H = A4
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM = 18 * mm, 30 * mm, 22 * mm

# Texts only used in the PDF
PDF_TEXTS = {
    "tool": {"fr": "Pré-diagnostic RSE", "en": "CSR pre-assessment", "ja": "CSR簡易診断"},
    "priorities": {"fr": "Vos 3 priorités", "en": "Your 3 priorities", "ja": "優先すべき3つの取り組み"},
    "to_track": {"fr": "À suivre", "en": "To track", "ja": "追跡指標"},
    "plan_sub": {
        "fr": "Les actions les plus utiles, classées par priorité. La liste complète est dans l'outil en ligne.",
        "en": "The most useful actions, ranked by priority. The full list is in the online tool.",
        "ja": "効果の高い取り組みを優先順に掲載しています。全項目はオンラインツールで確認できます。",
    },
    "regulatory": {"fr": "Réglementaire", "en": "Regulatory", "ja": "規制関連"},
    "all_done": {
        "fr": "Toutes les pratiques sont déployées et mesurées. Bravo.",
        "en": "Every practice is rolled out and measured. Well done.",
        "ja": "すべての取り組みが展開・測定されています。",
    },
    "free_tool": {"fr": "Outil gratuit : ", "en": "Free tool: ", "ja": "無料ツール："},
}
VERDICTS = {
    "fr": {
        "Insuffisant": "Les fondations restent à poser. Commencez par les actions rapides : elles rassurent vite vos clients et vos équipes.",
        "Partiel": "Des initiatives existent mais manquent de cadre. Formalisez vos politiques et choisissez quelques indicateurs à suivre.",
        "Solide": "La démarche est structurée. L'enjeu est maintenant de la déployer dans tous les pays et d'en mesurer les résultats.",
        "Avancé": "Démarche mature. Concentrez vos efforts sur la chaîne d'approvisionnement et sur la preuve des résultats.",
    },
    "en": {
        "Insufficient": "The foundations are still to be laid. Start with the quick wins: they reassure customers and teams fast.",
        "Partial": "Initiatives exist but lack a framework. Formalise your policies and pick a few KPIs to track.",
        "Good": "The approach is structured. The next step is to deploy it in every country and measure the results.",
        "Advanced": "A mature approach. Focus on the supply chain and on proving results.",
    },
    "ja": {
        "不十分": "まだ基盤づくりの段階です。すぐに着手できる施策から始めると、顧客や社内の安心につながります。",
        "部分的": "取り組みはあるものの、仕組みが整っていません。方針を文書化し、追跡する指標をいくつか決めましょう。",
        "良好": "体制は整っています。次はすべての国に展開し、成果を測定することが課題です。",
        "先進的": "成熟した取り組みです。サプライチェーンと成果の証明に注力しましょう。",
    },
}
# Level pill colours, from the most advanced level to the least
LEVEL_COLORS = [(PINE, colors.white), (MOSS, colors.white), (AMBER_SOFT, AMBER_INK), (DANGER_SOFT, colors.HexColor("#7A2E12"))]
LEVEL_ORDER = {"fr": ["Avancé", "Solide", "Partiel", "Insuffisant"], "en": ["Advanced", "Good", "Partial", "Insufficient"], "ja": ["先進的", "良好", "部分的", "不十分"]}

# Japanese font: IPA Gothic is embedded when installed (see packages.txt for
# Streamlit Cloud). Otherwise fall back to a built-in CID font, which most PDF
# readers display but which is not embedded in the file.
IPA_PATHS = [
    "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
    "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
    "/Library/Fonts/ipag.ttf",
]


def _register_japanese_font() -> str:
    for path in IPA_PATHS:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont("IPAGothic", path))
            return "IPAGothic"
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    return "HeiseiKakuGo-W5"


JA_FONT = _register_japanese_font()


def _font(lang: str, bold: bool = False) -> str:
    if lang == "ja":
        return JA_FONT
    return "Helvetica-Bold" if bold else "Helvetica"


def _p(key: str, lang: str) -> str:
    return PDF_TEXTS[key][lang]


def _styles(lang: str) -> dict:
    extra = {"wordWrap": "CJK"} if lang == "ja" else {}
    reg, bold = _font(lang), _font(lang, bold=True)

    def st(name, **kw):
        base = {"fontName": reg, "fontSize": 10, "leading": 14, "textColor": INK}
        base.update(kw)
        return ParagraphStyle(name, **base, **extra)

    return {
        "title": st("title", fontName=bold, fontSize=24, leading=28, spaceAfter=4 * mm),
        "h2": st("h2", fontName=bold, fontSize=15, leading=19, spaceAfter=2 * mm),
        "label": st("label", fontName=bold, fontSize=8.5, leading=11, textColor=MUTED, spaceAfter=3 * mm),
        "meta_k": st("meta_k", fontSize=7.5, leading=10, textColor=MUTED),
        "meta_v": st("meta_v", fontSize=9, leading=12),
        "body": st("body", fontSize=10, leading=14),
        "lead": st("lead", fontSize=10, leading=14, textColor=INK_2, spaceAfter=6 * mm),
        "verdict": st("verdict", fontSize=11, leading=15.5),
        "score": st("score", fontName="Helvetica-Bold", fontSize=46, leading=48),
        "pill": st("pill", fontName=bold, fontSize=9, leading=11),
        "act": st("act", fontName=bold, fontSize=10.5, leading=14),
        "sub": st("sub", fontSize=8.5, leading=12, textColor=MUTED),
        "num": st("num", fontName="Helvetica-Bold", fontSize=20, leading=22),
        "cell": st("cell", fontSize=9.5, leading=13),
        "cell_head": st("cell_head", fontName=bold, fontSize=8, leading=10, textColor=MUTED),
        "cell_num": st("cell_num", fontName="Helvetica-Bold", fontSize=9.5, leading=13),
        "list": st("list", fontSize=9.5, leading=13.5, leftIndent=4 * mm, bulletIndent=0),
        "fine": st("fine", fontSize=7.8, leading=10.5, textColor=MUTED, spaceAfter=2 * mm),
        "empty": st("empty", fontSize=9.5, leading=13, textColor=MUTED),
    }


def _bars(scores: dict, lang: str, width: float) -> Drawing:
    """One bar per theme: label and score on top, thin track below."""
    row = 9 * mm
    d = Drawing(width, row * len(scores))
    for i, (pillar, score) in enumerate(scores.items()):
        y = row * (len(scores) - 1 - i)
        d.add(String(0, y + 4.2 * mm, PILLARS[pillar][lang], fontName=_font(lang), fontSize=9, fillColor=INK))
        d.add(String(width, y + 4.2 * mm, f"{score:.0f}", fontName="Helvetica-Bold", fontSize=9, fillColor=INK, textAnchor="end"))
        d.add(Rect(0, y + 1.2 * mm, width, 2.4 * mm, fillColor=MIST, strokeColor=None))
        d.add(Rect(0, y + 1.2 * mm, max(width * score / 100, 0.6 * mm), 2.4 * mm, fillColor=PINE, strokeColor=None))
    return d


def _tag(text: str, bg, fg, lang: str) -> str:
    # Inline tag drawn with a background colour behind the text
    return f'<font name="{_font(lang, True)}" size="7.5" color="{fg.hexval()}" backColor="{bg.hexval()}">&nbsp;{escape(text)}&nbsp;</font>'


def build_pdf(result, profile, entity_name: str, lang: str) -> bytes:
    s = _styles(lang)
    buf = BytesIO()
    today = date.today()
    date_txt = (
        f"{today.year}年{today.month}月{today.day}日" if lang == "ja"
        else today.strftime("%d/%m/%Y") if lang == "fr" else today.strftime("%d %B %Y")
    )
    content_w = PAGE_W - 2 * MARGIN_X - 12  # frame keeps 6 pt padding on each side

    def decorate(canvas, doc):
        canvas.saveState()
        X0, X1 = MARGIN_X + 6, PAGE_W - MARGIN_X - 6  # align with the frame content
        top = PAGE_H - 16 * mm
        canvas.setFont(_font(lang, True), 10)
        canvas.setFillColor(INK)
        canvas.drawString(X0, top, _p("tool", lang))
        canvas.setFont(_font(lang), 9)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - X0, top, date_txt)
        canvas.setStrokeColor(INK)
        canvas.setLineWidth(1.2)
        canvas.line(X0, top - 4 * mm, PAGE_W - X0, top - 4 * mm)
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(X0, 16 * mm, PAGE_W - X0, 16 * mm)
        canvas.setFont(_font(lang), 7.5)
        canvas.drawString(X0, 11 * mm, _p("free_tool", lang) + TOOL_URL)
        page = f"{doc.page} / 2"
        canvas.drawRightString(PAGE_W - X0, 11 * mm, page)
        canvas.restoreState()

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X, topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
        title=t(lang, "report_title"), author="CSR pre-assessment",
    )
    name = entity_name.strip() or t(lang, "unnamed")
    sep = {"fr": " : ", "en": ": ", "ja": "："}[lang]
    regions = ("、" if lang == "ja" else ", ").join(REGIONS[r][lang] for r in profile.regions) or "-"
    level = result.level[lang]
    order = LEVEL_ORDER[lang]
    bg, fg = LEVEL_COLORS[order.index(level)] if level in order else (MIST, INK)

    # ---------- Page 1: synthesis ----------
    story = [Paragraph(escape(name), s["title"])]
    meta = Table(
        [[Paragraph(t(lang, k), s["meta_k"]) for k in ("sector", "entity_type", "regions")],
         [Paragraph(SECTORS[profile.sector][lang], s["meta_v"]),
          Paragraph(ENTITY_TYPES[profile.entity_type][lang], s["meta_v"]),
          Paragraph(regions, s["meta_v"])]],
        colWidths=[content_w * 0.28, content_w * 0.24, content_w * 0.48],
    )
    meta.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                              ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6 * mm),
                              ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [meta, Spacer(1, 8 * mm)]

    pill_w = pdfmetrics.stringWidth(level, _font(lang, True), 9) + 6.5 * mm
    pill = Table([[Paragraph(escape(level), ParagraphStyle("p", parent=s["pill"], textColor=fg))]], colWidths=[pill_w])
    pill.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("ROUNDEDCORNERS", [8, 8, 8, 8]),
                              ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                              ("TOPPADDING", (0, 0), (-1, -1), 0.8 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm)]))
    pill.hAlign = "LEFT"
    score = Paragraph(f'{result.overall:.0f}<font size="13" color="{MUTED.hexval()}"> /100</font>', s["score"])
    verdict = Table([[score, [pill, Spacer(1, 2.5 * mm), Paragraph(escape(VERDICTS[lang].get(level, "")), s["verdict"])]]],
                    colWidths=[44 * mm, content_w - 44 * mm])
    verdict.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PAPER), ("ROUNDEDCORNERS", [10, 10, 10, 10]),
                                 ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 7 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 7 * mm),
                                 ("TOPPADDING", (0, 0), (-1, -1), 7 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 7 * mm)]))
    story += [verdict, Spacer(1, 9 * mm)]

    left_w, gap = content_w * 0.55, 10 * mm
    right_w = content_w - left_w - gap
    regs = ([Paragraph(escape(REGULATIONS[r][lang]), s["list"], bulletText="•") for r in result.regulations[:6]]
            or [Paragraph(t(lang, "no_regulation"), s["empty"])])
    cols = Table([[[Paragraph(t(lang, "by_theme"), s["label"]), _bars(result.pillar_scores, lang, left_w)],
                   "", [Paragraph(t(lang, "regulations"), s["label"])] + regs]],
                 colWidths=[left_w, gap, right_w])
    cols.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0)]))
    story += [cols, Spacer(1, 9 * mm), Paragraph(_p("priorities", lang), s["label"])]

    def tags(a):
        out = [_tag(PILLARS[a.question.pillar][lang], MIST, PINE_DEEP, lang)]
        if a.quick_win:
            out.append(_tag(t(lang, "quick_win"), AMBER_SOFT, AMBER_INK, lang))
        if a.question.regulations:
            out.append(_tag(_p("regulatory", lang), colors.HexColor("#EEF0EE"), INK_2, lang))
        return " ".join(out)

    prio = result.actions[:3]
    if prio:
        rows = []
        for i, a in enumerate(prio, start=1):
            kpi = a.question.kpi.get(lang, "") if a.question.kpi else ""
            sub = tags(a) + (f"&nbsp;&nbsp;{_p('to_track', lang)}{sep}{escape(kpi)}" if kpi else "")
            rows.append([Paragraph(str(i), s["num"]), [Paragraph(escape(a.question.action[lang]), s["act"]), Spacer(1, 1.2 * mm), Paragraph(sub, s["sub"])]])
        pt = Table(rows, colWidths=[12 * mm, content_w - 12 * mm])
        pt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5 * mm)]))
        story.append(pt)
    else:
        story.append(Paragraph(_p("all_done", lang), s["empty"]))

    # ---------- Page 2: action plan ----------
    story += [PageBreak(), Paragraph(t(lang, "action_plan"), s["h2"]), Paragraph(_p("plan_sub", lang), s["lead"])]
    plan = result.actions[:8]
    if plan:
        rows = [[Paragraph("#", s["cell_head"]), Paragraph(t(lang, "action"), s["cell_head"]), Paragraph(t(lang, "theme"), s["cell_head"])]]
        for i, a in enumerate(plan, start=1):
            act = escape(a.question.action[lang]) + ("&nbsp;&nbsp;" + _tag(t(lang, "quick_win"), AMBER_SOFT, AMBER_INK, lang) if a.quick_win else "")
            rows.append([Paragraph(str(i), s["cell_num"]), Paragraph(act, s["cell"]), Paragraph(PILLARS[a.question.pillar][lang], s["cell"])])
        table = Table(rows, colWidths=[9 * mm, content_w - 9 * mm - 46 * mm, 46 * mm], repeatRows=1)
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
            ("TOPPADDING", (0, 1), (-1, -1), 3 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ("LINEBELOW", (0, 0), (-1, 0), 1, INK),
            ("LINEBELOW", (0, 1), (-1, -1), 0.5, LINE),
        ]))
        story.append(table)
    else:
        story.append(Paragraph(_p("all_done", lang), s["empty"]))

    story += [Spacer(1, 8 * mm), Paragraph(t(lang, "strengths"), s["label"])]
    if result.strengths:
        counts = {}
        for q in result.strengths:
            counts[q.pillar] = counts.get(q.pillar, 0) + 1
        for pillar, n in counts.items():
            story.append(Paragraph(f"{PILLARS[pillar][lang]}{sep}{_strength_count(n, lang)}", s["list"], bulletText="•"))
    else:
        story.append(Paragraph(t(lang, "no_strength"), s["empty"]))

    story += [Spacer(1, 10 * mm), KeepTogether([
        Paragraph(f"<b>{t(lang, 'methodology')}</b>{sep}{t(lang, 'methodology_text')}", s["fine"]),
        Paragraph(t(lang, "disclaimer"), s["fine"]),
    ])]

    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    return buf.getvalue()


def _strength_count(n: int, lang: str) -> str:
    if lang == "fr":
        pl = "s" if n > 1 else ""
        return f"{n} pratique{pl} déployée{pl} et mesurée{pl} partout"
    if lang == "ja":
        return f"全拠点で展開・測定済みの取り組み{n}件"
    return f"{n} practice{'s' if n > 1 else ''} rolled out and measured everywhere"

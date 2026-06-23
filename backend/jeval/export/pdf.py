"""Рендер карточки предварительной оценки должности в PDF (раздел 10 методики).

Кнопка «Экспорт в PDF» на `EvaluationCardPage.tsx` — подписываемый документ
для досье Оценочного комитета, в отличие от `window.print()` (распечатка
HTML-вёрстки браузера, не годится для архива/подписи). Содержание зеркалит
карточку на экране: баллы, грейд, профиль, формула, QC-флаги, обоснование,
резюме и рекомендация для комитета.
"""

from __future__ import annotations

from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from ..domain.models import Evaluation, JobDossier, QCFlag, ScoreResult
from .fonts import register_cyrillic_font

_ACCENT_HEX, _WARN_HEX, _OK_HEX = "#b3261e", "#9a6700", "#1a7f37"
_ACCENT = colors.HexColor(_ACCENT_HEX)
_WARN = colors.HexColor(_WARN_HEX)
_OK = colors.HexColor(_OK_HEX)
_MUTED = colors.HexColor("#6b6b6b")
_BORDER = colors.HexColor("#d8d3ca")

_STATUS_LABEL = {
    "ready": "Готово к комитету",
    "needs_clarification": "Требуются уточнения",
    "cannot_evaluate": "Оценка невозможна",
}
_STATUS_SUMMARY = {
    "ready": "Баллы рассчитаны, а блокирующих проблем по данным нет. Карточку можно выносить на Оценочный комитет.",
    "needs_clarification": "Баллы уже есть, но есть уточнения или QC-флаги. Карточка предварительная и требует подтверждения спорных мест.",
    "cannot_evaluate": "Критических данных недостаточно. Уровни факторов, баллы и грейд не присваиваются, пока досье не будет доработано.",
}
_CONFIDENCE_LABEL = {"high": "Высокая", "medium": "Средняя", "low": "Низкая"}
_FACTOR_LABEL = {
    "know_how": "Знания и умения · Know-How",
    "problem_solving": "Решение вопросов · Problem Solving",
    "accountability": "Ответственность · Accountability",
}
_TEST_DATA_TEXT = (
    "Уровни факторов выбраны офлайн-заглушкой, а не реальным AI-агентом — это "
    "демонстрационный расчёт. Обратитесь к администратору системы, чтобы подключить "
    "реальный агент, и переоцените должность перед выносом на комитет."
)


def _esc(text: str) -> str:
    return escape(text).replace("\n", "<br/>")


def _pm(value: int) -> str:
    if value > 0:
        return " (+)"
    if value < 0:
        return " (−)"
    return ""


def _fmt_pct(value: float) -> str:
    return f"{value:g}"


def _factor_codes(score: ScoreResult) -> dict[str, str]:
    kh = score.know_how.selection
    ps = score.problem_solving.selection
    acc = score.accountability.selection
    return {
        "know_how": f"{kh.specialization} / {kh.management} / {kh.communication}{_pm(kh.plus_minus)}",
        # ProblemComplexity — plain `int, Enum` (не проектный StrEnum), его
        # f-string без .value даёт "ProblemComplexity.VARIABLE", а не "3".
        "problem_solving": f"{ps.area} / {ps.complexity.value}{_pm(ps.plus_minus)} / {_fmt_pct(score.problem_solving.percentage)}%",
        "accountability": (
            f"{acc.freedom} / {acc.magnitude} / "
            f"{acc.non_quantitative_impact or acc.impact or '—'}{_pm(acc.plus_minus)}"
        ),
    }


def _styles(font: str, font_bold: str) -> dict[str, ParagraphStyle]:
    return {
        "h1": ParagraphStyle("h1", fontName=font_bold, fontSize=20, leading=24, spaceAfter=2),
        "h2": ParagraphStyle("h2", fontName=font_bold, fontSize=14, leading=18, spaceAfter=4),
        "h3": ParagraphStyle("h3", fontName=font_bold, fontSize=11, leading=14, spaceAfter=4),
        "body": ParagraphStyle("body", fontName=font, fontSize=10, leading=15, spaceAfter=2),
        "muted": ParagraphStyle("muted", fontName=font, fontSize=9, leading=13, textColor=_MUTED),
        "formula": ParagraphStyle("formula", fontName=font_bold, fontSize=11, leading=16),
        "footnote": ParagraphStyle("footnote", fontName=font, fontSize=8, leading=11, textColor=_MUTED, spaceBefore=6),
        "cell": ParagraphStyle("cell", fontName=font, fontSize=9, leading=12),
        "cell_bold": ParagraphStyle("cell_bold", fontName=font_bold, fontSize=9, leading=12),
    }


def _test_data_banner(styles: dict[str, ParagraphStyle]) -> Table:
    title = Paragraph(
        "⚠ ТЕСТОВЫЕ ДАННЫЕ — НЕ ДЛЯ ОЦЕНОЧНОГО КОМИТЕТА",
        ParagraphStyle("banner_title", fontName=styles["h3"].fontName, fontSize=11, textColor=_ACCENT),
    )
    body = Paragraph(_esc(_TEST_DATA_TEXT), styles["body"])
    table = Table([[title], [body]], colWidths=[174 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbeceb")),
        ("BOX", (0, 0), (-1, -1), 1, _ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def _score_summary_table(evaluation: Evaluation, score: ScoreResult, styles: dict[str, ParagraphStyle]) -> Table:
    labels = ["Грейд", "Итоговый балл", "Профиль", "Надёжность данных"]
    values = [
        str(score.grade),
        str(score.total_points),
        score.profile_long or score.profile.value,
        _CONFIDENCE_LABEL.get(evaluation.confidence.value, evaluation.confidence.value),
    ]
    notes = [
        f"{score.grade_lower}–{score.grade_upper} · {score.grade_zone} зона",
        "Сумма трёх факторов",
        f"{score.profile_steps} шаг(ов)",
        "",
    ]
    header_style = styles["cell"]
    value_style = ParagraphStyle("summary_value", fontName=styles["h2"].fontName, fontSize=16, leading=19)
    note_style = styles["muted"]
    rows = [
        [Paragraph(label, header_style) for label in labels],
        [Paragraph(value, value_style) for value in values],
        [Paragraph(note, note_style) if note else "" for note in notes],
    ]
    table = Table(rows, colWidths=[43.5 * mm] * 4)
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, _BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, _BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table


def _factor_table(score: ScoreResult, evaluation: Evaluation, styles: dict[str, ParagraphStyle]) -> Table:
    codes = _factor_codes(score)
    points = {
        "know_how": score.know_how.points,
        "problem_solving": score.problem_solving.points,
        "accountability": score.accountability.points,
    }
    header = [Paragraph(t, styles["cell_bold"]) for t in ("Фактор", "Код", "Баллы")]
    rows = [header]
    for group in ("know_how", "problem_solving", "accountability"):
        rows.append([
            Paragraph(_FACTOR_LABEL[group], styles["cell"]),
            Paragraph(codes[group], styles["cell"]),
            Paragraph(str(points[group]), styles["cell"]),
        ])
    table = Table(rows, colWidths=[80 * mm, 70 * mm, 24 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f1ec")),
        ("BOX", (0, 0), (-1, -1), 0.5, _BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, _BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (2, 0), (2, -1), "RIGHT"),
    ]))
    return table


def _formula_line(score: ScoreResult) -> str:
    return (
        f"Know-How {score.know_how.points} + "
        f"Problem Solving {score.problem_solving.points} ({_fmt_pct(score.problem_solving.percentage)}%) + "
        f"Accountability {score.accountability.points} = "
        f"Итого {score.total_points} &rarr; Грейд {score.grade} "
        f"· Профиль {escape(score.profile_long or score.profile.value)}"
    )


def _qc_section(flags: list[QCFlag], styles: dict[str, ParagraphStyle]) -> list:
    story: list = [Paragraph("QC-проверки", styles["h3"])]
    if not flags:
        story.append(Paragraph("Проверки не выполнялись.", styles["muted"]))
        return story

    fail = [f for f in flags if f.status.value == "fail"]
    warn = [f for f in flags if f.status.value == "warn"]
    passed = [f for f in flags if f.status.value == "pass"]
    story.append(Paragraph(
        f'<font color="{_ACCENT_HEX}">FAIL: {len(fail)}</font> &nbsp;&nbsp; '
        f'<font color="{_WARN_HEX}">WARN: {len(warn)}</font> &nbsp;&nbsp; '
        f'<font color="{_OK_HEX}">PASS: {len(passed)}</font>',
        styles["body"],
    ))
    for title, items, color in (("Блокирующие", fail, _ACCENT), ("Требуют уточнения", warn, _WARN)):
        if not items:
            continue
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph(title, ParagraphStyle("qc_group", fontName=styles["h3"].fontName, fontSize=10, textColor=color)))
        for flag in items:
            story.append(Paragraph(f"<b>{_esc(flag.message)}</b>", styles["body"]))
            if flag.recommendation:
                story.append(Paragraph(_esc(flag.recommendation), styles["muted"]))
            story.append(Spacer(1, 1.5 * mm))
    return story


def build_evaluation_pdf(position: JobDossier, evaluation: Evaluation) -> bytes:
    """Собирает PDF карточки оценки в байты. Поднимает RuntimeError, если в
    окружении не найден кириллический шрифт (см. `export/fonts.py`)."""
    font, font_bold = register_cyrillic_font()
    styles = _styles(font, font_bold)
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=f"Карточка оценки — {position.name}",
    )

    story: list = []

    if evaluation.is_test_data:
        story.append(_test_data_banner(styles))
        story.append(Spacer(1, 6 * mm))

    story.append(Paragraph(_esc(position.name), styles["h1"]))
    meta = " · ".join(filter(None, [position.dzo, position.department, position.function]))
    if position.snapshot_date:
        date_part = f"дата среза {position.snapshot_date}"
        meta = f"{meta} · {date_part}" if meta else date_part
    if meta:
        story.append(Paragraph(_esc(meta), styles["muted"]))

    version_line = f"оценка от {evaluation.created_at.date().isoformat()}"
    if evaluation.created_by_name:
        version_line += f" · {_esc(evaluation.created_by_name)}"
    if evaluation.is_final:
        version_line += " · финальная версия"
    story.append(Paragraph(version_line, styles["muted"]))
    story.append(Spacer(1, 6 * mm))

    story.append(Paragraph(_STATUS_LABEL.get(evaluation.status.value, evaluation.status.value), styles["h2"]))
    story.append(Paragraph(_STATUS_SUMMARY.get(evaluation.status.value, ""), styles["body"]))
    story.append(Spacer(1, 4 * mm))

    score = evaluation.score
    if score is not None:
        story.append(_score_summary_table(evaluation, score, styles))
        story.append(Spacer(1, 5 * mm))
        story.append(_factor_table(score, evaluation, styles))
        story.append(Spacer(1, 5 * mm))
        story.append(Paragraph(_formula_line(score), styles["formula"]))
        story.append(Spacer(1, 5 * mm))
        if score.calculation_explanation:
            story.append(Paragraph("Подробное объяснение расчёта", styles["h3"]))
            for index, line in enumerate(score.calculation_explanation, start=1):
                story.append(Paragraph(f"{index}. {_esc(line)}", styles["body"]))
            story.append(Spacer(1, 5 * mm))

    if evaluation.role_summary:
        story.append(Paragraph("Резюме должности", styles["h3"]))
        story.append(Paragraph(_esc(evaluation.role_summary), styles["body"]))
        story.append(Spacer(1, 4 * mm))

    if evaluation.reasoning:
        story.append(Paragraph("Обоснование по факторам", styles["h3"]))
        story.append(Paragraph(_esc(evaluation.reasoning), styles["body"]))
        story.append(Spacer(1, 4 * mm))

    story.extend(_qc_section(evaluation.qc_flags, styles))
    story.append(Spacer(1, 4 * mm))

    if evaluation.recommendation:
        story.append(Paragraph("Рекомендация для Оценочного комитета", styles["h3"]))
        story.append(Paragraph(_esc(evaluation.recommendation), styles["body"]))
        story.append(Spacer(1, 4 * mm))

    story.append(Paragraph(
        "Оценка предварительная: итоговый грейд утверждает Оценочный комитет.",
        styles["footnote"],
    ))

    doc.build(story)
    return buffer.getvalue()
